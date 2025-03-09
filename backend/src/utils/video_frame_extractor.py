import cv2
import os


def extract_frames(video_path, interval_seconds, output_dir):
    # 提取视频文件名（不带扩展名）
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频文件:", video_path)
        return

    # 获取视频帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("无法获取视频帧率")
        return

    # 计算每隔多少帧截一次图
    frame_interval = int(fps * interval_seconds)
    print(f"视频帧率: {fps:.2f}, 每 {interval_seconds} 秒截取一帧，相当于每 {frame_interval} 帧")

    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # 如果当前帧数是截图间隔的倍数，则保存该帧
        if frame_count % frame_interval == 0:
            # 拼接保存文件名，如 0.jpg
            filename = os.path.join(output_dir, f"{frame_count}.jpg")
            cv2.imwrite(filename, frame)
            print(f"保存帧 {frame_count} 到 {filename}")
            saved_count += 1
        frame_count += 1

    cap.release()
    print(f"共保存 {saved_count} 张截图")


if __name__ == "__main__":
    video_path = "video.mp4"
    interval_seconds = 3
    output_dir = "screenshots"
    extract_frames(video_path, interval_seconds, output_dir)
