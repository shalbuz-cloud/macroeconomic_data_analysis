from dataclasses import dataclass


@dataclass
class EconomicRecord:
    """
    DTO для одной записи экономических данных.
    Соответствует строке CSV файла.
    """

    country: str
    year: int
    gdp: float
    gdp_growth: float
    inflation: float
    unemployment: float
    population: int
    continent: str


@dataclass
class CountryStatistics:
    """DTO для статистики по стране."""

    country: str
    average_gdp: float = 0.0
    year_count: int = 0

    def __post_init__(self) -> None:
        """Округление числовых значений."""
        self.average_gdp = round(self.average_gdp, 2)
