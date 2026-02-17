import pytest

from src.models import CountryStatistics, EconomicRecord


class TestEconomicRecord:
    """Тесты для модели EconomicRecord."""

    def test_economic_record_creation(self, sample_record_dict):
        """Тест успешного создания EconomicRecord из словаря."""
        record = EconomicRecord(**sample_record_dict)

        for key, value in sample_record_dict.items():
            assert getattr(record, key) == value


class TestCountryStatistics:
    """Тесты для модели CountryStatistics."""

    def test_country_statistics_creation(self):
        """Тест создания объекта и проверки на округление."""
        stats = CountryStatistics(
            country="Testland",
            average_gdp=1500.7556,
            years_count=3,
        )

        assert stats.country == "Testland"
        assert stats.average_gdp == 1500.76
        assert stats.years_count == 3

    @pytest.mark.parametrize(
        "avg_gdp,years_count",
        [
            (0, 1),
            (1000.5, 5),
            (999999.99, 10),
        ],
    )
    def test_valid_statistics_values(self, avg_gdp, years_count):
        """Тест корректных значений статистики."""
        stats = CountryStatistics(
            country="Testland",
            average_gdp=avg_gdp,
            years_count=years_count,
        )
        assert stats.average_gdp == avg_gdp
        assert stats.years_count == years_count
