from flask import Blueprint
from flask import request,render_template,session,redirect
from user.models import User
from user.models import db
#from libs.function_collect import make_password
#from libs.function_collect import check_password
from libs.save_image import save_image
from libs.function_collect import login_check
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import datetime

user_bp= Blueprint('user',__name__,url_prefix='/user')
user_bp.template_folder='./templates'

@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        user_name=request.form.get('name','').strip()
        user_phone=request.form.get('phone','').strip()
        user_password=request.form.get('password','').strip()
        user_ack_password=request.form.get('ack_password',''.strip())
        user_gender=request.form.get('gender','').strip()
        user_birthday=request.form.get('birthday','').strip()
        user_location=request.form.get('location','').strip()
        user_description=request.form.get('description','').strip()
        register_time=datetime.datetime.now()

        #判断密码非空且第一次输入与第二次输入一致,其中之一不满足则返回密码错误
        if not user_password or user_password != user_ack_password:
            return render_template('register.html',err='密码不符合要求')

        user_data=User(name=user_name,password=user_password,gender=user_gender,birthday=user_birthday,
                       phone=user_phone,location=user_location,description=user_description,register_time=register_time)
        # 保存头像
        u_image = request.files.get('user_image')
        if u_image:
           user_data.user_image=save_image(u_image)
        try:
            db.session.add(user_data)
            db.session.commit()
            return redirect('/user/login')
        except IntegrityError:   #用来追踪若插入重复的键值则会报错
            db.session.rollback()
            return render_template('register.html',err='您的昵称已被占用！')
    else:
        return render_template('register.html')

@user_bp.route('/login',methods=('POST','GET'))
def login():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        password = request.form.get('password','').strip()
        try:
            udata=User.query.filter_by(name=name).one()
        except NoResultFound:
            db.session.rollback()
            return render_template('login.html', err='该用户不存在！')
        #在服务器端记录用户登录的cookies
        if password==udata.password:
            session['uid']=udata.id
            session['username']=udata.name
            return redirect('/user/info')
        else:
            render_template('login.html',err='密码不正确！')
    else:
        return render_template('login.html')

@user_bp.route('/info')
@login_check
def info():
    uid=session['uid']
    user_data=User.query.get(uid)
    return render_template('info.html',user_data=user_data)

@user_bp.route('/logout')
def logout():
    '''退出功能'''
    session.clear()
    return redirect('/')
