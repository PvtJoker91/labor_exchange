import pytest
from httpx import Response
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.v1.users.schemas import UserInSchema


@pytest.mark.asyncio
async def test_create_user(
        app: FastAPI,
        client: TestClient,
        new_user: UserInSchema
):
    url = app.url_path_for('create_user')
    response: Response = client.post(url=url, json=new_user.model_dump())

    assert response.is_success


@pytest.mark.asyncio
async def test_read_users(
        app: FastAPI,
        client: TestClient,
):
    url = app.url_path_for('read_users')
    response: Response = client.get(url=url)

    assert response.is_success


# @pytest.mark.asyncio
# async def test_update_user(
#         user_id: str,
#         user: UserUpdateSchema,
#         user_service: FromDishka[BaseUserService],
#         auth_user: UserEntity = Depends(get_auth_user),
# ) -> UserSchema:
#     try:
#         updated_user = await user_service.update_user(
#             user_id=user_id,
#             user_in=user.to_entity(),
#             auth_user_email=auth_user.email
#         )
#     except ApplicationException as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=e.message,
#         )
#
#     return UserSchema.from_entity(updated_user)
