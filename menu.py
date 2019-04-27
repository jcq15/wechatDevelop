# -*- coding: UTF-8 -*-

import requests
import passwd
import json

# 这个函数以后分离出来
def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (passwd.appid, passwd.app_secret)
    response = requests.get(url)
    #print(response.content.decode('utf-8'))
    res_dic = json.loads(response.content.decode('utf-8'))
    return res_dic['access_token']

data = {
    "button":[
        {
            "name":"药春女少",
            "sub_button":[
                {
                    "type":"view",
                    "name":"更换微信号之后",
                    "url":"https://mp.weixin.qq.com/s?__biz=MzIwOTgzOTI5MQ==&mid=2247484353"
                },
            ]
        },
        {
            "type":"click",
            "name":"你是个啥",
            "key":"menu"
        },
        {
            "name":"冰开塞露",
            "sub_button":[
                {
                    "type":"view",
                    "name":"学霸谈996",
                    "url":"https://mp.weixin.qq.com/s/h3sibQFx_Lq-dZLV7vMgGw"
                },
            ]
        }
    ]
}

url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % get_access_token()

if __name__ == '__main__':
    response = requests.post(url, data=json.dumps(data))
    res_dic = json.loads(response.content.decode('utf-8'))
    print(res_dic)