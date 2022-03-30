FROM node:latest

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip install --upgrade pip \
    && apt-get install -y nginx

ADD nginx.conf /root/SpeechScore/
ADD db /root/SpeechScore/db
ADD server /root/SpeechScore/server
ADD frontend /root/SpeechScore/frontend
ADD start_server.sh /root/SpeechScore/

RUN cd /root \
    && cd SpeechScore/frontend \
    && npm install \
    && npm run build \
    && cd ../server \
    && pip3 install -r requirements.txt

EXPOSE 3010 8002

# 
# 有bug, 可进入docker 手动打开
CMD ["bash", "/root/SpeechScore/start_server.sh"]
# ENTRYPOINT ["bash /root/SpeechScore/start_server.sh"]