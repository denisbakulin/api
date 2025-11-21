from fastapi import Query


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
