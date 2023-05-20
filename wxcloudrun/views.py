import hashlib, time, requests
import datetime
from flask import render_template, request
import xml.etree.ElementTree as ET
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid, insert_user, query_userbyid, update_userbyid
from wxcloudrun.model import Counters, User
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response, make_text_response, make_wx_text_response, make_wx_success_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/wx', methods=['POST'])
def wechat_chat():
    # 获取请求体参数
    xml_data = request.get_data(as_text=True)
    xml_tree = ET.fromstring(xml_data)
    msg_type = xml_tree.find('MsgType').text
    username = xml_tree.find("FromUserName").text
    user = query_userbyid(username)
    # 检查action参数
    if msg_type == 'text':
        if user.vip_expire_time > datetime.datetime.now():
            # 转发到聊天服务器
            requests.post("http://66.42.103.84/wx", data=xml_data)
            return make_wx_text_response(requests.text)
        else:
            return make_wx_text_response('您的会员已过期，请购买会员以继续使用服务')
    elif msg_type == 'subscribe':
        # 加入数据库       
        if user is None:
            user = User()
            user.username = username
            user.vip_expire_time = datetime.datetime.now() - datetime.timedelta(days=-1)    # 首次关注的第一天免费使用
            insert_user(user)
        return make_wx_text_response('欢迎关注千言chat，开始与我聊天吧！')
    else:
        return make_wx_text_response('暂不支持该类型消息的回复。')


@app.route('/wx', methods=['GET'])
def wechat_auth():
    token = 'Hz19910330Fz19890403'
    params = request.get_json()
    signature = params.get('signature', '')
    timestamp = params.get('timestamp', '')
    nonce = params.get('nonce', '')
    echostr = params.get('echostr', '')
    list = [token, timestamp, nonce]
    list.sort()
    s = ''.join(list).encode('utf-8')
    if (hashlib.sha1(s).hexdigest() == signature):
        return make_text_response(echostr)
    else:
        return make_text_response('Invalid Signature')

