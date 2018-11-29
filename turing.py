#!/user/bin/python3
#-*- coding:utf-8 -*-

import requests
import json
import passwd

def my_post(txt):
    print("Good!\n")
# post请求格式
    dic = {
        "reqType":0,
        "perception": {
            "inputText": {
                "text": txt
            },
        },
        "userInfo": {
            "apiKey": passwd.turing_apikey,
            "userId": "jcq15"
        }
    }

    response = requests.post(url='http://openapi.tuling123.com/openapi/api/v2', data=json.dumps(dic))
    # post的时候，将data字典形式的参数用json包转换成json格式。

    res_dic = json.loads(response.content.decode('utf-8'))
    print(res_dic['results'][0]['values']['text'])
    return res_dic['results'][0]['values']['text']
