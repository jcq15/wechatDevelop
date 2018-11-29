# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import reply
import receive
import turing
import requests, json
import passwd           #各种token

class Handle(object):
    def POST(self):
        try:
        #if True:
            webData = web.data()
            print("Handle Post webdata is ", webData) #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                openid = recMsg.FromUserName    #用户
                me = recMsg.ToUserName          #我
                if recMsg.MsgType == 'text':
                    #如果是文本消息
                    receive_content = recMsg.Content.decode() #消息内容

                    # 关键词检验
                    send_content = self.dealText(receive_content)
                    
                    print("\nreceive: ", receive_content, '\nsend: ', send_content)

                    replyMsg = reply.TextMsg(openid, me, send_content)
                    
                    return replyMsg.send()
                
                if recMsg.MsgType == 'event':
                    event = recMsg.Event
                    if event == 'subscribe': #如果是关注
                        print("有人关注了！")
                        content = ('感谢关注！\n1.直接发送消息即可调戏机器人\n'
                                   '2.表情包制作：回复helpmake查看\n'
                                   '3.后台代码已经托管到GitHub，回复\"code\"查看项目\n'
                                   '4.公众号有很多有趣的推送，欢迎查看历史消息!\n'
                                   '5.您可随时回复menu查看此消息\n'
                                   '----------------\n'
                                   '有任何建议或者商业合作，可直接向后台发送消息，'
                                   '或者联系mail.shazi@foxmail.com')
                        replyMsg = reply.TextMsg(openid, me, content)
                        return replyMsg.send()

                else:
                    print("啥玩意啊")
            return "success" #微信爸爸要求回复success，否则不依不饶

        except Exception as Argment:
            return Argment

    # 一开始验证用
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = passwd.check_token #按照公众号-基本配置中的自定义的token填写
            list = [token, timestamp, nonce]
            list.sort()         #为啥要排序
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return echostr
        except Exception as Argument:
            return Argument

    # 表情包制作
    def makegif(self, txt):
        t = txt.split(' ')

        # value第一项是模板里几句话，第二项是API的template name
        makeDict = {
            'makewjz':(4, 'wangjingze'), 
            'makejkl':(6, 'jinkela'),
            'maketbs':(2, 'marmot'),
            'makeqgwl':(6, 'dagong'),
            'makewsyw':(9, 'sorry'),
        }
        
        try:
            tmplt = makeDict[t[0]]
        except KeyError as keyerr:
            return ('输入错误！第一行只能是：'
                    '\nmakewjz\nmakejkl\nmaketbs\nmakeqgwl\nmakewsyw\n'
                    '可是你这个皮孩子竟然输入了') + txt
        
        if len(t)-1 != tmplt[0]:
            return '不对！应该输入%d句话，但你竟然输入了%d句话，我的天呐，笨死！%s'\
                    % (tmplt[0], len(t)-1, '要不然你回复helpmake查看一下说明吧！')

        # 一会要post的东西
        postDict = dict([(str(i), t[i+1]) for i in range(tmplt[0])])

        response = requests.post(url = 'https://sorry.xuty.tk/api/%s/make' % tmplt[1],\
                                 data = json.dumps(postDict))

        if 200 == response.status_code:
            res = bytes.decode(response.content)
            r = ('制作成功！打开后点击下面的“访问原网页”或者复制链接用浏览器打开即可！\n'
                 '感谢GitHub用户xtyxtyx提供的API\n'
                 'https://sorry.xuty.tk') + res
            return r
        else:
            return "API出现异常，请联系我查看情况！\nmail.shazi@foxmail.com"

    # 处理文本，先检查是否是关键词，不是就发送到图灵
    def dealText(self, txt):
        if len(txt) >= 4 and txt[0:4] == 'make':
            return self.makegif(txt)
        if txt == 'helpmake':
            return ('表情包制作功能，格式为：\n\n'
                    'makexxx 第1句 第2句 ... 第n句\n\n'
                    '每句之间用一个半角空格分割，将xxx替换为下列表情包名字即可：\n'
                    'wjz:王境泽，4句\njkl:金坷垃，6句\ntbs:土拨鼠，2句\n'
                    'qgwl:窃格瓦拉，6句\nwsyw:为所欲为，9句\n\n'
                    '示例：\n\nmakewjz 我就是饿死 死外边 不吃你们东西 真香')
        if txt == 'code':
            return '项目地址：https://github.com/jcq15/wechatDevelop'
        if txt == 'menu':
            return ('感谢关注！\n1.直接发送消息即可调戏机器人\n'
                   '2.表情包制作：回复helpmake查看\n'
                   '3.后台代码已经托管到GitHub，回复\"code\"查看项目\n'
                   '4.公众号有很多有趣的推送，欢迎查看历史消息!\n'
                   '5.您可随时回复menu查看此消息\n'
                   '----------------\n'
                   '有任何建议或者商业合作，可直接向后台发送消息，'
                   '或者联系mail.shazi@foxmail.com')
        
        # 不是关键词，发送到图灵
        return turing.my_post(txt)
