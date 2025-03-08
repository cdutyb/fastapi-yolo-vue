from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):#确保令牌中的用户名是一个字符串
    username: Optional[str] = None


class Status(BaseModel):#用于返回状态消息
    message: str