from abc import ABC
from dataclasses import dataclass

from domain.entities.users import UserEntity, TokenEntity
from logic.services.users.base import BaseUserService
from logic.utils.security import verify_password, create_access_token, hash_password
from logic.exceptions.users import UserNotFoundException, UserAlreadyExistsException, UpdateOtherUserException, \
    WrongCredentialsException
from infra.exceptions.base import RepositoryException
from infra.repositories.alchemy_models.users import User as UserDTO
from infra.repositories.users.base import BaseUserRepository


@dataclass
class RepositoryUserService(BaseUserService):
    repository: BaseUserRepository

    async def get_user_list(self, limit: int, offset: int) -> list[UserEntity]:
        user_list: list[UserDTO] = await self.repository.get_all(limit=limit, offset=offset)
        return [user.to_entity() for user in user_list]

    async def create_user(self, user_in: UserEntity) -> UserEntity:
        hashed_password = hash_password(user_in.password)
        user_in.hashed_password = hashed_password
        try:
            new_user: UserDTO = await self.repository.add(user_in=user_in)
        except RepositoryException:
            raise UserAlreadyExistsException(user_email=user_in.email)
        return new_user.to_entity()

    async def update_user(self, user_id: str, auth_user_email: str, user_in: UserEntity) -> UserEntity:
        try:
            old_user = await self.repository.get_by_id(user_id=user_id)
        except RepositoryException:
            raise UserNotFoundException(user_id=user_id)

        if old_user.email != auth_user_email:
            raise UpdateOtherUserException(user_email=old_user.email)

        user_in.hashed_password = old_user.hashed_password
        user_in.id = user_id

        updated_user: UserDTO = await self.repository.update(user_in=user_in)
        return updated_user.to_entity()

    async def login_user(self, email: str, password: str):
        try:
            user = await self.repository.get_by_email(email=email)
        except RepositoryException:
            raise UserNotFoundException(user_email=email)

        if not verify_password(password, user.hashed_password):
            raise WrongCredentialsException

        return TokenEntity(access_token=create_access_token({"sub": user.email}), token_type="Bearer")
