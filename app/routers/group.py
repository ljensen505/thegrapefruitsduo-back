from fastapi import APIRouter, HTTPException, Security, status

from app.admin import VerifyToken
from app.db import QueryException, queries
from app.models.group import Group

router = APIRouter(
    prefix="/group",
    tags=["group"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_group() -> Group:
    try:
        return queries.get_group()
    except QueryException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/")
async def update_group(group: Group, auth_result=Security(auth.verify)) -> Group | None:
    """Updates the group bio, but requires the entire group object to be sent in the request body.
    Requires authentication."""
    received_user_id = auth_result.get("sub")
    users = queries.get_users()
    user_subs = [user.auth0_id for user in users]
    if not received_user_id or received_user_id not in user_subs:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action",
        )
    queries.update_group_bio(group.bio)
    return await get_group()
