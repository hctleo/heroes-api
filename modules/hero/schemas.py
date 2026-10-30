from .models import HeroBase
from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


class HeroResponse(HeroBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    photo_path: str | None = None


class HeroPhotoResponse(SQLModel):
    hero_id: UUID
    filename: str
    content_type: str
    size: int
    path: str
