import csv
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator

from src.models import EconomicRecord
from src.utils.converters import EconomicDataConverter
from src.utils.validators import EconomicDataValidator, ValidationError

logger = logging.getLogger(__name__)


class DataReader(ABC):
    """Абстрактных базовый класс для чтения данных."""

    @abstractmethod
    def read(self, file_paths: list[str]) -> list[EconomicRecord]:
        """Читает данные из файлов."""
        pass


class CSVReader(DataReader):
    """Читатель CSV файлов с экономическими данными."""

    def __init__(
        self,
        validator: EconomicDataValidator | None = None,
        converter: EconomicDataConverter | None = None,
    ):
        """Инициализация читателя.

        Args:
            validator: Валидатор данных (создается по умолчанию).
            converter: Конвертер данных (создается по умолчанию).
        """
        self.validator = validator or EconomicDataValidator()
        self.converter = converter or EconomicDataConverter()

    def read_file(self, file_path: str) -> Generator[EconomicRecord, None, None]:
        """Читает один CSV файл и возвращает генератор записей.

        Args:
            file_path: Путь к CSV файлу.

        Returns:
            EconomicRecord: Объект с экономическими данными.

        Raises:
            FileNotFoundError: Если файл не существует.
            ValidationError: При ошибках валидации.
            csv.Error: При ошибках парсинга CSV.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.debug(f"Reading file: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            # Пробуем определить разделитель
            sample = f.read(1024)
            f.seek(0)

            dialect: type[csv.Dialect]
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                # Если не удалось определить, используем запятую
                dialect = csv.excel

            reader = csv.DictReader(f, delimiter=dialect.delimiter)

            # Валидация заголовка
            self.validator.validate_header(reader.fieldnames or [])

            for row_num, row in enumerate(reader, start=2):
                try:
                    # Очищаем пробелы в ключах и значениях
                    # Защита от None значений
                    clean_row = {}
                    for k, v in row.items():
                        clean_k = k.strip().lower() if k else ""
                        clean_v = v.strip() if v is not None else ""
                        clean_row[clean_k] = clean_v
                        clean_row[clean_k] = clean_v

                    self.validator.validate_row(clean_row, row_num)
                    yield self.converter.to_record(clean_row)

                except ValidationError as e:
                    logger.error(f"Validation error in {file_path}:{row_num}: {e}")
                    raise

    def read(self, file_paths: list[str]) -> list[EconomicRecord]:
        """Читает все CSV файлы и объединяет результаты.

        Args:
            file_paths: Список путей к CSV файлам.

        Returns:
            list[EconomicRecord]: Список всех записей из всех файлов.

        Raises:
            ValueError: Если список файлов пуст.
            FileNotFoundError: Если один из файлов не существует.
        """
        if not file_paths:
            raise ValueError("No files provided for reading")

        all_records = []

        for file_path in file_paths:
            try:
                records = list(self.read_file(file_path))
                all_records.extend(records)
                logger.info(f"Loaded {len(records)} records from {file_path}")
            except Exception as e:
                logger.error(f"Failed to read {file_path}: {e}")
                raise

        logger.info(f"Total records loaded: {len(all_records)}")
        return all_records
