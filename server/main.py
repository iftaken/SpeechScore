from unittest import result
from fastapi import FastAPI, Header, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional, List 
from sql import DataBase 
from utils import SuccessRequest, ErrorRequest, ranstr
import aiofiles
import os
import datetime
from tokens import TokenCotrol
from starlette.responses import FileResponse
import uvicorn


tokenCon = TokenCotrol()

app = FastAPI()
db = DataBase(db_path="../db/speech.sqlite",
    sql_path="../db/speech.sql")
files_dir = os.path.realpath("../files")
if not os.path.exists(files_dir):
    os.makedirs(files_dir)


class LoginInfo(BaseModel):
    username: str
    password: str

class TaskInfo(BaseModel):
    taskname: str
    leader_id: int
    desc: str

class TaskId(BaseModel):
    taskId: int
    
class ScoreWav(BaseModel):
    taskId: int
    userId: int

class FileId(BaseModel):
    fileId: int

class ScoreClient(BaseModel):
    fileId: int
    taskId: int
    userId: int
    score: float


@app.post("/user/login")
async def login(login_info: LoginInfo):
    # 登录
    # 先查 user 是否存在
    user = db.select_user_by_username(login_info.username)
    if user:
        # 检查密码是否正确
        if login_info.password == user['password']:
            token = tokenCon.addTokenWithUserId(user['id'])
            user['token'] = token
            return SuccessRequest(user,message="Login Right")
        else:
            return ErrorRequest(message="密码不正确")
    else:
        return ErrorRequest(message="用户不存在")


@app.post("/user/loginOut")
async def loginOut():
    return None



@app.post("/user/register")
async def register(register_info: LoginInfo):
    # 用户注册
    if register_info.username == "":
        return ErrorRequest(message="注册用户名不可以为空")

    user = db.select_user_by_username(register_info.username)
    if user:
        return ErrorRequest(message="用户已存在")
    else:
        db.insert_users(user_name=register_info.username, password=register_info.password)
        return SuccessRequest(message="用户注册成功")

### tasks ####
# 创建任务
@app.post("/tasks/create_tasks")
async def create_tasks(task_info: TaskInfo):
    # 新建任务
    now = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    task_filepath = os.path.join(files_dir, task_info.taskname+now)
    res = db.insert_tasks(task_name=task_info.taskname,
                    leader_id=task_info.leader_id, 
                    task_filepath=task_filepath,
                    desc=task_info.desc)
    if res:
        return SuccessRequest(result=None, message="创建任务成功")
    else:
        return SuccessRequest(result=None, message="创建任务失败")

# 获取任务列表
@app.get("/tasks/get_tasklist")
async def get_task_lists():
    # 获取Task列表
    result = db.select_tasksList()

    if not result:
        result = None
    else:
        for i in range(len(result)):
            user = db.select_user_by_id(result[i]['leader_id'])
            if user:
                result[i]['leader_name'] = db.select_user_by_id(result[i]['leader_id'])['username']
            else:
                result[i]['leader_name'] = f"未知用户: {result[i]['leader_id']}"
            
            # 计算 Mos
            result[i]['mos'] = 0
            scores = db.select_scores_by_taskid(result[i]['id'])
            if scores:
                mos = sum([score['score'] for score in scores]) / len(scores)
                result[i]['mos'] = round(mos,2)


    
    return SuccessRequest(result, message="ok")


# 上传文件
@app.post("/tasks/upload_files")
async def upload_task_files(files: List[UploadFile], task_id: int = Form(...)):
    # 上传文件
    # 上传多个音频文件

    # 先检查 task id 是否存在
    task = db.select_task_by_id(task_id=task_id)
    
    if not task:
        return ErrorRequest(message=f"task id 为 {task_id} 的任务不存在")
    
    message = ""

    task_dir = task['task_filepath']
    os.makedirs(task_dir, exist_ok=True)

    for file in files:
        out_file_path = os.path.join(task_dir, file.filename)
        if file.filename.endswith(".wav"):
            # 检查文件是否存在
            if not os.path.exists(out_file_path):
                # 存储到本地,不存在就保存
                async with aiofiles.open(out_file_path, 'wb') as out_file:
                    content = await file.read()  # async read
                    await out_file.write(content)  # async write
            # 信息存入数据库
            res = db.insert_files(task_id, file_path=out_file_path, file_name=file.filename)
            if not res:
                # 记录异常信息
                message += f"{file.filename} 存入数据库失败;"
    
    if not message:
        message = "存入数据库完成"
    
    return SuccessRequest(result = None, message=message)


# 获取文件列表
@app.post("/tasks/getScoreList")
async def getScoreList(taskId:TaskId):
    task_id = taskId.taskId
    # 通过 task_id 查询文件列表
    task_result = db.select_task_by_id(task_id=task_id)
    if not task_result:
        # 为查询到
        return ErrorRequest(message=f"未查询到 id 为 { task_id }的任务")

    file_result = db.select_files_by_taskid(task_id=task_id)
    if not file_result:
        # 文件列表为空，直接返回
        return ErrorRequest(message=f" { task_id } 号任务未上传音频文件")
    else:
        # 有文件表则返回统计结果
        # 结果包含： 各音频文件打分频次，平均MOS，
        cnt_results = []
        for file in file_result:
            cnt_res = {}
            cnt_res['mos'] = 0
            cnt_res['file_name'] = file['file_name']
            cnt_res['cnt'] = 0
            cnt_res['file_id'] = file['id']

            # 查询分数
            score_result = db.select_scores_by_fileid(file_id=file['id'])
            if score_result:
                for score in score_result:
                    cnt_res['cnt'] += 1
                    cnt_res['mos'] += score['score']
                cnt_res['mos'] = cnt_res['mos'] / cnt_res['cnt']

            cnt_results.append(cnt_res)
        return SuccessRequest(result=cnt_results, message="获取文件成功")



# 获取文件列表
@app.post("/tasks/scoreWavList")
async def getScoreList(score_wav:ScoreWav):
    task_id = score_wav.taskId
    user_id = score_wav.userId
    
    # 通过 task_id 查询文件列表
    task_result = db.select_task_by_id(task_id=task_id)
    if not task_result:
        # 为查询到
        return ErrorRequest(message=f"未查询到 id 为 { task_id }的任务")

    file_result = db.select_files_by_taskid(task_id=task_id)
    if not file_result:
        # 文件列表为空，直接返回
        return ErrorRequest(message=f" { task_id } 号任务未上传音频文件")
    else:
        # 有文件表则返回统计结果
        # 结果包含： 各音频文件打分频次，平均MOS，
        cnt_results = []
        for file in file_result:
            cnt_res = {}
            cnt_res['score'] = 0
            cnt_res['file_name'] = file['file_name']
            cnt_res['file_id'] = file['id']

            # 查询分数
            score_result = db.select_scores_by_fileid_userid(file_id=file['id'], user_id=user_id)
            if score_result:
                cnt_res['score'] = score_result['score']

            cnt_results.append(cnt_res)
        return SuccessRequest(result=cnt_results, message="获取文件成功")



@app.post("/tasks/deleteTask")
async def deleteTask(taskId:TaskId):
    task_id = taskId.taskId
    # 通过 task_id 查询文件列表
    task_result = db.select_task_by_id(task_id=task_id)
    if not task_result:
        # 为查询到
        return ErrorRequest(message=f"未查询到 id 为 { task_id }的任务")
    else:
        # 查到了
        result = db.drop_task_by_id(task_id=task_id)
        if result:            
            return SuccessRequest(message=f"删除 {task_id} 任务成功")
        else:
            return ErrorRequest(message=f"删除 { task_id } 任务失败")


@app.post("/tasks/dropFileId")    
async def dropFile(fileId:FileId):
    fileId = fileId.fileId
    # 先查
    file = db.select_file_by_fileId(fileId)
    if file:
        # 删除file
        db.drop_file_by_id(fileId)
        # 删除文件
        if os.path.exists(file['file_path']):
            os.remove(file['file_path'])
        # 删除score
        db.drop_score_by_fileid(fileId)
        
        return SuccessRequest(message=f"删除文件Id { fileId } 成功")
    else:
        return ErrorRequest(message=f"文件Id { fileId } 不存在")




# 下载音频文件
@app.get("/dowanload")
async def downloadFile(fileId:int):
    file = db.select_file_by_fileId(fileId)
    if not file:
        return None
    else:
        # 把文件传回去
        return FileResponse(file['file_path'], filename=file['file_name'])
             
# 上传打分
@app.post("/scores/postScoreList")
async def uploadScore(scores: List[ScoreClient]):
    message = ""
    for score in scores:
        if score.score > 0:
            # 现查
            score_result = db.select_scores_by_custom(file_id=score.fileId,
                user_id=score.userId)
            
            if not score_result:
                # 插入
                inser_result = db.insert_scores(
                    task_id=score.taskId,
                    file_id=score.fileId,
                    user_id=score.userId,
                    score=score.score
                    )
                if not inser_result:
                    message += f"{score.fileId} 打分失败\n"
            else:
                # 更新
                db.update_score_by_id(score_id=score_result['id'], score=score.score)
                if "分数更新成功" not in message:
                    message += "分数更新成功;"
                
        else:
            message += f"{score.fileId} 打分无效（需>0）\n"
    return SuccessRequest(result=None, message=message)

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8002)


    
    
