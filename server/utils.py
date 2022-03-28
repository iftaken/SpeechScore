import random
import string

def ranstr(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt


def SuccessRequest(result=None, message="ok"):
    return {
        "code": 0,
        "result":result,
        "message": message
    }

def ErrorRequest(result=None, message="error"):
    return {
        "code": -1,
        "result":result,
        "message": message
    }