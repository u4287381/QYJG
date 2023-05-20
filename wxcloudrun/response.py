import json, time

from flask import Response, make_response

reply = '''
        <xml>
          <ToUserName><![CDATA[{}]]></ToUserName>
          <FromUserName><![CDATA[{}]]></FromUserName>
          <CreateTime>{}</CreateTime>
          <MsgType><![CDATA[text]]></MsgType>
          <Content><![CDATA[{}]]></Content>
        </xml>
        '''

def make_succ_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def make_succ_response(data):
    data = json.dumps({'code': 0, 'data': data})
    return Response(data, mimetype='application/json')


def make_err_response(err_msg):
    data = json.dumps({'code': -1, 'errorMsg': err_msg})
    return Response(data, mimetype='application/json')

def make_text_response(text):
    return make_response(text)

def make_wx_text_response(self, xml_tree, content):    
    fromName = xml_tree.find("ToUserName").text
    toName = xml_tree.find("FromUserName").text
    if content == '':
        content = "抱歉超时"       
    return make_response(reply.format(toName, fromName, str(int(time.time())), content))

def make_wx_success_response(self):
    return make_response("success")