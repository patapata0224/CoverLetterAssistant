from pathlib import Path
from datetime import date, datetime
import pandas as pd
import numpy as np

# def is_image_file(path: Path):
#     return path.suffix.lower() in {
#         '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.jfif'
#         }


def is_valid_path(path: str):
    return Path(path).exists() and path != ''



def to_japanese_era(date_value, format_code="ggge"):
    """
    Convert date into string of Japanese style

    Parameters
    ----------
    date_value : datetime.date / datetime.datetime / str
        The date to be converted.
        If str, the format is supposed to be "YYYYMMDD".
    format_code : str
        The format used in Microsoft Excel.
        e.g.
          "ggge"          -> 令和8
          "ggge年m月d日"  -> 令和8年9月13日
          "ge"            -> R8
          "ggee"          -> 令和08

    Returns
    -------
    str
        String in the date style of Japanese
    """

    if isinstance(date_value, datetime):
        dt = date_value.date()
    elif isinstance(date_value, date):
        dt = date_value
    elif isinstance(date_value, str):
        dt = datetime.strptime(date_value, "%Y%m%d").date()
    else:
        raise TypeError("date_value is supposed to be a date, datetime, string in YYYYMMDD style.")

    eras = [
        ("令和", "R", date(2019, 5, 1)),
        ("平成", "H", date(1989, 1, 8)),
        ("昭和", "S", date(1926, 12, 25)),
        ("大正", "T", date(1912, 7, 30)),
        ("明治", "M", date(1868, 1, 25)),
    ]

    era_name = None
    era_alpha = None
    era_start = None

    for name, alpha, start_date in eras:
        if dt >= start_date:
            era_name = name
            era_alpha = alpha
            era_start = start_date
            break

    if era_name is None:
        raise ValueError("This function does not react to a date before Meiji.")

    result = format_code

    result = result.replace("ggg", era_name)
    result = result.replace("gg", era_name[0])
    result = result.replace("g", era_alpha)

    era_year = dt.year - era_start.year + 1
    if "ee" in result:
        result = result.replace("ee", f"{era_year:02d}" if era_year > 1 else "元")
    elif "e" in result:
        result = result.replace("e", str(era_year) if era_year > 1 else "元")
    else:
        result = result.replace("yyyy", str(dt.year))

    result = result.replace("mm", f"{dt.month:02d}")
    result = result.replace("m", str(dt.month))
    result = result.replace("dd", f"{dt.day:02d}")
    result = result.replace("d", str(dt.day))

    return result


def find_rows(df: pd.DataFrame, id_item: str, search_val):
    """
    Find corresponding rows including search value in given header of dataframe

    Parameters
    ----------
    df : DataFrame read by pd.read_csv(if, header=1)
        LIFE exports only this type of csv.
    col_name : str
        String in header items.
        Third argument is searched from this column.
    search_val : int / str
        The value looking for.

    Returns
    -------
    str
        Array of int indicating the rows.
    """

    if id_item not in df.columns:
        raise ValueError(f"Header title '{id_item}' is not found.")

    rows = np.where(df[id_item] == search_val)[0]

    return rows
