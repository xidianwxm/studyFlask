from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/name')
def hello_name():
    return 'my name is hello\n'

@app.route('/index/')
@app.route('/index/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/indexa/')
@app.route('/indexa/<name>')
def helloa(name=None):
    return render_template('indexa.html', name=name)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',80)