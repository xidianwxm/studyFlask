from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return 'Hello World!'

@app.route('/name', methods=['POST', 'GET'])
def hello_name():
    return 'my name is hello\n'

@app.route('/index/', methods=['POST', 'GET'])
@app.route('/index/<name>', methods=['POST', 'GET'])
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/indexa/', methods=['POST', 'GET'])
@app.route('/indexa/<name>', methods=['POST', 'GET'])
def helloa(name=None):
    return render_template('indexa.html', name=name)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',80)