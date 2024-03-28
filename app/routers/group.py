from fastapi import APIRouter, HTTPException, Security, status

from app.admin.utils import VerifyToken
from app.controllers import Controller
from app.models.group import Group

router = APIRouter(
    prefix="/group",
    tags=["group"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()
controller = Controller()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_group() -> Group:
    return await controller.get_group()


@router.patch("/")
async def update_group(group: Group, auth_result=Security(auth.verify)) -> Group | None:
    """Updates the group bio, but requires the entire group object to be sent in the request body.
    Requires authentication."""
    auth0_id: str = auth_result.get("sub")
    return await controller.update_group_bio(group.bio, auth0_id)
