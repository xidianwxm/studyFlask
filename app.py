#-*- coding=utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, abort, session, redirect, url_for, escape, request, make_response, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return 'Index Page'

@app.route('/hello/', methods=['POST', 'GET'])
@app.route('/hello/<name>', methods=['POST', 'GET'])
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>', methods=['POST', 'GET'])
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/', methods=['POST', 'GET'])
def projects():
    return 'The project page'

@app.route('/about', methods=['POST', 'GET'])
def about():
    return 'The about page'


@app.route('/ln', methods=['POST', 'GET'])
def ln():
    abort(401)
    this_is_never_executed()

def this_is_never_executed():
    pass

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['title'] = 'gbk'
    return resp


@app.route('/getjson/', methods=['POST', 'GET'])
def getjson():
    response = make_response(jsonify({'test': 'good'}, 403))
    return response


'''
test code

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

environ = ''
with app.request_context(environ):
    assert request.method == 'POST'
'''

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
