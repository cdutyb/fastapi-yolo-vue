from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import Optional, List
import os
import shutil
from src.core.yolo.detector import Detector  # 导入你的YOLO检测类

router = APIRouter(prefix="/yolo", tags=["yolo"])

# 初始化 YOLO 目标检测器（默认模型路径）
model_path = "src/core/yolo/models/gtav_50kplus.pt"
detector = Detector(model_path)


@router.post("/detect")
async def detect_objects(
        files: List[UploadFile] = File(...),
        conf_threshold: float = Form(0.25)
):
    """图像目标检测 - 支持多个文件上传"""
    try:
        # 保存上传的文件
        save_dir = "src/core/yolo/uploads/images"
        os.makedirs(save_dir, exist_ok=True)

        file_paths = []
        for i, file in enumerate(files):  # 使用enumerate获取索引和值
            # 保存原始文件
            file_path = os.path.join(save_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_paths.append(file_path)

        # 进行目标检测
        detector.detect(file_paths, conf_threshold)

        # 返回正确的处理后图片文件名（与detector.py中保存的格式匹配）
        output_images = [f"image_{i}.jpg" for i in range(len(files))]

        return {
            "message": "检测完成",
            "output_images": output_images
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect_video")
async def detect_video(
        file: UploadFile = File(...),
        conf_threshold: float = Form(0.25)
):
    """视频目标检测 - 处理视频并返回结果视频文件名"""
    try:
        # 保存上传的视频文件
        save_dir = "src/core/yolo/uploads/videos"
        os.makedirs(save_dir, exist_ok=True)

        video_path = os.path.join(save_dir, file.filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 处理视频目标检测
        detector.detect_video(video_path, conf_threshold)

        # 从路径中提取正确的输出文件名
        video_name = os.path.splitext(file.filename)[0]
        output_video_filename = f"{video_name}_detected.mp4"

        return {
            "message": "视频检测完成",
            "output_video": output_video_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/change_model")
async def change_model_endpoint(model_path: str = Form(...)):
    """切换当前使用的YOLO模型"""
    try:
        detector.change_model(model_path)
        return {"message": f"成功切换模型至 {model_path}"}
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail=f"模型文件 {model_path} 不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/available_models")
async def get_available_models():
    """获取所有可用的YOLO模型"""
    try:
        models_dir = "src/core/yolo/models"
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        # 获取所有.pt文件（YOLO模型）
        models = [f for f in os.listdir(models_dir) if f.endswith('.pt')]

        # 获取当前正在使用的模型名称
        current_model = os.path.basename(detector.model_path) if detector.model_path else None

        return {"models": models, "current_model": current_model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")
