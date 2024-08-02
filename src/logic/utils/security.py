import datetime
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from jose import jwt

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=settings.auth_jwt.access_token_expire_minutes
    )})
    return jwt.encode(
        to_encode,
        settings.auth_jwt.jwt_secret_key,
        algorithm=settings.auth_jwt.algorithm,
    )


def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.decode(
            token,
            settings.auth_jwt.jwt_secret_key,
            algorithms=[settings.auth_jwt.algorithm])
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
