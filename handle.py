# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import reply
import receive
import requests
import json
import passwd           #各种token
import time
import chrishat
import traceback
import cv2
import numpy as np
import gufeng
import newyear
from urllib import parse

class Handle(object):
    welcome = ('感谢关注！\n0.发送help2019查看2019年会发生的事\n'
               '1.直接发送消息即可调戏机器人\n'
               '2.表情包制作：回复helpmake查看\n'
               '3.古风歌词制作：发送gufeng随机生成古风歌词\n'
               '4.后台代码已经托管到GitHub，回复\"code\"查看项目\n'
               '5.公众号有很多有趣的推送，欢迎查看历史消息!\n'
               '6.您可随时回复menu查看此消息\n'
               '----------------\n'
               '商业合作请联系mail.shazi@foxmail.com')
    def POST(self):
        try:
        #if True:
            webData = web.data()
            print("Handle Post webdata is ", webData) #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                openid = recMsg.FromUserName    #用户
                me = recMsg.ToUserName          #我
                # 文本消息
                if recMsg.MsgType == 'text':
                    #如果是文本消息
                    receive_content = recMsg.Content.decode() #消息内容

                    # 文本处理
                    send_content = self.dealText(receive_content)
                    
                    print("\nreceive: ", receive_content, '\nsend: ', send_content)

                    replyMsg = reply.TextMsg(openid, me, send_content)
                    
                    return replyMsg.send()
                
                # 图片
                if recMsg.MsgType == 'image':
                    return success
                    '''
                    pic_url = recMsg.PicUrl + '.jpg'
                    response = requests.get(pic_url)
                    image = np.asarray(bytearray(response.content), dtype="uint8")  
                    img = cv2.imdecode(image, cv2.IMREAD_COLOR)

                    # 读帽子图，做
                    hat_img = cv2.imread("chris/hat.png",-1)
                    output = chrishat.add_hat(img, hat_img)
                    
                    # 存
                    timename = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    cv2.imwrite("/assets/image/"+timename+".png", output)
                    cv2.destroyAllWindows()

                    replyMsg = reply.TextMsg(openid, me, send_content)
                    return replyMsg.send()
                    '''
                
                # 事件
                if recMsg.MsgType == 'event':
                    event = recMsg.Event
                    if event == 'subscribe': #如果是关注
                        print("有人关注了！")
                        replyMsg = reply.TextMsg(openid, me, Handle.welcome)
                        return replyMsg.send()
                    return "success"

                else:
                    print("啥玩意啊")
            return "success" #微信爸爸要求回复success，否则不依不饶

        except Exception as Argment:
            print(traceback.format_exc())
            return "success"

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
            r = ('制作成功！打开后点击下面的“访问原网页”或者复制链接用浏览器打开即可！\nhttps://sorry.xuty.tk') + res
            return r
        else:
            return "API出现异常，请联系我查看情况！\nmail.shazi@foxmail.com"

    # 机器人
    def robot(self, txt):
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % txt
        response = requests.post(url=url)
        res_dic = json.loads(response.content.decode('utf-8'))
        return res_dic['content']

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
            return Handle.welcome
        #if txt == 'helphat':
        #    return '直接发送图片即可制作，但必须有人脸。做完之后点击链接，再点下面的“访问原网页”。如果打开一片空白，说明没检测到人脸。'
        if txt == 'gufeng':
            return gufeng.getSentence(10)   
        if len(txt) >= 4 and txt[0:4] == '2019':
            return newyear.makeNewYear(txt)
        if txt == 'help2019':
            return '发送“2019+你的名字”，例如“2019李华”，打开后点击下面的“访问原网页”保存即可！'
        # 不是关键词，发送到机器人
        return self.robot(txt)
