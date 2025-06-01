from typing import Annotatede

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[
        int | None,
        Query(1, ge=1, description="Номер страницы"),
    ]
    per_page: Annotated[
        int | None,
        Query(None, ge=1, lt=100, description="Количество отелей на странице"),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]
