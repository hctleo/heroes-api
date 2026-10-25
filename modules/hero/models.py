from typing import TYPE_CHECKING
from shared.models import BaseModel
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from modules.mission.models import MissionModel


class HeroBase(SQLModel):
    name: str = Field(min_length=2, max_length=25)
    age: int = Field(ge=18)
    secret_name: str = Field(min_length=1, max_length=25)


class HeroModel(BaseModel, HeroBase, table=True):
    __tablename__ = "hero"

    missions: list["MissionModel"] = Relationship(back_populates="hero")
