from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.core.database.models import Users
from src.core.schemas.token import Status
from src.core.schemas.users import UserOutSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
    """
    创建一个新用户。

    参数:
        user (UserInSchema): 包含用户信息的 Pydantic 模型。

    返回:
        UserOutSchema: 创建成功的用户信息。

    异常:
        HTTPException: 如果用户名已存在，抛出 401 错误。
    """
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:
    """
    删除指定 ID 的用户。

    参数:
        user_id (int): 要删除的用户 ID。
        current_user (UserOutSchema): 当前登录的用户信息。

    返回:
        Status: 删除操作的状态信息。

    异常:
        HTTPException: 如果用户未找到或没有权限删除，抛出 404 或 403 错误。
    """
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")