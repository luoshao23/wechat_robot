import itchat, time
from itchat.content import *
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

WHITE_LIST = {  u'@f4d1646321100155379a43c02b0621e3',
                u'@a50d0c5a5c41ab77d8344488dc55a623'}
WHITE_REMARK_LIST = { u'\u5c0f\u5a34',
                      u'Shelly2',
                      u'Shelly'
                    }

def get_response_from_robot(info, userid):

    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : 'b78d27022de543b3bb8091b22052a25f',
        'info'   : info.decode('utf8'),
        'userid' : userid,
    }

    try:
        r = requests.post(apiUrl, data=data).json()
        code = r.get('code')
        msg = []
        if code:
            if code == 100000:
                msg.append(r.get('text').encode('utf8'))
                return msg

            if code == 200000:
                msg.append(r.get('text').encode('utf8'))
                msg.append(r.get('url'))
                return msg

            if code == 302000:
                msg.append(r.get('text').encode('utf8'))
                for li in r.get('list'):
                    new = li.get('article').encode('utf8') + '\n'
                    new += li.get('detailurl')
                    msg.append(new)
                return msg

            if code == 308000:
                msg.append(r.get('text').encode('utf8'))
                for li in r.get('list'):
                    new = li.get('name').encode('utf8') + '\n'
                    new += li.get('info').encode('utf8') + '\n'
                    new += li.get('detailurl')
                    msg.append(new)
                return msg

            return msg.append(r.get('text').encode('utf8'))


    except:
        return None



@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # print msg.user.items() #340632480

    if msg.user.NickName in WHITE_REMARK_LIST or msg.user.RemarkName in WHITE_REMARK_LIST:
        pass
    else:
        text = get_response_from_robot(msg.text, msg.user.NickName)
        if text:
            for t in text:
                msg.user.send('%s' % (t))
                # print '%s' % (t)
        else:
            msg.user.send('%s' % ('Sorry...I cannot answer.'))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (
            msg.actualNickName, msg.text))

itchat.auto_login(enableCmdQR=True, hotReload=True)
itchat.run(True)