from flask import Flask, request,jsonify
from ips_r import RedisClient

__all__ = ['app']
app = Flask(__name__)


redis=RedisClient()



@app.route('/')
def index():
    return '<h2>Welcome come to Proxy Pool System</h2>'
@app.route('/random/', methods=['GET'])
def get_proxy():
    num = int(request.args.get('num'))

    return jsonify(redis.random(num))
    # conn = get_conn()
    # return conn.random(num)
@app.route('/count')
def get_counts():
    return str(redis.count())


if __name__ =='__main__':
    app.run(host='127.0.0.1',port=5555,debug=True)



