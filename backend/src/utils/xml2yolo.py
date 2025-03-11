import os
import xml.etree.ElementTree as ET

# 类别映射，根据实际情况调整
class_mapping = {"car": 0}

# 指定存放 XML 文件的文件夹路径（请修改为实际路径）
folder_path = r"D:\downloads\repro_10k_annotations\VOC2012\Annotations"

# 遍历文件夹中的所有 XML 文件
for filename in os.listdir(folder_path):
    if not filename.endswith(".xml"):
        continue  # 过滤非 XML 文件
    xml_file = os.path.join(folder_path, filename)

    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取图片尺寸
    img_width = float(root.find('size/width').text)
    img_height = float(root.find('size/height').text)

    lines = []
    # 遍历每个目标对象
    for obj in root.findall('object'):
        # 获取类别名称
        name = obj.find('name').text
        if name not in class_mapping:
            continue  # 若类别未定义，则跳过
        class_id = class_mapping[name]

        # 读取边界框坐标
        bndbox = obj.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)

        # 计算中心点、宽度和高度并归一化到 [0,1]
        x_center = ((xmin + xmax) / 2.0) / img_width
        y_center = ((ymin + ymax) / 2.0) / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        # 按 YOLO 格式保存（格式：class_index x_center y_center width height，保留6位小数）
        line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        lines.append(line)

    # 写入转换后的标注到 TXT 文件，文件名与 XML 文件同名（后缀改为 .txt）
    txt_file = xml_file.replace('.xml', '.txt')
    with open(txt_file, 'w') as f:
        f.write("\n".join(lines))

    print(f"转换完成：{txt_file}")
