from flask import Flask,render_template,redirect
from flask_login import LoginManager,login_user,login_required,current_user
from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import  Length,DataRequired,Optional


app = Flask(__name__)

#项目中设置flask_login
#可以进行会话管理
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '234rsdf34523rwsf'

#flask_wtf表单验证定义
class LoginForm(FlaskForm):
    BPIP = StringField('KCBP IP：', validators=[DataRequired(), Length(7, 15)])
    FuncId = StringField('FuncId：', validators=[DataRequired(), Length(6, 6)])
    ReqData = StringField('ReqData：', validators=[DataRequired(), Length(1, 3200)])


#根据信息验证登录
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        bpIP = form.BPIP.data
        funcId = form.FuncId.data
        reqData = form.ReqData.data

    #return render_template('login.html',formid='loginForm',action='/login',method='post',form=form)
'''登录函数，首先实例化form对象
然后通过form对象验证post接收到的数据格式是否正确'''






if __name__ == '__main__':
    app.run()