from fastapi import APIRouter, HTTPException, status

from app.controllers import Controller
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

controller = Controller()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users() -> list[User]:
    return await controller.get_users()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: int) -> User:
    return await controller.get_user(id)
