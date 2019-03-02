#encoding:utf-8
from flask import Flask,render_template,request

app = Flask(__name__)


@app.route('/')
def index(): #一访问127.0.0.1:5000就会返回index模板中的链接”跳转到搜索页面”
    return render_template('index2.html')

@app.route('/search/')
def search():
    #arguments
    print request.args #获取所有参数
    print request.args.get('q') #或者参数为q的值
    return 'search'

@app.route('/login/',methods=['GET','POST'])  #指定访问页面的方法
def login():
    if request.method == 'GET': #如果请求方法时GET,返回login.html模板页面
        return render_template('login1.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        return 'post request:username %s, password %s' %  (username,password)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 5000)
