from .schemas import MissionCreate, MissionUpdate, MissionResponse
from .models import MissionModel
from modules.hero.models import HeroModel
from database import Session
from fastapi import HTTPException
from sqlmodel import select
from uuid import UUID


def create(data: MissionCreate, session: Session) -> MissionResponse:
    if data.hero_id:
        hero = session.get(HeroModel, data.hero_id)

        if not hero or hero.deleted_at is not None:
            raise HTTPException(
                status_code=404, detail=f"Herói não encontrado com Id {data.hero_id}."
            )

    validated_mission = MissionModel.model_validate(data)

    session.add(validated_mission)
    session.commit()
    session.refresh(validated_mission)

    return validated_mission


def read(session: Session, offset: int = 0, limit: int = 100) -> list[MissionResponse]:
    missions = session.exec(
        select(MissionModel)
        .offset(offset)
        .where(MissionModel.deleted_at.is_(None))
        .limit(limit)
    ).all()

    if not missions:
        raise HTTPException(status_code=404, detail="Nenhuma missão encontrada.")

    return missions


def read_one(mission_id: UUID, session: Session) -> MissionResponse:
    existing_mission = session.get(MissionModel, mission_id)

    if not existing_mission or existing_mission.deleted_at is not None:
        raise HTTPException(
            status_code=404, detail=f"Nenhuma missão encontrada com o Id {mission_id}."
        )

    return existing_mission


def update(mission_id: UUID, data: MissionUpdate, session: Session):
    existing_mission = session.get(MissionModel, mission_id)

    if not existing_mission or existing_mission.deleted_at is not None:
        raise HTTPException(
            status_code=404, detail=f"Nenhuma missão encontrada com o Id {mission_id}."
        )

    mission = data.model_dump(exclude_unset=True)
    existing_mission.sqlmodel_update(mission)
    session.add(existing_mission)
    session.commit()
    session.refresh(existing_mission)

    return existing_mission


def delete(mission_id: UUID, session: Session):
    existing_mission = session.get(MissionModel, mission_id)

    if not existing_mission or existing_mission.deleted_at is not None:
        raise HTTPException(
            status_code=404, detail=f"Nenhuma missão encontrada com o Id {mission_id}."
        )

    existing_mission.soft_delete()
    session.add(existing_mission)
    session.commit()
