from typing import Any

from fastapi import APIRouter, Depends, File, Security, UploadFile

from app.admin.utils import VerifyToken
from app.controllers.controller import Controller
from app.models.event import Event, NewEvent

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

controller = Controller()
auth = VerifyToken()


@router.get("/")
async def get_events() -> list[Event]:
    return await controller.get_events()


@router.get("/{id}")
async def get_event(id: int) -> Event:
    return await controller.get_event(id)


@router.post("/")
async def create_event(
    event: NewEvent = Depends(),
    auth_result=Security(auth.verify),
) -> Event | None:
    user_id: str = auth_result.get("sub")
    return await controller.create_event(event, user_id)


@router.delete("/{id}")
async def delete_event(id: int, auth_result=Security(auth.verify)) -> None:
    user_id: str = auth_result.get("sub")
    await controller.delete_event(id, user_id)
