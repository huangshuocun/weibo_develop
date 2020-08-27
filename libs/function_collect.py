from flask import session
from flask import redirect
from functools import wraps
import os
from hashlib import sha256
from hashlib import md5

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

def login_check(view_func):   #这是一个闭包，即装饰器，用来装饰用户登录的视图函数
    @wraps(view_func)
    def check_session(*args, **kwargs):
        uid = session.get('uid')   #从服务器的cookies里获取上次用户登录保存的uid的数值
        if not uid:   #无uid则表明用户未登录
            return redirect('/user/login')  #重定向到用户的登录界面
        else:                               #若用户已登录，则返回视图函数
            return view_func(*args, **kwargs)
    return check_session

def check_password(password, safe_password):
    '''检查密码'''
    if not isinstance(password, bytes):   #检查密码是否为字节流型，不是则转
        password = str(password).encode('utf8')  #将密码转为字符串并用utf8编码

    # 计算哈希值
    hash_value = sha256(password).hexdigest()

    #若用户密码与安全密码（第32为开始为原始密码）一致，返回True
    return hash_value == safe_password[32:]

def save_image(image_file):
    '''保存头像文件'''
    # 读取文件的二进制数据
    file_bin_data = image_file.stream.read()

    # 文件指针归零
    image_file.stream.seek(0)

    # 计算文件的 md5 值
    filename = md5(file_bin_data).hexdigest()

    # 获取项目文件夹的绝对路径
    base_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

    # 文件绝对路径
    filepath = os.path.join(base_dir, 'static', 'upload', filename)

    # 保存文件
    image_file.save(filepath)

    # 文件的 URL
    image_url = f'/static/upload/{filename}'

    return image_url