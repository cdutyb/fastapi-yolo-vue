import os
import cv2
import random
from typing import List
from ultralytics.models import YOLO
from pathlib import Path


class Detector:
    def __init__(self, model_path: str = "src/core/yolo/models/yolo11n.pt"):
        """初始化 YOLO 目标检测模型"""
        self.model_path = model_path
        self.load_model()
        self.results = []

    def load_model(self):
        """加载 YOLO 模型"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"模型文件不存在: {self.model_path}")

        self.model = YOLO(model=self.model_path)

    def detect(self, image_path: List[str], conf_threshold: float = 0.25, output_dir: str = 'src/core/yolo/output/images'):
        """执行目标检测"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.results = self.model.predict(source=image_path,
                                          device="0", save=False, imgsz=640, show=False, conf=conf_threshold)
        self.save_result(output_dir)
        return output_dir

    def detect_video(self, video_path: str, conf_threshold: float = 0.25, output_dir: str = "src/core/yolo/output/videos"):
        """
        逐帧处理视频目标检测并保持原始格式。

        参数:
            video_path (str): 输入视频路径
            conf_threshold (float): 置信度阈值
            output_dir (str): 处理后的视频存放目录

        返回:
            str: 处理后视频的路径
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        video_name = Path(video_path).stem
        output_video_path = os.path.join(output_dir, f"{video_name}_detected.mp4")

        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        colors = {}

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model.predict(frame, device="0", imgsz=640, conf=conf_threshold)

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0].item()
                    class_id = int(box.cls[0].item())
                    class_name = result.names[class_id]

                    if conf >= conf_threshold:
                        if class_id not in colors:
                            colors[class_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                        color = colors[class_id]
                        label = f"{class_name} {conf:.2f}"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            out.write(frame)

        cap.release()
        out.release()

        return output_video_path

    def change_model(self, new_model_path: str):
        """切换 YOLO 模型"""
        pre_path = 'src/core/yolo/models/'
        ful_path = pre_path + new_model_path
        if not os.path.exists(ful_path):
            raise FileNotFoundError(f"模型文件不存在: {new_model_path}")

        self.model_path = ful_path
        self.load_model()

    def save_result(self, output_dir: str = 'src/core/yolo/output/images'):
        """保存检测结果为图片"""
        for i, r in enumerate(self.results):
            img_with_boxes = r.plot(labels=True, line_width=2)
            cv2.imwrite(output_dir + f'/image_{i}.jpg', img_with_boxes)


if __name__ == '__main__':
    model_path = r'E:\GitHub Desktop\fastapi-yolov11-vue\backend\src\core\yolo\models\yolo11n.pt'
    detector = Detector(model_path)
    detector.detect_video(r'E:\GitHub Desktop\fastapi-yolov11-vue\frontend\src\assets\videos\002.mp4')
