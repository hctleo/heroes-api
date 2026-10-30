from sqlmodel import SQLModel


class VillainPowerStats(SQLModel):
    intelligence: int
    strength: int
    speed: int
    durability: int
    power: int
    combat: int


class VillainResponse(SQLModel):
    id: int
    name: str
    full_name: str
    alignment: str
    race: str | None
    powerstats: VillainPowerStats
    image: str
