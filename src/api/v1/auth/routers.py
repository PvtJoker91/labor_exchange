from fastapi import APIRouter, HTTPException, status, Depends
from dishka.integrations.fastapi import inject, FromDishka

from api.v1.auth.schemas import TokenSchema, LoginSchema, RefreshTokenSchema
from core.config import settings
from core.exceptions import ApplicationException
from logic.services.auth.jwt_auth import JWTAuthService
from logic.services.users.base import BaseUserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenSchema)
@inject
async def login(
        creds: LoginSchema,
        auth_service: FromDishka[JWTAuthService],
) -> TokenSchema:
    try:
        token = await auth_service.login_user(email=creds.email, password=creds.password)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
    return TokenSchema.from_entity(token)


@router.post(
    "/refresh",
    response_model=TokenSchema,
)
@inject
async def refresh_token(
        token: RefreshTokenSchema,
        auth_service: FromDishka[JWTAuthService],
        user_service: FromDishka[BaseUserService],
) -> TokenSchema:
    try:
        payload = auth_service.get_token_payload(
            token=token.refresh_token,
            token_type=settings.auth_jwt.refresh_token_name
        )
        user = await user_service.get_user_by_email(email=payload.sub)
        access_token = auth_service.create_access_token(user=user)
        refresh_token = auth_service.create_refresh_token(user=user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=settings.auth_jwt.token_type_field_name,
    )
