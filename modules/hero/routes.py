from fastapi import APIRouter, Query
from .schemas import HeroCreate, HeroUpdate, HeroResponse
from database import SessionDep
from .service import create, read, read_one, update, delete
from typing import Annotated
from uuid import UUID

hero_router = APIRouter(prefix="/hero", tags=["Hero"])


@hero_router.post("/", tags=["Hero"], response_model=HeroResponse)
def create_hero(data: HeroCreate, session: SessionDep) -> HeroResponse:
    return create(data, session)


@hero_router.get("/", tags=["Hero"], response_model=list[HeroResponse])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Máximo de itens por página.")
    ] = 100,
) -> list[HeroResponse]:
    return read(session, offset, limit)


@hero_router.get("/{hero_id}", tags=["Hero"], response_model=HeroResponse)
def read_one_hero(session: SessionDep, hero_id: UUID) -> HeroResponse:
    return read_one(session, hero_id)


@hero_router.patch("/{hero_id}", tags=["Hero"], response_model=HeroResponse)
def update_hero(session: SessionDep, hero_id: UUID, data: HeroUpdate) -> HeroResponse:
    return update(session, hero_id, data)


@hero_router.delete("/{hero_id}", status_code=204)
def delete_hero(session: SessionDep, hero_id: UUID):
    return delete(session, hero_id)
