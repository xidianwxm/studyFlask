#coding=utf-8

from flask import Flask, render_template, request, redirect
import sys
import logging

# python2里面默认编码为ASCII，对于中文脚本需要重新编码，否则解析出错
reload(sys)
sys.setdefaultencoding('utf-8')

# 引用logging日志模块，按照格式记录日志
logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s %(levelname)s - %(message)s' )
logger = logging.getLogger(__name__)


app = Flask(__name__,template_folder='../templates',static_url_path='/static/')
users={
    'root':"redhat",
    'westos':"123"
}

#首页,路由http：//ip:port
@app.route('/')
def headpage():
    #return render_template('headpage.html')
    return render_template('sendReq.html')


#用户登录
#通过route装饰器传递methods方法，改变http的方法
@app.route('/login',methods=['POST','GET'])
def login():
    #判断请求方法是否为post
    if request.method=='POST':
        #获取前端用户表单提交的数据
        username=request.form['name']
        passwd=request.form['passwd']

        #判断用户名和密码是否正确
        if username in users:
            #如果匹配成功就跳转到另一个页面
            if passwd==users[username]:
                return redirect("https://www.baidu.com/")
            else:
                return "用户密码不正确"
        else:
            return '用户不存在'

    #如果不是post方法，没有提交数据就调转到登录页面
    else:
        return render_template('login.html')

#用户注册
@app.route('/add',methods=['POST',"GET"])
def add():
    if request.method=="POST":
        addname=request.form['name']
        addpasswd=request.form['passwd']
        if addname in users:
            return "用户已经存在"
        else:
            users[addname]=addpasswd
            return "注册成功"
    else:
        return render_template('add.html')

#用户删除
@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method=='POST':
        delname=request.form['name']
        if delname in users:
            del users[delname]
            return "删除成功"
        else:
            return "用户不存在"

    else:
        return render_template('delete.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
