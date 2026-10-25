from fastapi import APIRouter, Query
from database import SessionDep
from .schemas import MissionCreate, MissionUpdate, MissionResponse
from .service import create, read, read_one, update, delete
from typing import Annotated
from uuid import UUID, uuid4

mission_router = APIRouter(prefix="/mission", tags=["Mission"])


@mission_router.post("/", tags=["Mission"], response_model=MissionResponse)
def create_mission(data: MissionCreate, session: SessionDep) -> MissionResponse:
    return create(data, session)


@mission_router.get("/", tags=["Mission"], response_model=list[MissionResponse])
def read_missions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Máximo de itens por página.")
    ] = 100,
) -> list[MissionResponse]:
    return read(session, offset, limit)


@mission_router.get("/{mission_id}", tags=["Mission"], response_model=MissionResponse)
def read_one_mission(mission_id: UUID, session: SessionDep) -> MissionResponse:
    return read_one(mission_id, session)


@mission_router.patch("/{mission_id}", tags=["Mission"], response_model=MissionResponse)
def update_mission(
    mission_id: UUID, data: MissionUpdate, session: SessionDep
) -> MissionResponse:
    return update(mission_id, data, session)


@mission_router.delete("/{mission_id}", tags=["Mission"], status_code=204)
def delete_mission(mission_id: UUID, session: SessionDep):
    return delete(mission_id, session)
