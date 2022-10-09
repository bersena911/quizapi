from dataclasses import dataclass

import pydantic
from fastapi import Query


class BasePaginate(pydantic.BaseModel):
    total_count: int
    limit: int
    offset: int


class Paginate:
    def __class_getitem__(cls, item):
        return pydantic.create_model(
            f"Paginate{item.__name__}", items=(list[item], ...), __base__=BasePaginate
        )


@dataclass
class PaginateSchema:
    limit: int
    offset: int


def pagination_parameters(
    limit: int = Query(15, ge=1, le=20),
    offset: int = 0,
):
    return PaginateSchema(limit=limit, offset=offset)
