from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import Optional
import os
import uuid

from src.core.yolo.detector import detector, change_model

router = APIRouter(prefix="/yolo", tags=["yolo"])

@router.post("/detect")
async def detect_objects(
    file: Optional[UploadFile] = File(None),
    image_base64: Optional[str] = Form(None),
    conf_threshold: float = Form(0.25)
):
    """图像目标检测 - 支持文件上传或base64"""
    # 处理图片并返回检测结果

@router.post("/detect_video")
async def detect_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    conf_threshold: float = Form(0.25),
    skip_frames: int = Form(0)
):
    """视频目标检测 - 处理视频并返回结果和处理后的视频URL"""
    # 处理视频并返回检测结果及视频URL

@router.post("/change_model")
async def change_model_endpoint(model_path: str = Form(...)):
    """切换当前使用的YOLO模型"""
    # 切换到指定的模型

@router.get("/available_models")
async def list_available_models():
    """获取所有可用的YOLO模型列表"""
    # 返回可用模型列表