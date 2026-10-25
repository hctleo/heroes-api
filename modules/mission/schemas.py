from datetime import datetime
from uuid import UUID
from .models import MissionBase, MissionModel
from sqlmodel import SQLModel, Field
from modules.hero.schemas import HeroResponse


class MissionCreate(MissionBase):
    pass


class MissionUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    hero_id: UUID | None = None


class MissionResponse(MissionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    hero: HeroResponse | None
    hero_id: UUID | None = Field(default=None, exclude=True)
