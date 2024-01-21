from fastapi import APIRouter, HTTPException, status

from app.db import QueryException, queries
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users() -> list[User]:
    try:
        return queries.get_users()
    except QueryException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: int) -> User:
    try:
        user = queries.get_user(id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
    except QueryException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
