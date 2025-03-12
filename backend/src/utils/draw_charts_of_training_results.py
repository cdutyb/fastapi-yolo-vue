# 绘制yolo训练结果的图表
import pandas as pd
import matplotlib.pyplot as plt
import os

# 读取 CSV 文件（请确保路径正确）
results = pd.read_csv('charts_50k/results_50k.csv')

# 创建保存图片的目录
output_dir = 'charts_50k'
os.makedirs(output_dir, exist_ok=True)

# 设置支持中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘制训练损失（train/box_loss, train/cls_loss, train/dfl_loss）
plt.figure(figsize=(12, 6))
plt.plot(results['epoch'], results['train/box_loss'], label='train/box_loss')
plt.plot(results['epoch'], results['train/cls_loss'], label='train/cls_loss')
plt.plot(results['epoch'], results['train/dfl_loss'], label='train/dfl_loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('训练损失变化')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'train_loss.png'))  # 保存图片
plt.close()  # 关闭当前图表

# 绘制验证损失（val/box_loss, val/cls_loss, val/dfl_loss）
plt.figure(figsize=(12, 6))
plt.plot(results['epoch'], results['val/box_loss'], label='val/box_loss')
plt.plot(results['epoch'], results['val/cls_loss'], label='val/cls_loss')
plt.plot(results['epoch'], results['val/dfl_loss'], label='val/dfl_loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('验证损失变化')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'val_loss.png'))
plt.close()

# 绘制指标曲线（metrics/precision(B), metrics/recall(B), metrics/mAP50(B), metrics/mAP50-95(B)）
plt.figure(figsize=(12, 6))
plt.plot(results['epoch'], results['metrics/precision(B)'], label='Precision (B)')
plt.plot(results['epoch'], results['metrics/recall(B)'], label='Recall (B)')
plt.plot(results['epoch'], results['metrics/mAP50(B)'], label='mAP50 (B)')
plt.plot(results['epoch'], results['metrics/mAP50-95(B)'], label='mAP50-95 (B)')
plt.xlabel('Epoch')
plt.ylabel('Metrics')
plt.title('验证指标变化')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'metrics.png'))
plt.close()

# 绘制学习率变化曲线（lr/pg0, lr/pg1, lr/pg2）
plt.figure(figsize=(12, 6))
plt.plot(results['epoch'], results['lr/pg0'], label='lr/pg0')
plt.plot(results['epoch'], results['lr/pg1'], label='lr/pg1')
plt.plot(results['epoch'], results['lr/pg2'], label='lr/pg2')
plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.title('学习率变化')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'learning_rate.png'))
plt.close()
