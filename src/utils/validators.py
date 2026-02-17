import logging
from typing import Sequence, Any

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Исключение для ошибок валидации данных."""

    pass


class EconomicDataValidator:
    """
    Валидатор экономических данных.
    Проверяет заголовки и значения CSV файлов.
    """

    REQUIRED_COLUMNS = {
        "country",
        "year",
        "gdp",
        "gdp_growth",
        "inflation",
        "unemployment",
        "population",
        "continent",
    }

    def validate_header(self, header: Sequence[str]) -> bool:
        """
        Проверяет наличие всех необходимых колонок.

        Args:
            header: Заголовок CSV файла.

        Returns:
            True, если все колонки присутствуют.

        Raises:
            ValidationError: Если отсутствуют обязательные колонки.
        """

        header_set = {col.strip() for col in header}
        missing = self.REQUIRED_COLUMNS - header_set

        if missing:
            raise ValidationError(f"Missing required columns: {', '.join(missing)}")
        return True

    def validate_row(self, row: dict[str, str], row_num: int) -> bool:
        """
        Валидирует одну строку данных.

        Args:
            row: Словарь с данными строки.
            row_num: Номер строки для логирования.

        Returns:
            True, если данные валидны.

        Raises:
            ValidationError: При обнаружении невалидных данных.
        """
        try:
            # Проверка наличия всех ключей
            self._validate_required_fields_present(row, row_num)

            # Валидация года
            self._validate_integer_field(
                row.get("year"), "year", row_num, min_value=1900, max_value=2100
            )

            # Валидация GDP
            self._validate_float_field(
                row.get("gdp"), "gdp", row_num, can_be_negative=False
            )

            # Валидация роста GDP (может быть отрицательным)
            self._validate_float_field(row.get("gdp_growth"), "gdp_growth", row_num)

            # Валидация инфляции
            self._validate_float_field(row.get("inflation"), "inflation", row_num)

            # Валидация безработицы
            self._validate_float_field(
                row.get("unemployment"), "unemployment", row_num, can_be_negative=False
            )

            # Валидация населения (положительное целое)
            population = self._validate_integer_field(
                row.get("population"), "population", row_num, min_value=1
            )
            if population <= 0:
                raise ValidationError(
                    f"Row {row_num}: Population mus be positive, got {population}"
                )

            # Валидация континента (не пустой)
            continent = row.get("continent", "")
            if isinstance(continent, str):
                if not continent.strip():
                    raise ValidationError(f"Row {row_num}: Continent cannot be empty")
            else:
                raise ValidationError(
                    f"Row {row_num}: Continent must be a string, got {type(continent).__name__}"
                )

            return True

        except ValidationError as e:
            # Пробрасываем ValidationError дальше без изменений
            raise
        except Exception as e:
            raise ValidationError(f"Row {row_num}: Unexcepted validation error - {e}") from e

    def _validate_required_fields_present(self, row: dict[str, Any], row_num: int) -> None:
        """Проверяет наличие всех обязательных полей и что они не пусты."""
        for col in self.REQUIRED_COLUMNS:
            value = row.get(col)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"Row {row_num}: Missing or empty value for column '{col}'")

    @staticmethod
    def _validate_integer_field(
            value: int | str | float, field_name: str, row_num: int, min_value: int = None, max_value: int = None
    ) -> int:
        """Валидирует целочисленное поле.

        Args:
            value: Значение для валидации.
            field_name: Имя поля (для сообщения об ошибке).
            row_num: Номер строки.
            min_value: Минимальное допустимое значение (если есть).

        Returns:
            int: Валидное число.

        Raises:
            ValidationError: При ошибке валидации.
        """
        if isinstance(value, int):
            result = value
        else:
            try:
                result = int(value)
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Row {row_num}: Invalid {field_name} format - expected integer, got '{value}'"
                )

        if min_value is not None and result < min_value:
            raise ValidationError(
                f"Row {row_num}: {field_name.capitalize()} must be >= {min_value}, got {result}"
            )

        if max_value is not None and result > max_value:
            raise ValidationError(
                f"Row {row_num}: {field_name.capitalize()} must be <= {max_value}, got {result}"
            )

        return result

    @staticmethod
    def _validate_float_field(
            value: Any, field_name: str, row_num: int, can_be_negative: bool = True
    ) -> float:
        """Валидирует поле с плавающей точкой.

        Args:
            value: Значение для валидации.
            field_name: Имя поля (для сообщения об ошибке).
            row_num: Номер строки.
            can_be_negative: Может ли значение быть отрицательным.

        Returns:
            float: Валидное число с плавающей точкой.

        Raises:
            ValidationError: При ошибке валидации.
        """

        if isinstance(value, float):
            result = value
        else:
            try:
                result = float(value)
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Row {row_num}: Invalid {field_name} format - expected number, got '{value}'"
                )

        if not can_be_negative and result < 0:
            raise ValidationError(
                f"Row {row_num}: {field_name.capitalize()} cannot be negative, got {result}"
            )

        return result


