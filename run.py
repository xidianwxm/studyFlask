from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, session

app = Flask(__name__)

@app.before_request
def myredirect():
    if not request.path=='/':
        username = request.args.get('username')
        if not username:
            return redirect('/')
        else:
            print 'success'

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return 'Hello  World!'


@app.route('/name', methods=['POST', 'GET'])
def hello_name():
    return 'this is name\n'

@app.route('/show', methods=['POST', 'GET'])
def show():
    return 'this is show \n'


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            session['username'] = request.form['username']
            if 'newurl' in session:
                newurl = session['newurl']
                session.pop('newurl', None)
                return redirect(newurl)
            else:
                return redirect('/home')
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


@app.route('/home')
def home():
    return render_template('home.html', username=session['username'])


@app.route('/test')
def test():
    if 'username' in session:
        return render_template('test.html')
    else:
        session['newurl'] = 'test'
        return redirect(url_for('login'))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 5000)