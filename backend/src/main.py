import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise import Tortoise

from src.core.database.register import register_tortoise
from src.core.database.config import TORTOISE_ORM


# enable schemas to read relationship between models
Tortoise.init_models(["src.core.database.models"], "models")

"""
import 'from src.routes import users, notes' must be after 'Tortoise.init_models'
why?
https://stackoverflow.com/questions/65531387/tortoise-orm-for-python-no-returns-relations-of-entities-pyndantic-fastapi
"""
from src.routes import users, yolo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080",
                   "http://localhost:8081", "http://127.0.0.1:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建输出目录（如果不存在）
os.makedirs("src/core/yolo/output/images", exist_ok=True)
os.makedirs("src/core/yolo/output/videos", exist_ok=True)

# 将输出目录挂载为静态资源
app.mount("/static/outputs", StaticFiles(directory="src/core/yolo/output"), name="static_outputs")

app.include_router(users.router)
app.include_router(yolo.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get("/")
def home():
    return "Hello, World!"