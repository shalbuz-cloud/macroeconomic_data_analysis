import pytest

from src.calculator import GDPCalculator
from src.models import CountryStatistics


class TestGDPCalculator:
    """Тесты для GDPCalculator."""

    @pytest.fixture
    def calculator(self):
        """Фикстура, возвращающая экземпляр калькулятора ВВП."""
        return GDPCalculator()

    def test_calculate_average_gdp_single_country(
        self, calculator, sample_records_list
    ):
        """Тест расчета среднего ВВП для одной страны (США)."""
        usa_records = [r for r in sample_records_list if r.country == "USA"]
        records = calculator.calculate(usa_records)
        assert len(records) == 1
        # (21433.2 + 23315.1) / 2 = 22374.15
        assert records[0].average_gdp == pytest.approx(22374.15)

    def test_calculate_average_gdp_multiple_countries(
        self, calculator, sample_records_list
    ):
        """Тест расчета среднего ВВП для нескольких стран."""
        stats_list = calculator.calculate(sample_records_list)

        assert len(stats_list) == 3  # USA, Germany, Japan
        assert all(isinstance(stat, CountryStatistics) for stat in stats_list)

        stats_dict = {stat.country: stat for stat in stats_list}
        assert stats_dict["USA"].average_gdp == pytest.approx(22374.15)
        assert stats_dict["Germany"].average_gdp == pytest.approx(
            4053.15
        )  # (3846.4 + 4259.9) / 2
        assert stats_dict["Japan"].average_gdp == pytest.approx(5057.8)

    def test_calculate_average_gdp_empty_list(self, calculator, caplog):
        """Тест на пустом списке."""
        result = calculator.calculate([])
        assert result == []

        # Проверяем, что было зарегистрировано предупреждение
        assert len(caplog.records) > 0
        assert "No records provided" in caplog.text
        assert caplog.records[0].levelname == "WARNING"
