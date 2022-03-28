import sqlite3
import os



def dict_factory(cursor, row):  
    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d 


class DataBase(object):
    def __init__(self, db_path:str, sql_path:str):
        db_path = os.path.realpath(db_path)
        sql_path = os.path.realpath(sql_path)

        print(db_path)
        print(sql_path)

        if os.path.exists(db_path):
            self.db_path = db_path
        else:
            db_path_dir = os.path.dirname(db_path)
            os.makedirs(db_path_dir, exist_ok=True)
            self.db_path = db_path
        
        if os.path.exists(sql_path):
            self.sql_path = sql_path
        else:
            raise FileExistsError(f"{sql_path} 不存在")
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()
        self.init_database()
    
    def init_database(self):
        """
        初始化数据库， 若表不存在则创建
        """
        sql = ""
        with open(self.sql_path, 'r', encoding='utf8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    sql += line
                if ");" in line:
                    self.cursor.execute(sql)
                    self.conn.commit()
                    sql = ""
    
    ###### 插入 #######
    def insert_base(self, sql, data_dict):
        self.cursor.execute(sql, data_dict)
        self.conn.commit()

    def insert_users(self, user_name:str, password:str):
        """新增用户
        Args:
            user_name (str): _description_
            password (str): _description_
        """
        sql = """
            insert into 
            users (username, password)
            values (:st_name, :st_pwd)
        """
        data_dict = {
            'st_name':user_name,
            'st_pwd':password,
        }
        self.insert_base(sql, data_dict)


    def insert_tasks(self, task_name:str, leader_id:int, task_filepath:str, desc:str):

        sql = """
            insert into 
            tasks (taskname, leader_id, task_filepath, desc)
            values (:st_name, :st_leader, :st_file, :st_desc)
        """
        
        data_dict = {
            'st_name': task_name,
            'st_leader': leader_id,
            'st_file': task_filepath,
            'st_desc': desc
        }
        try:
            self.insert_base(sql, data_dict)
        except Exception as e:
            print(e)
            return False
        
        return True

    def insert_scores(self, task_id, file_id, user_id, score):
        sql = """
            insert into 
            scores (task_id, file_id, user_id, score)
            values (:task_id, :file_id, :user_id, :score)
        """
        data_dict = {
            'task_id': task_id,
            'file_id': file_id,
            'user_id': user_id,
            'score': score
        }
        try:
            self.insert_base(sql, data_dict)
        except Exception as e:
            print(e)
            return False
        
        return True

    def insert_files(self, task_id, file_path, file_name):
        sql = """
            insert into 
            files (task_id, file_name, file_path)
            values (:task_id, :file_name, :file_path)
        """
        data_dict = {
            'task_id': task_id,
            'file_name': file_name,
            'file_path': file_path,
        }
        try:
            self.insert_base(sql, data_dict)
        except Exception as e:
            return False
        return True

    ##### 删除 #######
    def drop_user_all(self):
        # 清空 user 表
        sql = """DELETE from users"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_task_all(self):
        # 清空 tasks 表
        sql = """DELETE from tasks"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_files_all(self):
        # 清空 file 表
        sql = """DELETE from files"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_score_all(self):
        # 清空 sql 表
        sql = """DELETE from scores"""
        self.cursor.execute(sql)
        self.conn.commit()

    def drop_user_by_id(self, user_id):
        # 按照用户ID删除用户
        sql = f"""DELETE from users WHERE `id`={user_id}"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_task_by_id(self, task_id):
        # 按照 task id 删除task
        try:
            sql = f"""DELETE from tasks WHERE `id`={task_id} """
            self.cursor.execute(sql)
            self.conn.commit()
            
            # 删除对应的 files
            files = self.select_files_by_taskid(task_id)
            for file in files:
                # 删除 file
                self.drop_file_by_taskid(task_id)
                file_path = file['file_path']
                if os.path.exists(file_path):
                    os.remove(file_path)    
            # 删除对应的 scores
            self.drop_score_by_taskid(task_id)
            
            return True
        except Exception as e:
            print(e)
            return False

    def drop_file_by_id(self, file_id):
        # 按照 ID 删除 file 路径
        sql = f"""DELETE from files where `id`={file_id}"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_file_by_taskid(self, task_id):
        # 按照 taskID 删除 file
        sql = f""" DELETE from files where `task_id`={task_id} """
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_score_by_id(self, score_id):
        sql = f"""DELETE from scores where `id`={score_id}"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_score_by_fileid(self, file_id):
        sql = f"""DELETE from scores where `file_id`={file_id}"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def drop_score_by_taskid(self, task_id):
        sql = f"""DELETE from scores where `task_id`={task_id}"""
        self.cursor.execute(sql)
        self.conn.commit()
    


    ###### 查询 #######
    # user
    def select_user_by_username(self, user_name):
        # 根据 user_name 查询 user
        sql = f"""
        select * from users WHERE username = '{user_name}'
        """
        result = self.cursor.execute(sql).fetchone()
        return result

    def select_user_by_id(self, user_id):
        # 根据 ID 选择 用户
        sql = f"""
        select * from users WHERE id = {user_id}
        """
        result = self.cursor.execute(sql).fetchone()
        return result
    
    # task
    def select_taskname_by_id(self, task_id):
        # 根据 ID 选择 task name
        sql = f"""
        select taskname from tasks WHERE task_id = {task_id}
        """
        result = self.cursor.execute(sql).fetchone()
        return result

    def select_task_by_id(self, task_id):
        # 根据 ID 选择 task
        sql = f"""
        select * from tasks WHERE   `id` = {task_id}
        """
        result = self.cursor.execute(sql).fetchone()
        return result

    def select_tasksList(self):
        # 筛选 task List
        sql = f"""
        select * from tasks
        """
        result = self.cursor.execute(sql).fetchall()
        return result

    def select_files_by_taskid(self, task_id):
        # 根据 taskID 选择 文件
        sql = f"""
        SELECT * from files WHERE task_id = {task_id}
        """
        result = self.cursor.execute(sql).fetchall()
        return result

    def select_scores_by_taskid(self, task_id):
        # 根据 taskId 选择 score
        sql = f"""
        SELECT * from scores WHERE task_id = {task_id}
        """
        result = self.cursor.execute(sql).fetchall()
        return result
    
    def select_file_by_fileId(self, file_id):
        sql = f"""
        SELECT * from files WHERE `id` = {file_id}
        """
        result = self.cursor.execute(sql).fetchone()
        if not result:
            return None
        else:
            return result
    
    def select_scores_by_custom(self, file_id, user_id):
        sql = f"""
        SELECT * from scores WHERE file_id = {file_id} and user_id = {user_id}
        """
        result = self.cursor.execute(sql).fetchone()
        return result

    def select_scores_by_fileid(self, file_id):
        # 根据 fileID 选择 score信息
        sql = f"""
        SELECT * from scores WHERE file_id = {file_id}
        """
        result = self.cursor.execute(sql).fetchall()
        return result

    def select_scores_by_fileid_userid(self, file_id, user_id):
            # 根据 fileID 选择 score信息
        sql = f"""
        SELECT * from scores WHERE file_id = {file_id} and user_id = {user_id}
        """
        result = self.cursor.execute(sql).fetchone()
        return result

    ##### 更新 #######
    def update_score_by_id(self, score_id, score):
        sql = f"""
        UPDATE scores Set score = {score} WHERE `id` = {score_id}
        """
        self.cursor.execute(sql)
        self.conn.commit()
    
    def update_password_by_id(self, user_id, password):
        sql = f"""
        UPDATE users Set password = {password} WHERE `id` = {user_id}
        """
        self.cursor.execute(sql)
        self.conn.commit()

if __name__ == '__main__':
    db = DataBase(db_path="db/speech.sqlite",
     sql_path="db/speech.sql")

    # # user test
    # db.drop_user_all()
    # db.insert_users(user_name="admin", password='123456')
    # result = db.select_user_by_username(user_name="admin")
    # print(result)
    # # user clear
    # db.drop_user_all()
    # print("清空user")

    # task test
    # db.insert_tasks(task_name="fs1", leader_id='1', task_filepath="../example", desc='')
    # task_res = db.select_tasksList()
    # print(task_res)
    # task_res = db.select_task_by_id(task_id=task_res[0]['id'])
    # print(task_res)
    # db.drop_task_all()
    # sql = "DROP TABLE scores"
    # db.cursor.execute(sql)
    # db.conn.commit()


    
    


