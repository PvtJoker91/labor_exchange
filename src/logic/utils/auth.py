import datetime
import bcrypt
from jose import jwt

from core.config import settings
from logic.exceptions.auth import InvalidTokenException


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def verify_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def encode_jwt(
        payload: dict,
        secret_key: str = settings.auth_jwt.jwt_secret_key,
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: datetime.timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + datetime.timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        secret_key: str = settings.auth_jwt.jwt_secret_key,
        algorithm: str = settings.auth_jwt.algorithm,
) -> dict | None:
    try:
        decoded = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
        )
    except jwt.JWTError:
        raise InvalidTokenException
    return decoded


def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    current_token_type = payload.get(settings.auth_jwt.token_type_field_name)
    return current_token_type == token_type
