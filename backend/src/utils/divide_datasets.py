import os
import shutil
import random

# 设置路径
dataset_path = 'datasets'  # 数据集根目录
image_path = os.path.join(dataset_path, 'images', 'train')  # 原始图片路径
label_path = os.path.join(dataset_path, 'labels', 'train')  # 原始标签路径

# 目标文件夹
split_folders = ['train', 'val', 'test']
for folder in split_folders:
    os.makedirs(os.path.join(dataset_path, 'images', folder), exist_ok=True)
    os.makedirs(os.path.join(dataset_path, 'labels', folder), exist_ok=True)

# 获取所有图片文件（确保是 .jpg 或 .png）
image_files = [f for f in os.listdir(image_path) if f.endswith(('.jpg', '.png'))]
random.shuffle(image_files)  # 打乱数据

# 设置划分比例
train_ratio, val_ratio = 0.8, 0.1  # 80% 训练, 10% 验证, 10% 测试
num_train = int(len(image_files) * train_ratio)
num_val = int(len(image_files) * val_ratio)

# 划分数据
train_files = image_files[:num_train]
val_files = image_files[num_train:num_train + num_val]
test_files = image_files[num_train + num_val:]


# 函数：移动文件
def move_files(file_list, split_type):
    for file in file_list:
        img_src = os.path.join(image_path, file)
        img_dst = os.path.join(dataset_path, 'images', split_type, file)

        label_file = file.replace('.jpg', '.txt').replace('.png', '.txt')  # 标签文件名
        label_src = os.path.join(label_path, label_file)
        label_dst = os.path.join(dataset_path, 'labels', split_type, label_file)

        # 移动图片
        shutil.move(img_src, img_dst)

        # 移动对应的标签（如果存在）
        if os.path.exists(label_src):
            shutil.move(label_src, label_dst)

# 执行文件移动
move_files(train_files, 'train')
move_files(val_files, 'val')
move_files(test_files, 'test')

print("✅ 数据划分完成！")
