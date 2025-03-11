# 基于FastAPI、YOLOv11和Vue的检测功能页面（检测功能开发中）
（检测是主要的目的，其他是附带的，包含注册登录功能）
## 目前存在问题：
1、登录后点击Home页，再点击click，会直接退出登录，并跳转到登录页

后端代码路径报错不要管，不影响服务端运行，是因为docker环境内路径和本地路径不匹配导致的，有能力可以自己调整。
## 后端(localhost:5000)
1、安装docker\
2、在终端（根目录）输入命令
```
docker-compose exec backend aerich init -t src.core.database.config.TORTOISE_ORM # 初始化aerich
docker-compose exec backend aerich init-db # 初始化数据库
docker-compose up -d --build # 启动后端和数据库服务
```
后端启动完成\
\
*另外，如果修改了数据库模型，需要在根目录输入命令以更新（或者删除原有migrations/models中的文件并重新执行上一段命令）
```
docker-compose exec backend aerich migrate
docker-compose exec backend aerich upgrade
```
## 前端(localhost:8080)
（如果8080端口被占用会递增至8081端口）\
1、安装Node.js\
2、新开一个终端（根目录）输入命令
```
cd frontend
npm install
npm run dev
```
前端启动完成
## YOLO
使用YOLOv11: https://github.com/ultralytics/ultralytics \
使用GTAV开源车辆检测数据集: https://deepblue.lib.umich.edu/data/concern/data_sets/pv63g053w#items_display \
要研究代码和训练的话可以去找Ultralytics，这里就只放必要的代码和模型\
另外在搜寻数据集和模型训练途中用过一些工具，保存在utils文件夹中
