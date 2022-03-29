FROM node:latest

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip install --upgrade pip \
    && cd /root \
    # && git clone https://github.com/iftaken/SpeechScore.git \
    # 国内可用下面仓库
    && git clone https://gitee.com/huangyunting/SpeechScore.git \
    && cd SpeechScore/frontend \
    && npm install \
    && cd ../server \
    && pip3 install -r requirements.txt

EXPOSE 3010 8002

# 有bug, 可进入docker 手动打开
# ENTRYPOINT ["bash /root/SpeechScore/start_server.sh"]