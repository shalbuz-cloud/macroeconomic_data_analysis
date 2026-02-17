import pytest

from src.calculator import GDPCalculator
from src.reports.average_gdp import AverageGDPReport


class TestAverageGDPReport:
    """Тесты для AverageGDPReport."""

    @pytest.fixture
    def report(self):
        """Фикстура, возвращающая экземпляр отчета ВВП."""
        return AverageGDPReport()

    @pytest.fixture
    def calculator(self):
        """Фикстура, возвращающая экземпляр калькулятора ВВП."""
        return GDPCalculator()

    def test_generate_report_with_data(self, report, calculator, sample_records_list):
        """Тест генерации отчета с данными"""
        statistics = calculator.calculate(sample_records_list)

        result = report.generate(statistics)

        assert "USA" in result
        assert "Germany" in result
        assert "Japan" in result
        assert "22,374.15" in result or "22374.15" in result
        assert report.name == "average_gdp"
