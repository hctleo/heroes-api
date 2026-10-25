from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables

from modules.mission.routes import mission_router
from modules.hero.routes import hero_router

from modules.mission.models import MissionModel
from modules.hero.models import HeroModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Hero's Missions Control")

app.include_router(hero_router)
app.include_router(mission_router)
