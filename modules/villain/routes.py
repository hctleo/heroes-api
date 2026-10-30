from fastapi import APIRouter
from http_client import HttpClientDep
from .schemas import VillainResponse
from .service import read_one

villain_router = APIRouter(prefix="/villain", tags=["Villain"])


@villain_router.get("/{villain_id}", tags=["Villain"], response_model=VillainResponse)
async def read_one_villain(client: HttpClientDep, villain_id: int) -> VillainResponse:
    return await read_one(client, villain_id)
