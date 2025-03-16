# 基于FastAPI、YOLOv11和Vue的目标检测功能网页（还没开发完）
（检测识别是主要的目的，其他是附带的，比如注册登录功能，只是为了课程作业加的）
## 后端
1、安装**docker**（最好用命令行安装，否则会默认安装到C盘）。如果有英伟达显卡，确保**Nvidia**驱动和**NVIDIA Container Toolkit**安装好。镜像需要主机NVIDIA驱动兼容CUDA>=11.7，如果不支持，可以向下更改镜像。如果没有英伟达显卡，也支持cpu。\
2、启动docker\
3、在终端（根目录）输入命令
```
pip install -r backend/requirements.txt

docker pull pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime # 该镜像较大，自动拉取可能因为网络问题失败，所以直接手动拉取官方镜像，可能需要科学上网

docker-compose up -d --build # 启动后端和数据库服务

docker-compose exec backend aerich init -t src.core.database.config.TORTOISE_ORM # 初始化aerich
docker-compose exec backend aerich init-db # 初始化数据库 生成migrations/models里的文件 如果文件已存在 会报错 删除models文件夹即可
```
后端启动完成\
\
*另外，如果修改了数据库模型，需要在根目录输入命令以更新（或者删除migrations里的models并重新执行上一段命令）
```
docker-compose exec backend aerich migrate
docker-compose exec backend aerich upgrade
```
## 前端
（如果8080端口被占用会递增至8081端口）\
1、安装**Node.js**\
2、新开一个终端（根目录）输入命令
```
cd frontend
npm install
npm run serve
```
## 目标检测
默认放了yolov11n.pt，gtav_car_50k.pt，调整步骤如下：\
1、模型放在backend/src/core/yolo/models/当中\
2、修改 代码
```

```
\
YOLOv11: https://github.com/ultralytics/ultralytics \
在搜寻数据集和模型训练途中用过一些工具，保存在utils文件夹中
### 数据集
FCAV Simulation Dataset官网: https://deepblue.lib.umich.edu/data/concern/data_sets/pv63g053w#items_display \
有GTAV的10k、50k和200k数据集，类别只有car。200k数据集太大，老是下载出错，所以只下了50k的，上传到飞桨AI Studio方便下载:https://aistudio.baidu.com/datasetdetail/320051  \
\
GTAV50k数据集在utils文件夹中有相关训练数据指标。\
\
一开始自己半自动加手动标注了1002张，类别有car, motorbike, truck, bus, van, pickup, plane, bird\
数据集不大，有的类标的比较模糊，效果中等。上传到飞桨AI Studio: https://aistudio.baidu.com/datasetdetail/319974

前后端架构参考：https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/
