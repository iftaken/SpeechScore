FROM node:latest

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip install --upgrade pip \
    && cd /root \
    # && git clone https://github.com/iftaken/SpeechScore.git \
    && git clone https://gitee.com/huangyunting/SpeechScore.git \
    && cd SpeechScore/frontend \
    && npm install \
    && cd ../server \
    && pip3 install -r requirements.txt

EXPOSE 3010 8002

# ENTRYPOINT ["bash", "/root/SpeechScore/start_server.sh"]