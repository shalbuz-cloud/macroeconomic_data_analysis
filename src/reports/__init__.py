# Регистрация отчетов
from src.reports.average_gdp import AverageGDPReport
from src.reports.base import ReportFactory

ReportFactory.register("average-gdp", AverageGDPReport)

# Демонстрация расширяемости - регистрируем заготовки будущих отчетов
# Раскомментируйте, когда добавите реальные реализации
# from src.reports.average_gdp import UnemploymentChangeReport
# ReportFactory.register("unemployment-trend", UnemploymentChangeReport)

__all__ = [
    "ReportFactory",
    "AverageGDPReport",
]
