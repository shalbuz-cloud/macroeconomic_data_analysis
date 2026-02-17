import pytest

from src.reader import CSVReader
from src.utils.validators import ValidationError


class TestCSVReader:
    """Тесты для CSVReader."""

    @pytest.fixture
    def reader(self):
        """Фикстура, возвращающая экземпляр 'читателя' CSV."""
        return CSVReader()

    def test_read_valid_csv(self, reader, temp_csv_file_with_data, sample_record_dict):
        """Тест чтения корректного CSV-файла."""
        file_path = str(temp_csv_file_with_data)
        records = list(reader.read_file(file_path))

        assert len(records) == 1
        record = records[0]
        assert record.country == sample_record_dict["country"]
        assert record.gdp == sample_record_dict["gdp"]

    def test_read_csv_with_extra_spaces(self, reader, temp_csv_file):
        """Тест чтения CSV с пробелами в значениях."""
        file_path = temp_csv_file
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("  USA  , 2020,  21433.2 , -2.8, 1.2, 8.1, 331, North America\n")

        records = reader.read_file(str(file_path))
        record = next(records)

        # Проверяем, что больше нет записей
        with pytest.raises(StopIteration):
            next(records)

        assert record.country == "USA"
        assert record.gdp == 21433.2

    @pytest.mark.parametrize(
        "bad_line,expected_exception,expected_error_substring",
        [
            # Неверный формат GDP (строка вместо числа)
            (
                "USA,2020,gdp,-2.8,1.2,8.1,331,North America",
                ValidationError,
                "Invalid gdp format",
            ),
            # Неверный формат населения
            (
                "USA,2020,21433.2,-2.8,1.2,8.1,not-a-number,North America",
                ValidationError,
                "Invalid population format",
            ),
            # Недостаточно полей - может быть ошибка о population или continent
            (
                "USA,2020,21433.2,-2.8,1.2,8.1",
                ValidationError,
                "Missing or empty value for column",
            ),
            # Пустая строка - не вызывает исключения, просто игнорируется
            ("", None, None),
        ],
    )
    def test_read_invalid_csv_line(
        self,
        reader,
        temp_csv_file,
        bad_line,
        expected_exception,
        expected_error_substring,
    ):
        """Параметризованный тест на неверные строки CSV."""
        file_path = str(temp_csv_file)

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(bad_line + "\n")

        if expected_exception is None:
            # Для пустой строки исключения не должно быть
            records = list(reader.read_file(file_path))
            assert len(records) == 0
        else:
            with pytest.raises(expected_exception) as e:
                list(reader.read_file(file_path))

            error_msg = str(e.value)
            # Проверяем только часть сообщения, так как точное поле может варьироваться
            assert expected_error_substring.lower() in error_msg.lower()

    def test_file_not_found(self, reader):
        """Тест на отсутствие файла."""
        with pytest.raises(FileNotFoundError):
            next(reader.read_file("non_existent_file.csv"))
