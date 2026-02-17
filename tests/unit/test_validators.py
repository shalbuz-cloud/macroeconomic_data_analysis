import pytest

from src.utils.validators import EconomicDataValidator, ValidationError


class TestEconomicDataValidator:
    """Тесты для EconomicDataValidator."""

    @pytest.fixture
    def validator(self):
        """Фикстура, возвращающая экземпляр валидатора."""
        return EconomicDataValidator()

    class TestValidateHeader:
        """Тесты для метода validate_header."""

        def test_valid_header(self, validator):
            """Тест корректного заголовка."""
            assert validator.validate_header(list(validator.REQUIRED_COLUMNS)) is True

        def test_header_with_extra_columns(self, validator):
            header = list(validator.REQUIRED_COLUMNS)
            header.extend(["extra1", "extra2"])
            assert validator.validate_header(header) is True

        def test_header_with_spaces(self, validator):
            """Тест заголовка с пробелами в названиях колонок."""
            header = [
                " country ",
                " year ",
                " gdp ",
                " gdp_growth ",
                " inflation ",
                " unemployment ",
                " population ",
                " continent ",
            ]
            assert validator.validate_header(header) is True

        @pytest.mark.parametrize(
            "missing_column",
            [
                "country",
                "year",
                "gdp",
                "gdp_growth",
                "inflation",
                "unemployment",
                "population",
                "continent",
            ],
        )
        def test_missing_column(self, validator, missing_column):
            """Тест на отсутствие каждой обязательной колонки."""
            header = list(validator.REQUIRED_COLUMNS)
            header.remove(missing_column)

            with pytest.raises(ValidationError, match="Missing required columns") as e:
                validator.validate_header(header)

            assert missing_column in str(e.value)

        def test_multiple_missing_columns(self, validator):
            """Тест на отсутствие нескольких колонок."""
            header = ["country", "year", "gdp"]  # Только 3 колонки
            missing_columns = list(validator.REQUIRED_COLUMNS - set(header))

            with pytest.raises(ValidationError, match="Missing required columns") as e:
                validator.validate_header(header)

            # Проверяем, что все отсутствующие колонки перечислены
            error_ms = str(e.value)
            for col in missing_columns:
                assert col in error_ms

        def test_empty_header(self, validator):
            """Тест пустого заголовка."""
            with pytest.raises(ValidationError, match="Missing required columns") as e:
                validator.validate_header([])

            assert all(col in str(e) for col in validator.REQUIRED_COLUMNS)

    class TestValidateRow:
        """Тесты для метода validate_row."""

        def test_validate_row_with_strings(self, validator, sample_valid_record):
            """Тест корректной строки с данными в формате CSV (все строки)."""
            assert validator.validate_row(sample_valid_record, row_num=2) is True

        def test_valid_row_with_numbers(self, validator, sample_record_dict):
            """Тест корректной строки с числами вместо строк."""
            assert validator.validate_row(sample_record_dict, row_num=2) is True

        @pytest.mark.parametrize(
            "field,value",
            [
                ("gdp", 1000.5),
                ("gdp_growth", -2.5),
                ("inflation", 3.0),
                ("unemployment", 4.5),
            ],
        )
        def test_float_fields_with_numbers(
            self, validator, sample_record_dict, field, value
        ):
            """Тест, что валидатор принимает уже преобразованные float."""
            test_row = sample_record_dict.copy()
            test_row[field] = value
            assert validator.validate_row(test_row, row_num=2) is True

        @pytest.mark.parametrize(
            "missing_field",
            [
                "country",
                "year",
                "gdp",
                "gdp_growth",
                "inflation",
                "unemployment",
                "population",
                "continent",
            ],
        )
        def test_missing_field(self, validator, sample_valid_record, missing_field):
            """Тест на отсутствие каждого обязательного поля."""
            invalid_row = sample_valid_record.copy()
            del invalid_row[missing_field]

            with pytest.raises(ValidationError, match="Missing or empty value for column"):
                validator.validate_row(invalid_row, row_num=2)

        @pytest.mark.parametrize(
            "field",
            [
                "country",
                "year",
                "gdp",
                "gdp_growth",
                "inflation",
                "unemployment",
                "population",
                "continent",
            ],
        )
        def test_empty_string_field(self, validator, sample_valid_record, field):
            """Тест на пустые строковые значения."""
            invalid_row = sample_valid_record.copy()
            invalid_row[field] = ""

            with pytest.raises(
                ValidationError, match="Missing or empty value for column"
            ):
                validator.validate_row(invalid_row, row_num=2)

        @pytest.mark.parametrize(
            "field",
            [
                "country",
                "year",
                "gdp",
                "gdp_growth",
                "inflation",
                "unemployment",
                "population",
                "continent",
            ],
        )
        def test_whitespace_only_field(self, validator, sample_valid_record, field):
            """Тест на поля, содержащие только пробелы."""
            invalid_row = sample_valid_record.copy()
            invalid_row[field] = "   "

            with pytest.raises(ValidationError) as e:
                validator.validate_row(invalid_row, row_num=2)

            assert f"Missing or empty value for column '{field}'" in str(e.value)

        def test_none_value(self, validator, sample_valid_record):
            """Тест на значение None в поле."""
            invalid_row = sample_valid_record.copy()
            invalid_row["country"] = None

            with pytest.raises(
                ValidationError, match="Missing or empty value for column 'country'"
            ):
                validator.validate_row(invalid_row, row_num=2)

        @pytest.mark.parametrize(
            "year,expected_valid",
            [
                (1900, True),
                (2000, True),
                (2023, True),
                (2100, True),
                (1899, False),
                (2101, False),
            ],
        )
        def test_year_validation(
            self, validator, sample_valid_record, year, expected_valid
        ):
            """Тест граничных значений года."""
            test_row = sample_valid_record.copy()
            test_row["year"] = str(year)

            if expected_valid:
                assert validator.validate_row(test_row, row_num=2) is True
            else:
                with pytest.raises(ValidationError, match="Year must be"):
                    validator.validate_row(test_row, row_num=2)
