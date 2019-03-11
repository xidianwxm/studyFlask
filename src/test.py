#coding=utf-8

from flask import Flask, jsonify
from flask import request
import random
from flask import g
import logging
import sys
from flask_bootstrap import Bootstrap
from flask import render_template
import subprocess
import shlex
import string



# python2里面默认编码为ASCII，对于中文脚本需要重新编码，否则解析出错
reload(sys)
sys.setdefaultencoding('utf-8')

# 引用logging日志模块，按照格式记录日志
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s %(levelname)s - %(message)s' )
logger = logging.getLogger(__name__)



#模板路径： template_folder='templates'
#静态文件路径：static_url_path='/static/'
#静态文件引入别名：static_path='/xmwan'
app = Flask(__name__,template_folder='../templates',static_url_path='/static/')
#设置编码，指定json编码格式 如果为False 就不使用ascii编码，
app.config['JSON_AS_ASCII'] = False
#指定浏览器渲染的文件类型，和解码格式；
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

bootstrap = Bootstrap(app)


@app.before_request
def set_on_g_object():
    x = random.randint(0, 9)
    app.logger.debug('before request g.x is {x}'.format(x=x))
    g.x = x


@app.route("/abc")
def test():
    g.x = 1000
    return str(g.x)
#/abc路由的别名
app.add_url_rule("/index/",endpoint="test",view_func=test)


@app.after_request
def get_on_g_object(response):
    app.logger.debug('after request g.x is{g.x}'.format(g=g))
    return response


@app.route('/', methods=['GET','POST'])
def root():
    return render_template('sendReq.html')


@app.route('/sendreq', methods=['POST'])
def sendKCBPData():
    # 从request中获取表单请求的参数信息
    bpIP = request.form['BPIP']
    funcId = request.form['FuncId']
    reqData = request.form['ReqData']

    print "BPIP: %s" % (bpIP,)
    print "FuncId: %s" % (funcId,)
    print "ReqData: %s" % (reqData,)
    retDictInfo = {
        "BPIP":bpIP,
        "FuncId":funcId,
        "ReqData":reqData
    }
    #return jsonify(retDictInfo)

    # 返回3条信息
    # shellStr = r'E:/clienttest/clienttest.exe 10.187.114.76 811002 g_serverid:1,g_operid:3113703,g_operpwd:k$sdn6}Q,g_operway:4,g_funcid:811002,g_stationaddr:FA163E4910AA,custid:1300016,fundid:-1,orgid:3113,status:'
    # 返回1条信息
    # shellStr = r'E:/clienttest/clienttest.exe 10.187.114.76 410512 funcid:410512,custid:1006527,custorgid:2102,trdpwd:+0K8mU%),netaddr:13840580040,orgid:2102,operway:M,ext:0,terminalinfo:MI;UUID:8FF3BD5E-BC5F-4346-A170-32DD9BE056F5;MPN:13840580040;@GTJA|V8.22.0,fundid:10889,market:,secuid:,stkcode:,ordersno:,bankcode:6004,qryflag:0,count:5000,poststr:,'
    # 返回0条信息
    #shellStr = r'E:/clienttest/clienttest.exe 10.187.114.76 410530 funcid:410530,custid:2380907,custorgid:4211,trdpwd:+0K8mU%),netaddr:15071760818,operway:M,ext:0,orgid:4211,fundid:2414301,moneytype:0,terminalinfo:MI;UUID:F18AA9B1-E053-4F32-8820-5B0F851CCA4A;MPN:15071760818;@40GTJA|V8.22.0'
    # shellStr = "dir"
    shellStr = r'E:/clienttest/clienttest.exe' + " " + bpIP + " " + funcId + " " + reqData
    cmdList = shlex.split(shellStr)
    print "cmdList: %s" % (cmdList,)
    p = subprocess.Popen(cmdList, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # retCode == 0 成功
    # retCode = p.wait()
    # dir无法正常调用communicate
    # p.communicate(r'D:\\')
    pos = 0
    retDict = {}
    ansSetDict = {}
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.decode('gb2312').encode('utf-8')
        line = line.strip()
        if line:
            #print "%s" % (line.decode('gb2312').encode('utf-8'))
            print "%s" % (line,)
            if '#' not in line:
                print "other:Msg"
                continue
            key = line.split('#')[0]
            value = line.split('#')[1:]
            tmp = ''.join(value)
            index = 0
            innerList = []
            knnerList = []
            if key == "ReqStr":
                '''
                reqStrV = tmp.lstrip()
                print "ReqStr: %s" % (reqStrV,)
                '''
                innerList = reqData.split(',')
                if 0 == len(innerList):
                    continue
                for _i in range(0,len(innerList)):
                    #_j, _k = innerList[_i].split(':') 需要根据第一个:来区分
                    ###print "innerList[_i]: %s" % (innerList[_i],)
                    if ':' not in innerList[_i]:
                        continue
                    try:
                        tmpPos = innerList[_i].index(':')
                    except ValueError:
                        continue
                    else:
                        _j = innerList[_i][0:tmpPos]
                        _k = innerList[_i][tmpPos+1:]
                        jnnerList = [_j, _k]
                        knnerList.append(jnnerList)
                reqStrDict = dict(knnerList)
                retDict["ReqStr"] = reqStrDict
            elif key == "RetInfo":
                retInfoV = tmp.lstrip()
                print "RetInfo: %s" % (retInfoV,)
                innerList = retInfoV.split(',')
                for _i in range(0,len(innerList)):
                    try:
                        tmpPos = innerList[_i].index(':')
                    except ValueError:
                        continue
                    else:
                        _j = innerList[_i][0:tmpPos]
                        _k = innerList[_i][tmpPos+1:]
                        jnnerList = [_j, _k]
                        knnerList.append(jnnerList)
                retInfoDict = dict(knnerList)
                retDict["RetInfo"] = retInfoDict
            elif key == "RSNum":
                rsNumV = tmp.lstrip()
                print "RSNum: %s" % (rsNumV,)
                innerList = rsNumV.split(',')
                for _i in range(0,len(innerList)):
                    try:
                        tmpPos = innerList[_i].index(':')
                    except ValueError:
                        continue
                    else:
                        _j = innerList[_i][0:tmpPos]
                        _k = innerList[_i][tmpPos+1:]
                        jnnerList = [_j, _k]
                        knnerList.append(jnnerList)
                rsNumDict = dict(knnerList)
                retDict["RSNum"] = rsNumDict
            elif key[:3] == "Ans":
                ansI = int(key[3])
                ansV = tmp.lstrip()
                print "Ans%d: %s" % (ansI,ansV,)
                innerList = ansV.split(',')
                for _i in range(0,len(innerList)):
                    try:
                        tmpPos = innerList[_i].index(':')
                    except ValueError:
                        continue
                    else:
                        _j = innerList[_i][0:tmpPos]
                        _k = innerList[_i][tmpPos+1:]
                        jnnerList = [_j, _k]
                        knnerList.append(jnnerList)
                tmpDict = dict(knnerList)
                ansSetDict[ansI] = dict(tmpDict)
            else:
                print "Other: "

            retDict["Ans"] = ansSetDict
    print "retDict: %s" % (retDict,)
    return jsonify(retDict)


@app.route('/login', methods=['post'])
def login():
    name = request.form.get('name')
    # 从request中获取表单请求的参数信息
    bpIP = request.form.get('BPIP')
    funcId = request.form.get('FuncId')
    reqData = request.form.get('ReqData')
    retDictInfo = {
        "BPIP":bpIP,
        "FuncId":funcId,
        "ReqData":reqData
    }
    return render_template('hello.html')


@app.route('/hello', methods=['GET','POST'])
def hello():
    t = ['a','b','c']
    return render_template('testhtml.html',t=t)



if __name__ == '__main__':
    app.debug = True
    #修改port没用
    app.run('0.0.0.0', port=5000)
