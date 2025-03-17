from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from tortoise.contrib.fastapi import HTTPNotFoundError

import src.core.crud.users as crud
from src.core.auth.users import validate_user
from src.core.schemas.token import Status
from src.core.schemas.users import UserInSchema, UserOutSchema

from src.core.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


# 创建一个 FastAPI 路由对象
router = APIRouter(tags=["users"])


# 定义一个 POST 请求处理函数，用于创建新用户
@router.post("/register", response_model=UserOutSchema)
async def create_user(user: UserInSchema) -> UserOutSchema:
    """
    创建一个新用户。

    参数:
        user (UserInSchema): 包含新用户信息的 Pydantic 模型。

    返回:
        UserOutSchema: 创建成功的用户信息。
    """
    return await crud.create_user(user)


# 定义一个 POST 请求处理函数，用于用户登录
@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录。

    参数:
        user (OAuth2PasswordRequestForm): 包含用户名和密码的表单数据。

    返回:
        JSONResponse: 包含登录成功信息和访问令牌的 JSON 响应。
    """
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",# 设置 cookie 的键为 Authorizationq
        value=f"Bearer {token}",# 设置 cookie 的值为 Bearer 访问令牌
        httponly=True,# 设置 httponly 属性，防止 XSS 攻击
        max_age=1800,# 设置 cookie 的最大存活时间为 30 分钟
        expires=1800,# 设置 cookie 的过期时间为 30 分钟
        samesite="Lax",# 设置 cookie 的 SameSite 属性为 Lax，防止 CSRF 攻击
        secure=False,# 设置 secure 属性为 False，因为我们的应用是在本地运行的
    )
    return response


# 定义一个 GET 请求处理函数，用于获取当前登录用户的信息
@router.get(
    "/users/whoami", response_model=UserOutSchema, dependencies=[Depends(get_current_user)]
)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)):
    """
    获取当前登录用户的信息。

    参数:
        current_user (UserOutSchema): 当前登录用户的信息。

    返回:
        UserOutSchema: 当前登录用户的信息。
    """
    return current_user


# 定义一个 DELETE 请求处理函数，用于删除指定 ID 的用户
@router.delete(
    "/user/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    """
    删除指定 ID 的用户。

    参数:
        user_id (int): 要删除的用户 ID。
        current_user (UserOutSchema): 当前登录用户的信息。

    返回:
        Status: 删除操作的状态信息。
    """
    return await crud.delete_user(user_id, current_user)