import logging
from abc import ABC, abstractmethod
from collections import defaultdict

from src.models import CountryStatistics, EconomicRecord

logger = logging.getLogger(__name__)


class StatisticsCalculator(ABC):
    """Абстрактный базовый класс для калькуляторов статистик."""

    @abstractmethod
    def calculate(self, records: list[EconomicRecord]) -> list[CountryStatistics]:
        """
        Рассчитывает статистику на основе экономических данных.

        Args:
            records: Список экономических записей.

        Returns:
            list[CountryStatistics]: Список статистик по странам.
        """
        pass


class GDPCalculator(StatisticsCalculator):
    """
    Калькулятор среднего ВВП по странам.
    Вычисляет среднее арифметическое GDP по всем годам для каждой страны.
    """

    def calculate(self, records: list[EconomicRecord]) -> list[CountryStatistics]:
        """
        Вычисляет средний ВВП для всех стран.

        Args:
            records: Список экономических записей.

        Returns:
            list[CountryStatistics]: Отсортированный по убыванию ВВП список.
        """
        if not records:
            logger.warning("No records provided for calculation")
            return []

        # Агрегация данных по странам
        country_stats: dict[str, dict[str, float]] = defaultdict(
            lambda: {"total_gdp": 0.0, "count": 0}
        )

        for record in records:
            stats = country_stats[record.country]
            stats["total_gdp"] += record.gdp
            stats["count"] += 1

        # Формирование результатов
        statistics = []
        for country, data in country_stats.items():
            avg_gdp = data["total_gdp"] / data["count"]
            statistics.append(
                CountryStatistics(
                    country=country,
                    average_gdp=avg_gdp,
                    years_count=int(data["count"]),
                )
            )
            logger.debug(
                f"Country: {country}, Avg GDP: {avg_gdp:.2f}, Years: {data['count']}"
            )

        # Сортировка по убыванию среднего ВВП
        result: list[CountryStatistics] = sorted(
            statistics,
            key=lambda x: x.average_gdp,
            reverse=True,
        )

        logger.info(f"Calculated statistics for {len(result)} countries")
        return result


# Заготовка для будущих отчетов (демонстрация расширяемости)
class UnemploymentTrendCalculator(StatisticsCalculator):
    """
    Калькулятор трендов безработицы.
    Заготовка для демонстрации возможности добавления отчетов.
    """

    def calculate(self, records: list[EconomicRecord]) -> list[CountryStatistics]:
        """
        Заглушка для демонстрации расширяемости.
        В реальном отчете здесь был бы расчет изменения безработицы.
        """
        logger.info("UnemploymentTrendCalculator is a placeholder for future reports")
        return []


class PopulationByContinentCalculator(StatisticsCalculator):
    """
    Калькулятор населения по континентам.
    Заготовка для демонстрации возможности добавления новых отчетов.
    """

    def calculate(self, records: list[EconomicRecord]) -> list[CountryStatistics]:
        """
        Заглушка для демонстрации расширяемости.
        В реальном отчете здесь была бы агрегация по континентам.
        """
        logger.info(
            "PopulationByContinentCalculator is a placeholder for future reports"
        )
        return []
