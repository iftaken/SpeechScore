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

## 注意

如果运行的服务器和游览器客户端不在一台机器上，需要修改代理地址

1. 如果前端用vite进行dev开发，需要修改 `frontend/vite.config.js` 中 `target` 的值, 将其修改为服务器地址，不然会访问本地的localhost，找不到相关资源
2. 在docker中使用时，挂载了 nginx 代理，因此需要修改 `nginx.conf` 中的 `proxy_pass`, 将 `/api` 中 `proxy_pass http://0.0.0.0:8002/api` 改为 `proxy_pass http://serverIP:8002/api`, 修改完毕后再构建 docker 镜像

## 构建docker开启

```shell
bash build.sh
# 构建完成后
# 方式1： 后台运行
# 启动容器，后台运行
docker run -d \
  -p 8001:8001 \
  -p 8002:8002 \
  -v $PWD/db:/SpeechScore/db \
  -v $PWD/files:/SpeechScore/files \
  speech-score:v0

# 方式2：进入终端调试
docker run -i -t \
  --rm \
  -p 8001:8001 \
  -p 8002:8002 \
  -v $PWD/db:/SpeechScore/db \
  -v $PWD/files:/SpeechScore/files \
  speech-score:v0 /bin/bash

# 查看容器运行状态
bash /SpeechScore/start_server.sh

# 镜像导出
docker save -o SpeechScore.tar speech-score:v0

# 指定uid启动
docker run --user $(id -u) speech-score:v0

# 打开游览器 http://localhost:3010/
```

## 注意

Ubuntu中使用docker会以root的身份读写文件



