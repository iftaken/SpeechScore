SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

cd $SHELL_FOLDER/server

nohup python3 main.py >> ../files/server.out &

cd ../frontend

npm run build

nohup npm run dev >> ../files/frontend.out &