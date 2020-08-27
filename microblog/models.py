from libs.orm import db
from user.models import User
class Microblog(db.Model):
    __tablename__='microblog'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,nullable=False)   #与user表里面的id对应
    content = db.Column(db.Text, nullable=False)
    issued=db.Column(db.DateTime,nullable=False)
    updated=db.Column(db.DateTime,nullable=False)

    @property
    def author(self):
        '''获取当前微博的作者'''
        user =User.query.get(self.uid)
        return user

#使用举例：weibo = Microblog()
# weibo.author.name  微博作者的姓名
#weibo.author.location  微博作者的地方