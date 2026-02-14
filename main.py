#!/usr/bin/env python3
"""
Скрипт для анализа макроэкономических данных.
Читает CSV файлы с экономическими показателями и формирует отчеты.

Примеры запуска:
    python main.py --files data2023.csv data2024.csv --report average-gdp
    python main.py --files *.csv --report average-gdp
    python main.py --list-reports
"""

import argparse
import logging
import sys

from src.analyzer import MacroEconomicAnalyzer

logging.basicConfig(
    level=logging.CRITICAL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger(__name__)


def setup_argparse() -> argparse.ArgumentParser:
    """
    Настройка парсера аргумента командной строки.

    Returns:
        argparse.ArgumentParser: Настроенный парсер.
    """
    parser = argparse.ArgumentParser(
        description="Analyze macroeconomic data from CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --files data2023.csv --report average-gdp
  %(prog)s --files *.csv --report average-gdp
  %(prog)s --list-reports
        """,
    )

    # Основные аргументы
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="CSV files with economic data (country,year,gdp,gdp_growth,inflation,unemployment,population,continent)",
    )

    parser.add_argument(
        "--report",
        required=True,
        help="Type of report to generate (use --list-reports to see available)",
    )

    # Полезные дополнительные аргументы
    parser.add_argument(
        "--list-reports",
        action="store_true",
        help="Show all available reports and exit",
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    return parser


def main(args: list[str] | None = None) -> int:
    """
    Основная функция скрипта.

    Args:
        args: Аргументы командной строки (по умолчанию sys.argv[1:]).

    Returns:
        int: Код возврата (0 - успех, 1 - ошибка).
    """
    parser = setup_argparse()
    parsed_args: argparse.Namespace = parser.parse_args(args)

    # Настройка уровня логирования
    if parsed_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    try:
        analyzer = MacroEconomicAnalyzer()

        # Отдельный режим для --list-reports
        if parsed_args.list_reports:
            reports = analyzer.get_available_reports()
            print("\nAvailable reports:")
            print("-" * 40)
            for name, description in reports.items():
                print(f"  {name:<20} - {description}")
            return 0

        # Основной режим анализа
        logger.info(f"Starting analysis with files: {parsed_args.files}")
        logger.info(f"Report type: {parsed_args.report}")

        result = analyzer.analyze(parsed_args.files, parsed_args.report)

        # Вывод результата в консоль
        print(result)

        return 0

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        logger.error(f"Argument error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
