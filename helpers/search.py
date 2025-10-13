from fastapi import Query
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, le=15, default=10)


def search_param_fabric(allowed_fields: type[str]):
    class SearchParams:
        def __init__(
            self,
            q: str = Query(..., min_length=1, description="Значение запроса"),
            field: allowed_fields = Query(..., description="Критерий запроса"),
            strict: bool = Query(False, description="Строгое совпадение"),
        ):
            self.q = q
            self.strict = strict
            self.field = field

    return SearchParams
