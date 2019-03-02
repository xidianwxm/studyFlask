#encoding:utf-8
from flask import Flask,render_template,request,make_response,jsonify

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

@app.route('/post/',methods=['GET','POST'])  #指定访问页面的方法
def login():
    if request.method == 'GET': #如果请求方法时GET,返回login.html模板页面
        return render_template('postdemo.html')
    else:
        funcid = request.form.get('funcid')
        reqstr = request.form.get('reqstr')
        #return 'post request:funcid %s, reqstr %s' %  (funcid,reqstr)
        response = make_response(jsonify({'funcid':funcid, 'reqstr':reqstr}), 200)
        return response

if __name__ == '__main__':

    app.run('0.0.0.0',debug=True)

