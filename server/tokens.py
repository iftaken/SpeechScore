import os
import secrets

os.path.exists

class TokenCotrol:
    def __init__(self) -> None:
        self.control = {}
        self.loop_max = 20
        self.control_inv = {}

    def checkTokenExists(self, token):
        if token in self.control:
            return True
        else:
            return False
    

    def addTokenWithUserId(self, user_id):
        token = secrets.token_hex(16)
        loop_cnt = 0
        
        while not self.checkTokenExists(token):
            token = secrets.token_hex(16)
            loop_cnt += 1
            if loop_cnt > self.loop_max:
                break
        
        self.control[token] = user_id
        return token

