from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import Optional, List
import os
import shutil
from src.core.yolo.detector import Detector  # 导入你的YOLO检测类

router = APIRouter(prefix="/yolo", tags=["yolo"])

# 初始化 YOLO 目标检测器（默认模型路径）
model_path = "src/core/yolo/models/50kplus.pt"
detector = Detector(model_path)

@router.post("/detect")
async def detect_objects(
    files: List[UploadFile] = File(...),  # 允许上传多个文件
    conf_threshold: float = Form(0.25)
):
    """图像目标检测 - 支持多个文件上传"""
    try:
        # 保存上传的文件
        save_dir = "src/core/yolo/uploads/images"
        os.makedirs(save_dir, exist_ok=True)

        file_paths = []
        for file in files:
            file_path = os.path.join(save_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_paths.append(file_path)

        # 进行目标检测
        output_dir = detector.detect(file_paths, conf_threshold)

        return {
            "message": "检测完成",
            "input_images": [file.filename for file in files],
            "output_directory": output_dir
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect_video")
async def detect_video(
    file: UploadFile = File(...),
    conf_threshold: float = Form(0.25)
):
    """视频目标检测 - 处理视频并返回结果和处理后的视频URL"""
    try:
        # 保存上传的视频文件
        save_dir = "src/core/yolo/uploads/videos"
        os.makedirs(save_dir, exist_ok=True)

        video_path = os.path.join(save_dir, file.filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 处理视频目标检测
        output_video_path = detector.detect_video(video_path, conf_threshold)

        return {
            "message": "视频检测完成",
            "input_video": file.filename,
            "output_video": output_video_path
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
async def list_available_models():
    """获取所有可用的YOLO模型列表"""
    model_dir = "src/core/yolo/models"
    if not os.path.exists(model_dir):
        return {"models": []}

    models = [f for f in os.listdir(model_dir) if f.endswith(".pt")]
    return {"models": models}
