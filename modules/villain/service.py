from .schemas import VillainResponse, VillainPowerStats
from .constants import VILLAIN_API_URL
from fastapi import HTTPException
import httpx


async def read_one(client: httpx.AsyncClient, villain_id: int) -> VillainResponse:
    url = f"{VILLAIN_API_URL}/id/{villain_id}.json"

    try:
        response = await client.get(url)
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504, detail="A API de super-heróis demorou para responder."
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502, detail="Não foi possível acessar a API de super-heróis."
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404, detail=f"Nenhum vilão encontrado com o Id {villain_id}."
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502, detail="Erro ao consultar a API de super-vilões."
        )

    data = response.json()

    return VillainResponse(
        id=data["id"],
        name=data["name"],
        full_name=data["biography"]["fullName"],
        alignment=data["biography"]["alignment"],
        publisher=data["biography"]["publisher"],
        race=data["appearance"]["race"],
        powerstats=VillainPowerStats(
            **data["powerstats"]
        ),  # ** é a descompactação do dicionário do Python. Ele transforma cada par chave/valor do dicionário em um argumento nomeado da função.
        image=data["images"]["md"],
    )
