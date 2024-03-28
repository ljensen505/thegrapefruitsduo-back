from fastapi import HTTPException, status

from app.controllers.base_controller import BaseController
from app.db.users import UserQueries
from app.models.user import User


class UserController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db: UserQueries = UserQueries()

    async def get_users(self) -> list[User]:
        data = await self.db.get_all()
        try:
            return [User(**e) for e in data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user objects: {e}",
            )

    async def get_user_by_auth0_id(self, auth0_id: str) -> User:
        if (data := await self.db.get_one_by_auth0_id(auth0_id)) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or not authorized",
            )
        try:
            return User(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user object: {e}",
            )

    async def get_user_by_id(self, id: int) -> User:
        if (data := await self.db.get_one(id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        try:
            return User(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user object: {e}",
            )
