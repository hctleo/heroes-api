from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from shared.models import BaseModel
from uuid import UUID

if TYPE_CHECKING:
    from modules.hero.models import HeroModel


class MissionBase(SQLModel):
    title: str = Field(min_length=2)
    description: str = Field(nullable=False)
    hero_id: UUID | None = Field(default=None, foreign_key="hero.id")


class MissionModel(BaseModel, MissionBase, table=True):
    __tablename__ = "mission"

    hero: Optional["HeroModel"] = Relationship(back_populates="missions")
