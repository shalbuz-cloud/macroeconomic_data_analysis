import pytest

from src.models import EconomicRecord
from src.utils.converters import EconomicDataConverter


class TestEconomicDataConverter:
    """Тесты для EconomicDataConverter."""

    @pytest.fixture
    def converter(self):
        """Фикстура, возвращающая экземпляр конвертера."""
        return EconomicDataConverter()

    class TestConverterToRecord:
        """Тесты для метода to_record."""

        def test_valid_data(self, converter, sample_valid_record, sample_record_dict):
            """Тест конвертации валидных данных."""
            record = converter.to_record(sample_valid_record)

            assert isinstance(record, EconomicRecord)
            for key, value in sample_record_dict.items():
                assert getattr(record, key) == value

        def test_with_numeric_strings(self, converter):
            """Тест конвертации числовых строк."""
            row = {
                "country": "Germany",
                "year": "2020",
                "gdp": "3846.4",
                "gdp_growth": "-3.7",
                "inflation": "0.4",
                "unemployment": "3.8",
                "population": "83",
                "continent": "Europe",
            }

            record = converter.to_record(row)

            assert record.year == 2020  # строка в int
            assert record.gdp == 3846.4  # строка в float
            assert record.population == 83  # строка в int

        @pytest.mark.parametrize(
            "field,value,expected_type",
            [
                ("year", "2023", int),
                ("gdp", "1000.5", float),
                ("gdp_growth", "2.5", float),
                ("inflation", "3.0", float),
                ("unemployment", "4.5", float),
                ("population", "50", int),
            ],
        )
        def test_type_conversion(
            self, converter, sample_valid_record, field, value, expected_type
        ):
            """Тест преобразования типов."""
            row = sample_valid_record.copy()
            row[field] = value

            record = converter.to_record(row)

            assert isinstance(getattr(record, field), expected_type)

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
        def test_missing_field(self, converter, sample_valid_record, missing_field):
            """Тест на отсутствие обязательного поля вызывает KeyError."""
            row = sample_valid_record.copy()
            del row[missing_field]

            with pytest.raises(KeyError, match=missing_field):
                converter.to_record(row)
