from libs.orm import db

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'unknow'),default='unknow')
    birthday=db.Column(db.Date,default='2000-01-01')
    phone=db.Column(db.String(15))
    location = db.Column(db.String(10), default='中国')
    user_image = db.Column(db.String(256), default='/static/img/default.png')
    description = db.Column(db.Text, default='')
    register_time = db.Column(db.DateTime, nullable=False)  # 用户注册时间

