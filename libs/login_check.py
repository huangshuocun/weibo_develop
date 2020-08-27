from flask import session
from flask import redirect
from functools import wraps
def login_check(view_func):   #这是一个闭包，即装饰器，用来装饰用户登录的视图函数
    @wraps(view_func)
    def check_session(*args, **kwargs):
        uid = session.get('uid')   #从服务器的cookies里获取上次用户登录保存的uid的数值
        if not uid:   #无uid则表明用户未登录
            return redirect('/user/login')  #重定向到用户的登录界面
        else:                               #若用户已登录，则返回视图函数
            return view_func(*args, **kwargs)
    return check_session