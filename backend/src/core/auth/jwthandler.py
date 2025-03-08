import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist

from src.core.schemas.token import TokenData
from src.core.schemas.users import UserOutSchema
from src.core.database.models import Users


# 从环境变量中获取密钥，用于加密和解密 JWT
SECRET_KEY = os.environ.get("SECRET_KEY")
# JWT 加密算法
ALGORITHM = "HS256"
# 访问令牌过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        # 创建 OAuth2 流模型，指定密码模式的 token URL 和范围
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        # 初始化 OAuth2 类，设置流模型、方案名称和自动错误处理
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        # 从请求的 cookie 中获取 Authorization 头
        authorization: str = request.cookies.get("Authorization")
        # 获取 Authorization 头中的认证方案和参数
        scheme, param = get_authorization_scheme_param(authorization)

        # 如果没有 Authorization 头或方案不是 bearer，则根据 auto_error 参数进行处理
        if not authorization or scheme.lower()!= "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param


# 创建一个 OAuth2PasswordBearerCookie 实例，用于从 cookie 中获取访问令牌
security = OAuth2PasswordBearerCookie(token_url="/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # 复制传入的数据，用于生成 JWT
    to_encode = data.copy()

    # 如果没有指定过期时间，则设置默认过期时间为 15 分钟
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # 更新数据中的过期时间
    to_encode.update({"exp": expire})
    # 使用密钥和算法生成 JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(security)):
    # 定义一个 HTTPException，用于在认证失败时抛出
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 解码 JWT，获取 payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 从 payload 中获取用户名
        username: str = payload.get("sub")
        # 如果用户名不存在，抛出 credentials_exception
        if username is None:
            raise credentials_exception
        # 创建一个 TokenData 实例，包含用户名
        token_data = TokenData(username=username)
    except JWTError:
        # 如果 JWT 解码失败，抛出 credentials_exception
        raise credentials_exception

    try:
        # 根据用户名从数据库中查询用户，并返回 UserOutSchema 格式的用户数据
        user = await UserOutSchema.from_queryset_single(
            Users.get(username=token_data.username)
        )
    except DoesNotExist:
        # 如果用户不存在，抛出 credentials_exception
        raise credentials_exception

    return user