import tempfile
from pathlib import Path
from typing import Any, Iterator

import pytest

from src.models import EconomicRecord


@pytest.fixture
def sample_record_dict() -> dict[str, Any]:
    """Возвращает словарь с корректными данными для создания EconomicRecord."""
    return {
        "country": "Testland",
        "year": 2023,
        "gdp": 1000.5,
        "gdp_growth": 2.5,
        "inflation": 3.0,
        "unemployment": 4.5,
        "population": 50,
        "continent": "Testinia",
    }


@pytest.fixture
def sample_economic_record(sample_record_dict) -> EconomicRecord:
    """Возвращает объект EconomicRecord с корректными тестовыми данными."""
    return EconomicRecord(**sample_record_dict)


@pytest.fixture
def sample_records_list() -> list[EconomicRecord]:
    """Возвращает список записей для нескольких стран и лет."""
    return [
        EconomicRecord(
            country="USA",
            year=2020,
            gdp=21433.2,
            gdp_growth=-2.8,
            inflation=1.2,
            unemployment=8.1,
            population=331,
            continent="North America",
        ),
        EconomicRecord(
            country="USA",
            year=2021,
            gdp=23315.1,
            gdp_growth=5.8,
            inflation=4.7,
            unemployment=5.4,
            population=332,
            continent="North America",
        ),
        EconomicRecord(
            country="Germany",
            year=2020,
            gdp=3846.4,
            gdp_growth=-3.7,
            inflation=0.4,
            unemployment=3.8,
            population=83,
            continent="Europe",
        ),
        EconomicRecord(
            country="Germany",
            year=2021,
            gdp=4259.9,
            gdp_growth=2.6,
            inflation=3.1,
            unemployment=3.6,
            population=83,
            continent="Europe",
        ),
        EconomicRecord(
            country="Japan",
            year=2020,
            gdp=5057.8,
            gdp_growth=-4.3,
            inflation=0.0,
            unemployment=2.0,
            population=126,
            continent="Asia",
        ),
    ]


@pytest.fixture
def sample_valid_record(sample_record_dict) -> dict[str, str]:
    """Фикстура с валидной строкой данных.
    Преобразует числа в строки для CSV-подобных данных.
    """
    return {
        "country": sample_record_dict["country"],
        "year": str(sample_record_dict["year"]),
        "gdp": str(sample_record_dict["gdp"]),
        "gdp_growth": str(sample_record_dict["gdp_growth"]),
        "inflation": str(sample_record_dict["inflation"]),
        "unemployment": str(sample_record_dict["unemployment"]),
        "population": str(sample_record_dict["population"]),
        "continent": sample_record_dict["continent"],
    }


@pytest.fixture
def temp_csv_file() -> Iterator[Path]:
    """Создает временный CSV-файл и возвращает его путь.
    Файл удаляется после теста.
    """
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".csv", delete=False, encoding="utf-8"
    ) as tmp_file:
        file_path = tmp_file.name
        # Записываем стандартный заголовок
        tmp_file.write(
            "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
        )
        tmp_file.flush()  # Важно! Сбрасываем буфер
        yield Path(file_path)
    # Удаляем файл после теста
    Path(file_path).unlink()


@pytest.fixture
def temp_csv_file_with_data(temp_csv_file, sample_record_dict) -> Path:
    """Заполняет временный CSV-файл данными из sample_record_dict."""
    file_path = temp_csv_file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(
            f"{sample_record_dict['country']},{sample_record_dict['year']},{sample_record_dict['gdp']},"
            f"{sample_record_dict['gdp_growth']},{sample_record_dict['inflation']},"
            f"{sample_record_dict['unemployment']},{sample_record_dict['population']},"
            f"{sample_record_dict['continent']}\n"
        )
    return file_path
