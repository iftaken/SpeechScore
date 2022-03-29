SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

cd $SHELL_FOLDER/server

nohup python3 main.py >> ../files/server.out &

cd ../frontend

nohup npm run preview >> ../files/frontend.out &