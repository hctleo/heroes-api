from typing import Annotated
from fastapi import Depends, Request
import httpx


def create_http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=5.0)


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


HttpClientDep = Annotated[httpx.AsyncClient, Depends(get_http_client)]
