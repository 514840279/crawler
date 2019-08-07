#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
from flask import Flask, Response, render_template, request
from common.RuleConf import *

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
    pageCrawler = PageCrawler()
    pageCrawler.run(conf=json.loads(params['dictConf'],encoding='utf8')) # 采集字典（网站地图）
    pageCrawler.run(conf=json.loads(params['listConf'], encoding='utf8')) # 采集列表
    pageCrawler.run(conf=json.loads(params['detailConf'], encoding='utf8')) # 采集详细信息
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
