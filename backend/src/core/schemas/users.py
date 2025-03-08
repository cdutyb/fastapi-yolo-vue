from tortoise.contrib.pydantic import pydantic_model_creator

from src.core.database.models import Users


# 创建一个名为 UserIn 的 Pydantic 模型，用于表示用户输入数据，不包括只读字段
UserInSchema = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True
)

# 创建一个名为 UserOut 的 Pydantic 模型，用于表示用户输出数据，不包括密码、创建时间和修改时间字段
UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=["password", "created_at", "modified_at"]
)

# 创建一个名为 User 的 Pydantic 模型，用于表示数据库中的用户数据，不包括创建时间和修改时间字段
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)