# 由detect.py修改而来
# 通过用官方模型detect实现半自动标注，得到标签文件后，将类别编号转换为自定义编号，再在此基础上进行修改。
import os

from ultralytics.models import YOLO

if __name__ == '__main__':
    custom_class_map = {2: 0, 3: 1, 5: 3, 7: 2, 14: 7}  #自定义类别编号映射

    model = YOLO(model='./yolo11x.pt')
    # print(model.names)
    model.predict(source='../datasets(gtav)/train3/', device='cpu', imgsz=640, project='runs/detect/', name='exp',
                  save=True, save_txt=True, classes=list(custom_class_map.keys()))  #记得修改路径
    labels_path = "runs/detect/exp/labels/"  #记得修改路径

    # 遍历所有 .txt 结果文件
    for file_name in os.listdir(labels_path):
        file_path = os.path.join(labels_path, file_name)

        # 读取原始 .txt 文件
        with open(file_path, "r") as f:
            lines = f.readlines()

        # 处理并转换类别编号
        new_lines = []
        for line in lines:
            parts = line.strip().split()  # 拆分每一行
            old_class_id = int(parts[0])  # 取原始类别编号
            if old_class_id in custom_class_map:
                new_class_id = custom_class_map[old_class_id]  # 映射到新编号
                parts[0] = str(new_class_id)  # 替换类别编号
                new_lines.append(" ".join(parts))  # 重新组合并存储

        # 覆盖写入新 .txt 文件
        with open(file_path, "w") as f:
            f.write("\n".join(new_lines))

    print("类别编号转换完成！🚀")
