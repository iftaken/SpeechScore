FROM node:latest

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip install --upgrade pip \
    && apt-get install -y nginx

ADD db /root/SpeechScore/db
ADD server /root/SpeechScore/server
ADD frontend /root/SpeechScore/frontend

RUN cd /root \
    && cd SpeechScore/frontend \
    && npm install \
    && npm run build \
    && cd ../server \
    && pip3 install -r requirements.txt

ADD start_server.sh /root/SpeechScore/
ADD nginx.conf /root/SpeechScore/

EXPOSE 3010 8002

CMD ["sh", "/root/SpeechScore/start_server.sh"]