# 基于FastAPI、YOLOv11和Vue的目标检测功能网页（还没开发完）
（检测识别是主要的目的，其他是附带的，比如注册登录功能，只是为了课程作业加的）
## 后端
1、安装docker\
2、启动docker\
3、在终端（根目录）输入命令
```
pip install -r backend/requirements.txt
docker-compose up -d --build # 启动后端和数据库服务

cd backend
aerich init -t src.core.database.config.TORTOISE_ORM # 初始化aerich
aerich init-db # 初始化数据库
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
1、安装Node.js\
2、新开一个终端（根目录）输入命令
```
cd frontend
npm install
npm run serve
```
