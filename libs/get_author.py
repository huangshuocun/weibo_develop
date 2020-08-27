from libs.orm import db
from user.models import User
from microblog.models import Microblog
from flask import render_template,request
def get_author(self):
    aid = int(request.args.get('aid'))
    weibo = Microblog.query.get(aid)
    return render_template('read.html', weibo=weibo)