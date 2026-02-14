from src.models import EconomicRecord


class EconomicDataConverter:
    """
    Конвертер сырых данных в объекты EconomicRecord.
    Отвечает только за преобразование типов и создание DTO.
    """

    @staticmethod
    def to_record(row: dict[str, str]) -> EconomicRecord:
        """
        Преобразует строку CSV в объект EconomicRecord.

        :param row: Словарь с данными из CSV (уже очищенный)
        :return: EconomicRecord: Объект с экономическими данными
        """
        return EconomicRecord(
            country=row["country"].strip(),
            year=int(row["year"]),
            gdp=float(row["gdp"]),
            gdp_growth=float(row["gdp_growth"]),
            inflation=float(row["inflation"]),
            unemployment=float(row["unemployment"]),
            population=int(row["population"]),
            continent=row["continent"].strip(),
        )
