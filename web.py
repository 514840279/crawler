#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
from flask import Flask, Response, render_template, request
from common.RuleConf import *
from multiprocessing.managers import BaseManager


# 创建类似的QueueManager
class QueueManager(BaseManager):
    pass
# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字即可
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器
server_addr = '192.168.0.16' # '127.0.0.1'
print('connect to server %s...' % server_addr)
# 端口和验证码注意要保持完全一致
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
# 从网络连接
m.connect()
# 获取Queue的对象
task = m.get_task_queue()
result = m.get_result_queue()

# 引入 模块


# BASE_DIR建立一个基础路径，用于静态文件static，templates的调用
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder='templates', static_folder='static')


# 使用 蓝图 注册不同模块


# 当访问 "/"，"/index"，"/home","incex.hltml" 默认跳转到 "/index.hmtl" 模板中渲染首页
@app.route("/")
@app.route("/home")
@app.route("/index")
@app.route("/index.html")
def findhell():
    result = {'username': 'python', 'password': 'python'}
    return render_template('index.html', name=result)  # 采用模板方式解析页面


# 提供健康检查用接口
@app.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json')  # 采用json方式发送数据


# 测试接口
@app.route("/test")
def getUser():
    result = {'username': 'python', 'password': 'python'}
    return Response(json.dumps(result), mimetype='application/json')


# 测试接口
@app.route("/crawler", methods=['POST'])
def crawler():
    params = request.json
    print(params)
    if(params['delete'] == '0' or params['delete'] is None or params['delete'] =='null'):
        if params['statue'] == "1":
            # pageCrawler = PageCrawler()
            # pageCrawler.run(conf=json.loads(params['dictConf'],encoding='utf8')) # 采集字典（网站地图）
            # pageCrawler.run(conf=json.loads(params['listConf'], encoding='utf8')) # 采集列表
            # pageCrawler.run(conf=json.loads(params['detailConf'], encoding='utf8')) # 采集详细信息
            n = task.get()
            r = '%d * %d = %d' % (n, n, n * n)
            time.sleep(1)
            result.put(r)
    return Response(json.dumps(params), mimetype='application/json')


######################################
#           错误控制中心             #
######################################
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# 统一错误返回配置方法
def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    # resp = Response(content)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    resp = Response_headers(content)
    return resp
    # return "error_code:400"


@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp


# 要你命3000
app.run(port=3000, host='0.0.0.0')
