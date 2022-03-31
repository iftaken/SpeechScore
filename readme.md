# SpeechScore

一个半匿名的本地语音打分Demo，未做相关安全验证与加密。

前端： vue3

后端: fastapi

数据库: sqlite3

## 安装

后端环境配置：

```shell
cd server
pip install -r requirements.txt
```

前端环境配置：

```
cd frontend
npm install
npm run build
```

## 运行

1. 开启后端服务

```shell
python main.py
```

2. 开启前端服务

```shell
npm run preview
```

3. 本地访问

游览器打开 : `http://localhost:3010/`

## 使用

1. 注册 `admin` 用户，拥有数据的删除权限
2. 登录后 `创建任务 `
3. `任务列表`更新后，进入`详细`中上传音频文件 (仅限于`.wav`格式)
4. 返回`任务列表`中，开始评测打分
5. 非 `admin`用户只能删除自己创建的任务

## 构建docker开启

```shell
bash build.sh
# 构建完成后
# 启动容器，后台运行
docker run -d \
  -p 3010:3010 \
  -p 8002:8002 \
  -v $PWD/db:/root/SpeechScore/db \
  -v $PWD/files:/root/SpeechScore/files \
  speech-score:v0

# 查看容器运行状态
docker ps


# 打开游览器 http://localhost:3010/
```



