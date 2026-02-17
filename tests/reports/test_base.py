
from src.reports.average_gdp import AverageGDPReport
from src.reports.base import ReportFactory


class TestReportFactory:
    """Тесты фабрики отчетов."""

    def test_register_and_create_report(self):
        """Тест регистрации и создания отчета."""
        # Проверяем, что AverageGDPReport уже зарегистрирован в __init__.py
        report = ReportFactory.create("average-gdp")
        assert isinstance(report, AverageGDPReport)

    def test_create_unknown_report(self, caplog):
        """Тест на запрос неизвестного отчета."""
        report_name = "non-existent-report"
        report = ReportFactory.create(report_name)

        assert report is None
        assert len(caplog.records) > 0
        assert f"Report {report_name} not found" in caplog.text
        assert f"Available: {list(ReportFactory.list_reports().keys())}" in caplog.text
