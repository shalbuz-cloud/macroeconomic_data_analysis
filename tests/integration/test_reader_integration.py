from dataclasses import astuple

import pytest

from src.models import EconomicRecord
from src.reader import CSVReader


class TestCSVReaderIntegration:
    """Интеграционные тесты для CSVReader с реальными файлами."""

    @pytest.fixture
    def reader(self):
        """Фикстура, возвращающая экземпляр 'читателя' CSV."""
        return CSVReader()

    def test_read_and_validate_real_data(
        self, reader, temp_csv_file_with_data, sample_record_dict
    ):
        """Тест: чтение файла и проверка, что все записи являются EconomicRecord."""
        records = list(reader.read_file(str(temp_csv_file_with_data)))

        assert all(isinstance(rec, EconomicRecord) for rec in records)
        assert len(records) == 1

    def test_read_file_with_multiple_valid_records(
        self, reader, temp_csv_file, sample_records_list
    ):
        """Тест чтения файла с несколькими корректными записями."""
        file_path = str(temp_csv_file)
        with open(file_path, "a", encoding="utf-8") as f:
            for rec in sample_records_list:
                f.write(",".join(map(str, astuple(rec))) + "\n")

        records = reader.read_file(file_path)
        assert len(list(records)) == len(sample_records_list)
