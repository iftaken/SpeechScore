FROM node:latest

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip install --upgrade pip \
    && apt-get install -y nginx \
    && apt-get install -y vim

ADD db /SpeechScore/db
ADD server /SpeechScore/server
ADD frontend /SpeechScore/frontend

RUN cd /SpeechScore/frontend \
    && npm install \
    && npm run build \
    && cd ../server \
    && pip3 install -r requirements.txt

ADD start_server.sh /SpeechScore/
ADD nginx.conf /SpeechScore/

EXPOSE 3010 8002

CMD ["sh", "/root/SpeechScore/start_server.sh"]