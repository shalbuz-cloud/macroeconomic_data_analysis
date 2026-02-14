import logging
from abc import ABC, abstractmethod
from typing import ClassVar

from src.models import CountryStatistics

logger = logging.getLogger(__name__)


class Report(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Уникальное имя отчета для идентификации."""
        pass

    @property
    def description(self) -> str:
        """Описание отчета (опционально)."""
        return self.name

    """Абстрактный базовый класс для всех отчетов."""

    @abstractmethod
    def generate(self, data: list[CountryStatistics]) -> str:
        """
        Генерирует отчет в виде строки.

        Args:
            data: Статистические данные для отчета.

        Returns:
            str: Отформатированный отчет (обычно таблица).
        """
        pass


class ReportFactory:
    """
    Фабрика для создания отчетов по имени.
    Позволяет регистрировать новые типы отчетов без изменения существующего кода.
    """

    _reports: ClassVar[dict[str, type[Report]]] = {}

    @classmethod
    def register(cls, name: str, report_class: type[Report]) -> None:
        """
        Регистрирует новый тип отчета.

        Args:
            name: Имя отчета (значение параметра --report).
            report_class: Класс отчета, наследующий Report.
        """
        cls._reports[name] = report_class
        logger.debug(f"Registered report: {name} -> {report_class.__name__}")

    @classmethod
    def create(cls, name: str) -> Report | None:
        """
        Создает экземпляр отчета по имени.

        Args:
            name: Имя зарегистрированного отчета.

        Returns:
            Report: Экземпляр отчета или None, если не найден.
        """
        report_class = cls._reports.get(name)
        if report_class is None:
            logger.error(
                f"Report {name} not found. Available: {list(cls._reports.keys())}"
            )
            return None

        logger.debug(f"Creating report: {name}")
        return report_class()

    @classmethod
    def list_reports(cls) -> dict[str, str]:
        """
        Возвращает словарь всех зарегистрированный отчетов.

        Returns:
            dict[str, str]: {имя_отчета: описание}.
        """
        return {
            name: cls._reports[name]().description
            for name in sorted(cls._reports.keys())
        }
