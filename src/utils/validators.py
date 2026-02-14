import logging
from typing import Sequence

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
            for col in self.REQUIRED_COLUMNS:
                if col not in row or not row[col].strip():
                    raise ValidationError(
                        f"Row {row_num}: Missing or empty value for column '{col}'"
                    )

            # Проверка года
            year = int(row["year"])
            if year < 1900 or year > 2100:
                raise ValidationError(
                    f"Row {row_num}: Invalid year {year}. Must be between 1900 and 2100"
                )

            # Проверка GDP (должен быть положительным)
            gdp = float(row["gdp"])
            if gdp <= 0:
                raise ValidationError(f"Row {row_num}: GDP must be positive, got {gdp}")

            # Проверка роста GDP (может быть отрицательным)
            float(row["gdp_growth"])

            # Проверка безработицы (неотрицательные проценты)
            unemployment = float(row["unemployment"])
            if unemployment < 0:
                raise ValidationError(
                    f"Row {row_num}: Unemployment cannot be negative, got {unemployment}"
                )

            # Проверка населения (положительное целое)
            population = int(row["population"])
            if population <= 0:
                raise ValidationError(
                    f"Row {row_num}: Population mus be positive, got {population}"
                )

            # Проверка континента (не пустой)
            if not row["continent"].strip():
                raise ValidationError(f"Row {row_num}: Continent cannot be empty")

            return True

        except ValidationError as e:
            raise ValidationError(f"Row {row_num}: Invalid numeric format - {e}") from e
