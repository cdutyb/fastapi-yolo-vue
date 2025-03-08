from typing import Optional

from tortoise import Tortoise


def register_tortoise(
    app,
    config: Optional[dict] = None,
    generate_schemas: bool = False,
) -> None:
    """
    初始化并注册 Tortoise ORM 到 FastAPI 应用中。

    参数:
        app: FastAPI 应用实例。
        config (Optional[dict]): Tortoise ORM 的配置字典。如果未提供，将使用默认配置。
        generate_schemas (bool): 是否在应用启动时生成数据库模式。

    返回:
        None
    """
    @app.on_event("startup")
    async def init_orm():
        """
        在应用启动时初始化 Tortoise ORM。

        返回:
            None
        """
        await Tortoise.init(config=config)
        if generate_schemas:
            await Tortoise.generate_schemas()

    @app.on_event("shutdown")
    async def close_orm():
        """
        在应用关闭时关闭 Tortoise ORM 的连接。

        返回:
            None
        """
        await Tortoise.close_connections()
