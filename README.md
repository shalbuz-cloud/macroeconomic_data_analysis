# Macroeconomic Data Analyzer

Скрипт для анализа макроэкономических данных из CSV файлов. Формирует отчет со средним ВВП по странам.

---

## Требования

- Python 3.12+
- Poetry (для управления зависимостями)

---

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/shalbuz-cloud/macroeconomic_data_analysis.git
cd macroeconomic-analyzer

# Установка зависимостей
poetry install

# Активация виртуального окружения
poetry shell
```

---

## Использование

#### Базовый запуск

```bash
# Активируйте окружение (если еще не активировано)
poetry shell

# Анализ одного файла
python main.py --files data2023.csv --report average-gdp

# Анализ нескольких файлов
python main.py --files data2023.csv data2024.csv --report average-gdp

# Использование wildcards
python main.py --files *.csv --report average-gdp

# Сокращенная запись (флаг -f)
python main.py -f data2023.csv -r average-gdp

# С отладочной информацией
python main.py --files data.csv --report average-gdp --debug
```

#### Просмотр доступных отчетов

```bash
python main.py --list-reports
```
---

## Формат CSV файлов

Файлы должны содержать следующие колонки (порядок не важен):

| Колонка      | Описание        | Пример        |
|:-------------|:----------------|:--------------|
| country      | Название страны | United States |
| year         | Год             | 2023          |
| gdp ВВП      | (млрд USD)      | 25462         |
| gdp_growth   | Рост ВВП (%)    | 2.1           |
| inflation    | Инфляция (%)    | 3.4           |
| unemployment | Безработица (%) | 3.7           |
| population   | Население (млн) | 339           |
| continent    | Континент North | America       |

## Пример файла

```csv
country,year,gdp,gdp_growth,inflation,unemployment,population,continent
United States,2023,25462,2.1,3.4,3.7,339,North America
China,2023,17963,5.2,2.5,5.2,1425,Asia
Germany,2023,4086,-0.3,6.2,3.0,83,Europe
```

## Пример вывода

```text
$ python main.py --files economic_data.csv --report average-gdp

+-----+----------------+------------------------------+---------+
|   # | Country        | Average GDP (USD billions)   |   Years |
+=====+================+==============================+=========+
|   1 | United States  | 23,923.67                    |       3 |
+-----+----------------+------------------------------+---------+
|   2 | China          | 17,810.33                    |       3 |
+-----+----------------+------------------------------+---------+
|   3 | Japan          | 4,467.00                     |       3 |
+-----+----------------+------------------------------+---------+
```

---

## Архитектура и расширяемость

Проект спроектирован с возможностью легкого добавления новых отчетов.

#### Структура проекта
```text
macroeconomic-analyzer/
├── main.py # Точка входа
├── pyproject.toml # Конфигурация Poetry
├── src/
│   ├── __init__.py
│   ├── models.py # DTO (EconomicRecord, CountryStatistics)
│   ├── reader.py # Чтение CSV с валидацией
│   ├── calculator.py # Калькуляторы статистик (GDPCalculator)
│   ├── analyzer.py # Фасад для анализа
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py     # Валидация (отдельно)
│   │   └── converters.py     # Конвертация (отдельно)
│   └── reports/ # Отчеты (паттерн Strategy)
│   ├── __init__.py # Регистрация отчетов
│   ├── base.py # ReportFactory
│   └── average_gdp.py # Основной отчет
├── tests/ # Pytest тесты
└── README.md
```

---

## 🔄 Процесс добавления нового отчета:

#### 1. Создайте класс отчета в новом файле `src/reports/`:

Например `src/reports/population.py`:
```python
from src.reports.base import Report
from src.models import CountryStatistics

class PopulationReport(Report):
    @property
    def name(self) -> str:
        return "population-by-continent"
    
    def generate(self, data: list[CountryStatistics]) -> str:
        # логика отчета
        return "таблица"
```

#### 2. Зарегистрируйте отчет в `src/reports/__init__.py`:

```python
from src.reports.base import ReportFactory
from src.reports.average_gdp import AverageGDPReport
from src.reports.population import PopulationReport  # ✅ новый импорт

# Регистрация
ReportFactory.register('average-gdp', AverageGDPReport)
ReportFactory.register('population-by-continent', PopulationReport)  # ✅ новая регистрация
```

#### 3. Добавьте калькулятор (если нужны новые метрики) в `src/calculator.py`.

Готово! Новый отчет автоматически доступен через `--report population-by-continent`.

---

## Тестирование

```bash
# Все тесты
poetry run pytest tests/

# С покрытием
poetry run pytest --cov=src tests/

# Конкретный тест
poetry run pytest tests/test_calculator.py -v

# С подробным выводом
poetry run pytest -v --tb=short
```

---

## Разработка
```bash

# Установка dev-зависимостей
poetry install --with dev

# Линтинг (ruff)
poetry run ruff check .

# Форматирование (black)
poetry run black .

# Проверка типов (mypy)
poetry run mypy src/

# Все проверки одной командой
poetry run ruff check . && poetry run mypy core/ && poetry run pytest
```