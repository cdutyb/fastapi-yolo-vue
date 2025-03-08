from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from src.core.database.models import Users
from src.core.schemas.users import UserDatabaseSchema


# 使用 passlib 的 CryptContext 来处理密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 验证明文密码是否与哈希密码匹配
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 获取密码的哈希值
def get_password_hash(password):
    return pwd_context.hash(password)


# 根据用户名从数据库中获取用户
async def get_user(username: str):
    return await UserDatabaseSchema.from_queryset_single(Users.get(username=username))


# 验证用户的用户名和密码是否正确
async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    try:
        # 从数据库中获取用户
        db_user = await get_user(user.username)
    except DoesNotExist:
        # 如果用户不存在，抛出 HTTP 401 错误
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 验证密码是否正确
    if not verify_password(user.password, db_user.password):
        # 如果密码不正确，抛出 HTTP 401 错误
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 返回验证通过的用户
    return db_user