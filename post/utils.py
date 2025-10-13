from re import sub
from typing import Literal

from unidecode import unidecode

from helpers.search import search_param_fabric


def generate_slug(title: str, index: int | None = None) -> str:
    """Приводит строку к виду 'abc-de-f-g' путем
    транслитерации с русского(англ.) на английский
    и отброса специальных символов, убирая их или заменяя на '-'.

    Пример:
    'Привет! каК дела?,.' -> 'privet-kak-dela'"""

    result = sub(
        r"[^a-z0-9]+",
        "-",
        unidecode(f"{title} {index if index else ''}").lower()
    )

    return result.strip("-")


PostSearchParams = search_param_fabric(Literal["slug", "id", "title"])

