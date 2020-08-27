from hashlib import sha256

def check_password(password, safe_password):
    '''检查密码'''
    if not isinstance(password, bytes):   #检查密码是否为字节流型，不是则转
        password = str(password).encode('utf8')  #将密码转为字符串并用utf8编码

    # 计算哈希值
    hash_value = sha256(password).hexdigest()

    #若用户密码与安全密码（第32为开始为原始密码）一致，返回True
    return hash_value == safe_password[32:]