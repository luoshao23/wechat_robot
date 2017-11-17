# coding: utf-8
import requests

apiUrl = 'http://www.tuling123.com/openapi/api'
data = {
    'key'    : 'b78d27022de543b3bb8091b22052a25f',
    'info'   : '你叫什么',
    'userid' : 'wechat-robot',
}

r = requests.post(apiUrl, data=data).json()


print r.get('text').encode('utf8')