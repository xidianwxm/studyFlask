# coding:utf-8

import math
import redis
from flask import Flask, request
from flask.json import jsonify
from flask.views import MethodView


app = Flask(__name__)

class PiCache(object):
    def __init__(self, client):
        self.client = client

    def set(self, n, result):
        self.client.hset("pis", str(n), str(result))

    def get(self, n):
        result = self.client.hget("pis", str(n))
        if not result:
            return
        return float(result)




class PiAPI(MethodView):
    def __init__(self, cache):
        self.cache = cache

    def get(self, n):
        result = self.cache.get(n)
        if result:
            return jsonify({"cached": True, "result": result})
        else:
            s = 0.0
            for i in xrange(1, n):
                s += 1.0/i/i
            result = math.sqrt(6*s)
            self.cache.set(n, result)
            return jsonify({"cached": False, "result": result})


client = redis.StrictRedis()
cache = PiCache(client)

# as_view提供了参数可以直接注入到MethodView的构造器中
# 我们不再使用request.args，而是将参数直接放进URL里面，这就是RESTFUL风格的URL
app.add_url_rule('/pi/<int:n>', view_func=PiAPI.as_view('pi', cache))

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 5000)
