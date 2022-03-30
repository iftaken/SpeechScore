SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

cd $SHELL_FOLDER/server

build_dir="../files"
if [ ! -d "$build_dir" ]; then
        mkdir $build_dir
fi

nohup python3 main.py >> ../files/server.out &

# nginx -c /root/SpeechScore/files/nginx.conf
nginx -c /root/SpeechScore/nginx.conf

nginx -s reload
# nginx -s stop
# cd ../frontend

# nohup npm run preview >> ../files/frontend.out &