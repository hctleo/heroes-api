from .schemas import HeroCreate, HeroResponse, HeroUpdate, HeroPhotoResponse
from .models import HeroModel
from .constants import UPLOAD_DIR, ALLOWED, MAX_SIZE
from database import Session
from sqlmodel import select
from fastapi import HTTPException, UploadFile
from pathlib import Path
from uuid import UUID, uuid4


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


async def upload_photo(
    session: Session, hero_id: UUID, file: UploadFile
) -> HeroPhotoResponse:
    existing_hero = read_one(session, hero_id)

    if file.content_type not in ALLOWED:
        raise HTTPException(
            status_code=415, detail="Formato não suportado. Envie PNG ou JPEG."
        )

    content = await file.read()

    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=413, detail="Arquivo muito grande. Máximo de 2 MB."
        )

    name = f"{uuid4()}{ALLOWED[file.content_type]}"
    path = UPLOAD_DIR / name
    path.write_bytes(content)

    if existing_hero.photo_path:
        Path(existing_hero.photo_path).unlink(missing_ok=True)

    existing_hero.photo_path = str(path)
    session.add(existing_hero)
    session.commit()

    return HeroPhotoResponse(
        hero_id=hero_id,
        filename=file.filename,
        content_type=file.content_type,
        size=len(content),
        path=str(path),
    )


def get_photo_path(session: Session, hero_id: UUID) -> Path:
    existing_hero = read_one(session, hero_id)

    if not existing_hero.photo_path or not Path(existing_hero.photo_path).exists():
        raise HTTPException(status_code=404, detail="Herói sem foto.")

    return Path(existing_hero.photo_path)
