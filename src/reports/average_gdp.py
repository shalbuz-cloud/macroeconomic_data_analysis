from tabulate import tabulate

from src.models import CountryStatistics
from src.reports.base import Report


class AverageGDPReport(Report):
    """
    Отчет по среднему ВВП стран.
    Формирует таблицу со странами и их средним ВВП за все годы.
    """

    @property
    def name(self) -> str:
        """
        Уникальный идентификатор отчета.
        Используется в параметре --report командной строки.

        Returns:
            str: 'average_gdp'.
        """
        return "average_gdp"

    @property
    def description(self) -> str:
        """
        Описание отчета для --list-reports.

        Returns:
            str: Краткое описание.
        """
        return "Average GDP by country (arithmetic mean across all years)"

    def generate(self, data: list[CountryStatistics]) -> str:
        """
        Генерирует таблицу со средним ВВП по странам.

        Args:
            data: Список статистик по странам, отсортированный по убыванию ВВП.

        Returns:
            str: Отформатированная таблица для вывода в консоль.
        """

        table_data = []
        for idx, stats in enumerate(data, start=1):
            table_data.append(
                [
                    idx,
                    stats.country,
                    f"{stats.average_gdp:,.2f}",  # Формат с разделителями тысяч
                    stats.years_count,
                ]
            )

        return tabulate(
            table_data,
            headers=["#", "Country", "Average GDP (USD billions)", "Years"],
            tablefmt="grid",
            stralign="left",
            numalign="right",
            floatfmt=".2f",
        )


# Заготовка для будущего отчета (демонстрация расширяемости)
class UnemploymentChangeReport(Report):
    """
    Заготовка для отчета по изменению безработицы.
    Демонстрирует возможность легкого добавления отчетов.
    """

    @property
    def name(self) -> str:
        return "unemployment-trend"

    @property
    def description(self) -> str:
        return "Unemployment rate changes over years (placeholder)"

    def generate(self, data: list[CountryStatistics]) -> str:
        """
        Заглушка для демонстрации расширяемости архитектуры.
        В реальном отчете здесь была бы сложная логика расчета.
        """
        return "Unemployment trend report - to be implemented"
