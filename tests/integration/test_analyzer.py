
import pytest

from src.analyzer import Analyzer


class TestAnalyzer:
    """Интеграционные тесты для Analyzer."""

    @pytest.fixture
    def analyzer(self):
        """Фикстура, возвращающая экземпляр фасада Analyzer."""
        return Analyzer()

    def test_analyze_single_file(
        self, analyzer, temp_csv_file_with_data, sample_record_dict
    ):
        """Тест анализа одного файла через фасад Analyzer."""
        file_paths = [str(temp_csv_file_with_data)]

        result = analyzer.analyze(file_paths, "average-gdp")

        assert result is not None
        assert isinstance(result, str)
        assert sample_record_dict["country"] in result
        # Проверяем форматирование таблицы (наличие символов таблицы)
        assert "+" in result and "|" in result

    def test_analyze_multiple_files(self, analyzer, temp_csv_file_with_data, tmp_path):
        """Тест анализа двух временных файлов."""
        # Создаем второй временный файл с другой записью
        file2_path = tmp_path / "data2.csv"
        with open(file2_path, "w", encoding="utf-8") as f:
            f.write(
                "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
            )
            f.write("Atlantis,2023,2000.0,3.0,2.0,5.0,10,Mythica\n")

        file_paths = [str(temp_csv_file_with_data), str(file2_path)]

        result = analyzer.analyze(file_paths, "average-gdp")

        assert "Testland" in result
        assert "Atlantis" in result

    def test_analyze_with_empty_file_list(self, analyzer):
        """Тест с пустыми списком файлов."""
        with pytest.raises(ValueError, match="No files provided"):
            analyzer.analyze([], "average-gdp")

    def test_analyze_with_nonexistent_file(self, analyzer):
        """Тест с несуществующим файлом."""
        file_paths = ["nonexistent-file.csv"]

        with pytest.raises(FileNotFoundError):
            analyzer.analyze(file_paths, "average-gdp")
