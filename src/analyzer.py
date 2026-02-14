import logging

from src.calculator import GDPCalculator, StatisticsCalculator
from src.reader import CSVEconomicReader
from src.reports.base import ReportFactory

logger = logging.getLogger(__name__)


class MacroEconomicAnalyzer:
    """
    Фасад для анализа макроэкономических данных.

    Скрывает сложность подсистем (чтение CSV, расчет статистик, генерация отчетов)
    за простым интерфейсом.

    Пример использования:
        >>> analyzer = MacroEconomicAnalyzer()
        >>> result = analyzer.analyze(["data.csv"], "average-gdp")
        >>> print(result)
    """

    def __init__(
        self,
        reader: CSVEconomicReader | None = None,
        calculator: StatisticsCalculator | None = None,
    ):
        """
        Инициализация анализатора.

        Args:
            reader: Читатель CSV файлов (создается по умолчанию).
            calculator: Калькулятор статистик (создается по умолчанию).
        """
        self.reader = reader or CSVEconomicReader()
        self.calculator = calculator or GDPCalculator()
        logger.debug(
            f"Initialized MacroEconomicAnalyzer with {type(self.calculator).__name__}"
        )

    def analyze(self, file_paths: list[str], report_type: str) -> str:
        """
        Выполняет полный цикл анализа данных.

        Этапы:
        1. Чтение данных из CSV файлов.
        2. Расчет статистик по странам.
        3. Генерация отчета.
        4. Возврат отформатированного результата.

        Args:
            file_paths: Список путей к CSV файлам.
            report_type: Тип отчета (например, 'average-gdp').

        Returns:
            str: Готовый к выводу в консоль отчет.

        Raises:
            FileNotFoundError: Если один из файлов не существует.
            ValidationError: При ошибках валидации данных.
            ValueError: Если указан неизвестный тип отчета.
        """
        logger.info(
            f"Starting analysis with {len(file_paths)} file(s), report: {report_type}"
        )

        # Шаг 1: Чтение данных
        records = self.reader.read(file_paths)
        logger.info(f"Loaded {len(records)} records total")

        # Шаг 2: Расчет статистик
        statistics = self.calculator.calculate(records)
        logger.info(f"Calculated statistics for {len(statistics)} countries")

        # Шаг 3: Создание отчета
        report = ReportFactory.create(report_type)
        if report is None:
            available = ReportFactory.list_reports()
            raise ValueError(
                f"Unknown report type: '{report_type}'. "
                f"Available reports: {list(available.keys())}"
            )

        # Шаг 4: Генерация отчета
        result = report.generate(statistics)
        logger.info(f"Report '{report_type}' generated successfully")

        return result

    @staticmethod
    def get_available_reports() -> dict:
        """
        Возвращает список доступных отчетов.

        Returns:
            dict[str, str]: Словарь {имя_отчета: описание}.
        """
        return ReportFactory.list_reports()


# Для обратной совместимости и удобства импорта
def analyze_economic_data(
    file_paths: list[str],
    report_type: str,
) -> str:
    """
    Функция-обертка для быстрого запуска анализа.

    Args:
        file_paths: Список CSV файлов.
        report_type: Тип отчета.

    Returns:
        str: Результат анализа.
    """
    analyzer = MacroEconomicAnalyzer()
    return analyzer.analyze(file_paths, report_type)
