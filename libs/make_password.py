import os
from hashlib import sha256

def make_password(password):
    '''给用户输入密码进行加密，产生一个安全密码'''
    if not isinstance(password,bytes):   #判断密码是否为字节类型
        password = str(password).encode('utf8')  #转化为以utf8编码的字符串
    hash_value = sha256(password).hexdigest()
       #用sha256对密码进行加密并转为16进制数
    salt = os.urandom(16).hex()
    #urandom产生一个长度为32个字节的字节对象，包含随机字节
    safe_password = salt + hash_value
    #拼接成一个新的安全密码
    return safe_password