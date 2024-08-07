from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import inject, FromDishka

from api.v1.users.schemas import UserSchema, UserInSchema, UserUpdateSchema
from core.exceptions import ApplicationException
from api.dependencies.auth import get_auth_user
from domain.entities.users import UserEntity

from logic.services.users.base import BaseUserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserSchema])
@inject
async def read_users(
        user_service: FromDishka[BaseUserService],
        limit: int = 100,
        offset: int = 0
) -> list[UserSchema]:
    users = await user_service.get_user_list(limit=limit, offset=offset)
    return [UserSchema.from_entity(user) for user in users]


@router.post("", response_model=UserSchema)
@inject
async def create_user(
        user_in: UserInSchema,
        user_service: FromDishka[BaseUserService],
) -> UserSchema:
    try:
        user = await user_service.create_user(user_in=user_in.to_entity())
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return UserSchema.from_entity(user)


@router.patch("/{user_id}", response_model=UserSchema)
@inject
async def update_user(
        user_id: str,
        user: UserUpdateSchema,
        user_service: FromDishka[BaseUserService],
        auth_user: UserEntity = Depends(get_auth_user),
) -> UserSchema:
    try:
        updated_user = await user_service.update_user(
            user_id=user_id,
            user_in=user.to_entity(),
            auth_user_email=auth_user.email
        )
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    return UserSchema.from_entity(updated_user)
