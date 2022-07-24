from backend.core.schemas import PaginationPydantic


def get_pagination(offset: int, limit: int):
    return PaginationPydantic(offset=offset, limit=limit)


