from flask import Blueprint,request,render_template,redirect,session
from microblog.models import Microblog
from libs.orm import db
from libs.login_check import login_check
from flask import abort
import datetime
from math import ceil

weibo_bp=Blueprint(
    'weibo',
    __name__,
    url_prefix='/weibo',
    template_folder='./templates')
#微博首页
@weibo_bp.route('/index')
def index_weibo():
    page=int(request.args.get('page',1))  #从URL当中取key键-page所对应的值，若没有则返回1
    per_page=30  #设置每页显示30条
    offset=per_page*(page-1)
    #按微博发布时间由近到远进行排列-降序排，跳过offset条，显示后面的per_page条
    #比如：第1页-跳过0条，显示30条即显示1-30条；第2页-跳过前30条，显示后30条；第3页跳过前60条，显示后30条
    weibo=Microblog.query.order_by(Microblog.issued.desc()).limit(per_page).offset(offset)
    #添加一个分页功能：
    #Microblog.query.count()统计发布的微博数量，每页显示30条，得到需要使用的最大页码
    max_page=ceil(Microblog.query.count()/per_page) #最大页码
    #以下的逻辑是什么？
    if page <= 3:
        start, end = 1, 7  # 起始处的页码范围，中间相差6页
    elif page > (max_page - 3): #要显示页数小于最后3页，则显示最后7页
        start, end = max_page - 6, max_page  # 结尾处的页码范围
    else:    #page向前3页，向后3页
        start, end = (page - 3), (page + 3)

    pages = range(start, end + 1)
    return render_template('index.html', weibo=weibo, pages=pages, page=page)

#发布微博
@weibo_bp.route('/release', methods=("POST","GET"))
def release_weibo():
    if request.method=="POST":
        uid=session['uid'] #当前已登录的用户是谁，login登录模块加进去的sesion['uid']=request.form.get(id)
        content=request.form.get('content')
        now=datetime.datetime.now()
        #检查内容是否为空
        if not content:
            return render_template('release.html',err='内容不允许为空')

        #增加微博，这是第一次发布
        weibo=Microblog(uid=uid,content=content,issued=now,updated=now)
        db.session.add(weibo)
        db.session.commit()
        return redirect('/weibo/read?aid=%s' % weibo.id)
    else:
        return render_template('release.html')

#更新微博
@weibo_bp.route('/update')
def update_weibo():
    # 检查是否当前用户在修改：从服务器session中取uid即是当前用户与所发微博的uid进行比较
    # 逻辑：第一步：如何取weibo里的uid，能把session里面的uid传进去吗？不可以，同源的话还用判断是否相等吗？一定相等。
    # 怎么才能获取当前要修改的是哪条微博呢？所以在修改页面里面设置了隐藏提交的信息名叫"wid",wid的值就是weibo.id

    if request.method == 'POST':
        wid=int(request.form.get('wid',0))  #修改后提交
    else:
        wid=int(request.args.get('aid',0))  #当前修改页提交
    # 第一步：获取当前要修改id的微博
    weibo=Microblog.query.get('wid')  #获取id号即序列号为wid的微博数据
    if weibo.uid != session['uid']:
        abort(403)  #不允许修改

    if request.method == 'POST':
        content = request.form.get('content')
        now = datetime.datetime.now()
        # 检查内容是否为空
        if not content:
            return render_template('update.html', err='内容不允许为空')
        weibo.content=request.form.get('update_content')
        weibo.updated=datetime.datetime.now()
        db.session.commit()
        return redirect('/weibo/read?aid=%s' % {{ wid }})
    else:
        weibo=Microblog.query.get('wid')  #要重新获取一遍，因为weibo已经更新了
        return render_template('update.html',weibo=weibo)

#阅读微博
@weibo_bp.route('/read')
def read_weibo():
    aid=int(request.args.get('aid'))  #aid是这条已发布的微博的序列号，第几条微博
    weibo=Microblog.query.get(aid)   #取这条发布的微博的行数据
    return render_template('read.html',weibo=weibo)

#删除微博
@weibo_bp.route('/delete')
def delete_weibo():
    #不能删除别人的微博
    aid = int(request.args.get('aid'))  #aid在release当中定义，等于微博的序列号
    #检查是否是在删除自己的微博
    weibo=Microblog.query.get(aid) #从数据库中查询序列号等于aid的这条微博
    if weibo.uid == session['uid']:  #检查当前微博的作者编号uid与留存服务器的登录作者id是否一致，一致才能删除，删的是自己的
        db.session.delete(weibo)
        db.session.commit()
        return redirect('/')
    else:
        abort(403)
       # return redirect('/weibo/index')