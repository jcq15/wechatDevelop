from PIL import Image,ImageDraw,ImageFont
import random
import time

def makeNewYear(txt):
    name = txt[4:]

    sentense = [u'网购的鞋子左右脚都是反的 只得去医院\n换脚',
                u'新买的袜子有个洞 欲退货被卖家嘲笑',
                u'2019年受到的打击组成了打击乐 赢得宇\n宙冠军',
                u'立志学一门乐器 经过不懈努力学会了退\n堂鼓',
                u'废寝忘食地钻研物理 得出结论：手机只\n有在有电的情况下才能玩',
                u'经过一年的努力 终于从穷人变成了没有\n钱的人',
                u'在一起绑架案中成功击毙人质 使绑匪失\n去谈判筹码',
                u'为了减肥买了个跑步机 但是发现怎么也\n举不起来',
                u'苦练气功 成功将人气死',
                u'结束了长达20年的单身生活 开始了第21\n年的',
                u'学游泳嫌水咸 每次都要带两个馒头才肯\n下水',
                u'企图饿死肚子里的蛔虫 被动物保护协会\n谴责',
                u'相亲遇到喜欢的人被加微信 结束后对方\n发来消息：你牙上有菜',
                u'忘带U盘情急之下将C盘重命名为U盘',
                u'面试程序员岗位 因为头发太茂盛被淘汰',
                u'在期末考试中用实力告诉大家 年级有多\n少人']

    ttfont = ImageFont.truetype('华康手札体W5P.ttf',20)
    namefont = ImageFont.truetype('华康手札体W5P.ttf',30)
    im = Image.open("newyear.png")
    draw = ImageDraw.Draw(im)
    x0 = 39

    use_sentense = random.sample(sentense, 5)
    y = [225, 286, 342, 400, 455]

    draw.text((102, 48), name, fill=(0,0,0), font=namefont)

    for i in range(5):
        draw.text((x0, y[i]), '%d%s%s' % (i, '. ', use_sentense[i]), fill=(0,0,0), font=ttfont)

    timename = time.strftime("%Y%m%d%H%M%S", time.localtime())
    im.save('/assets/image/%s.png' % timename)

    return 'http://47.95.245.218:2000/%s.png' % timename

if __name__ == "__main__":
    print(makeNewYear("2019大佬"))