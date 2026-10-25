from .schemas import HeroCreate, HeroResponse, HeroUpdate
from .models import HeroModel
from database import Session
from sqlmodel import select
from fastapi import HTTPException
from uuid import UUID


def create(data: HeroCreate, session: Session) -> HeroResponse:
    validated_hero_data = HeroModel.model_validate(data)

    session.add(validated_hero_data)
    session.commit()
    session.refresh(validated_hero_data)

    return validated_hero_data


def read(session: Session, offset: int, limit: int) -> list[HeroResponse]:
    heroes = session.exec(
        select(HeroModel)
        .offset(offset)
        .where(HeroModel.deleted_at.is_(None))
        .limit(limit)
    ).all()

    if not heroes:
        raise HTTPException(status_code=404, detail="Nenhum herói encontrado.")

    return heroes


def read_one(session: Session, hero_id: UUID) -> HeroResponse:
    existing_hero = session.get(HeroModel, hero_id)

    if not existing_hero or existing_hero.deleted_at is not None:
        raise HTTPException(
            status_code=404, detail=f"Nenhum herói encontrado com o Id {hero_id}."
        )

    return existing_hero


def update(session: Session, hero_id: UUID, data: HeroUpdate) -> HeroResponse:
    existing_hero = session.get(HeroModel, hero_id)

    if not existing_hero or existing_hero.deleted_at is not None:
        raise HTTPException(
            status_code=404, detail=f"Nenhum herói encontrado com o Id {hero_id}."
        )

    hero = data.model_dump(exclude_unset=True)
    existing_hero.sqlmodel_update(hero)

    session.add(existing_hero)
    session.commit()
    session.refresh(existing_hero)

    return existing_hero


def delete(session: Session, hero_id: UUID):
    existing_hero = session.get(HeroModel, hero_id)

    if not existing_hero or existing_hero.deleted_at is not None:
        raise HTTPException(
            status_code=404, detail=f"Nenhum herói encontrado com o Id {hero_id}."
        )

    existing_hero.soft_delete()
    session.add(existing_hero)
    session.commit()
