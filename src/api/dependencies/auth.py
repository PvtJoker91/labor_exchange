from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer
from dishka.integrations.fastapi import inject, FromDishka
from core.config import settings
from core.exceptions import ApplicationException
from domain.entities.users import UserEntity
from logic.services.users.base import BaseUserService
from logic.services.auth.jwt_auth import JWTAuthService
from logic.utils.auth import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            try:
                decode_jwt(credentials.credentials)
            except ApplicationException as e:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")


@inject
async def get_auth_user(
        auth_service: FromDishka[JWTAuthService],
        user_service: FromDishka[BaseUserService],
        token: str = Depends(JWTBearer())
) -> UserEntity:
    try:
        payload = auth_service.get_token_payload(token, settings.auth_jwt.access_token_name)
        user = await user_service.get_user_by_email(email=payload.sub)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    return user
