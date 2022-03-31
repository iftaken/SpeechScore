SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

cd $SHELL_FOLDER/server

build_dir="../files"
if [ ! -d "$build_dir" ]; then
        mkdir $build_dir
fi

nginx -c /root/SpeechScore/nginx.conf

nginx -s reload

nohup python3 main.py >> ../files/server.out
