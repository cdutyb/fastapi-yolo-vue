import cv2
import os


def extract_frames(video_path, interval_seconds, output_dir):
    """从视频中按指定时间间隔提取帧并保存为图片"""

    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        print(f"❌ 错误: 视频文件 '{video_path}' 不存在")
        return

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ 错误: 无法打开视频文件 '{video_path}'")
        return

    # 获取视频帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print("⚠️ 警告: 无法获取视频帧率，默认使用 30 FPS")
        fps = 30  # 默认帧率

    # 计算每隔多少帧截一次图
    frame_interval = max(1, int(fps * interval_seconds))  # 确保 frame_interval 至少为 1
    print(f"📹 视频帧率: {fps:.2f}, 每 {interval_seconds} 秒截取一帧（每 {frame_interval} 帧）")

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✅ 视频读取完毕")
            break

        # 按指定间隔保存帧
        if frame_count % frame_interval == 0:
            filename = os.path.join(output_dir, f"{saved_count}.jpg")
            success = cv2.imwrite(filename, frame)
            if success:
                print(f"✅ 保存帧 {frame_count} -> {filename}")
                saved_count += 1
            else:
                print(f"❌ 错误: 无法保存帧 {frame_count}")

        frame_count += 1

    cap.release()
    print(f"🎉 完成: 共保存 {saved_count} 张截图")


if __name__ == "__main__":
    video_path = "E:/project_pycharm/AI/video.mp4"  # 视频文件路径
    interval_seconds = 3  # 每 3 秒截取一帧
    output_dir = "E:/datasets/train"  # 输出目录

    extract_frames(video_path, interval_seconds, output_dir)
