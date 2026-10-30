from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from http_client import create_http_client

from modules.mission.routes import mission_router
from modules.hero.routes import hero_router
from modules.villain.routes import villain_router

from modules.mission.models import MissionModel
from modules.hero.models import HeroModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    async with create_http_client() as http_client:
        app.state.http_client = http_client
        yield


app = FastAPI(lifespan=lifespan, title="Hero's Missions Control")

app.include_router(hero_router)
app.include_router(mission_router)
app.include_router(villain_router)
