#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
import pytz
import requests
import json

import sxtwl as sxtwl
from urllib3.exceptions import *


# 今天是我们相遇xx天
# 距离你的生日还有xx天
# 成都天气
# 温度 low ~ high
# 风   xx ~ xx
# 每日一句：xxxxxx
def getMsgHeader():
    tz = pytz.timezone('Asia/Shanghai')
    dt = datetime.now(tz)
    h = "今天是 <font color=\"info\">{}</font>".format(dt.strftime('%Y-%m-%d %A'))
    return h


def getMsgHeaderToWechat():
    tz = pytz.timezone('Asia/Shanghai')
    dt = datetime.now(tz)
    h = "今天是 <font color=\"#87CEEB\">{}</font>".format(dt.strftime('%Y-%m-%d %A'))
    return h


class Weather:
    weather = ''
    temphigh = ''
    templow = ''
    windspeed = ''

    def isValide(self) -> bool:
        if self.city != '':
            return True
        return False

    def jsonDecode(self, jsonTex):
        #
        self.weather = jsonTex['dayweather']
        self.temphigh = jsonTex['daytemp']
        self.templow = jsonTex['nighttemp']
        self.windspeed = jsonTex['daypower'].replace("-", " ~ ")

    def getWeatherTextToWechat(self):  # ， 空气质量:<font color=\"green\">{}</font>，{}。
        tex = "<hr>成都天气情况 <br> 天气: <font color=\"green\">{}</font> <br> 温度: <font color=\"green\">{}</font> ~ <font color=\"green\">{}</font> <br> 风速: <font color=\"green\">{}</font>".format(
            self.weather,
            self.templow,
            self.temphigh,
            self.windspeed
        )
        return tex


def getWeather() -> Weather:
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?key=a33b0715439a8637963d781b3e853ddd&city=510100&extensions=all'
    r = requests.get(url)
    r.encoding = 'utf-8'
    msg = r.json()

    w = Weather()
    result = r.json().get('forecasts')[0].get('casts')[0]
    # 天气封装
    w.jsonDecode(result)
    return w


def getMeetingDay():
    # 2023/11/25 00:00:00  1700841600
    unixTimeStamp = 1700841600
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)
    print("现在时间:{}".format(now))
    day = int((now.timestamp() - unixTimeStamp) / (24 * 60 * 60))
    return day


def getNextMeetDay():
    from datetime import date
    import time
    timeArray = time.strptime(str(date.today()), "%Y-%m-%d")
    # 转换成时间戳
    now_timestamp = time.mktime(timeArray)
    list2 = []
    list2.append({"2024-01-01": "元旦"})
    list2.append({"2024-02-10": '春节'})
    list2.append({"2024-02-14": '情人节'})
    list2.append({"2024-04-04": '清明节'})
    list2.append({"2024-05-01": '劳动节'})
    list2.append({"2024-06-10": '端午节'})
    list2.append({"2024-09-17": '中秋节'})
    list2.append({"2024-10-01": '国庆节'})
    list2.append({"2024-11-01": '万圣节'})
    list2.append({"2024-12-25": '圣诞节'})

    for dicts in list2:

        for key, value in dicts.items():
            # 转换成时间数组
            timeArray = time.strptime((key), "%Y-%m-%d")
            # 转换成时间戳
            timestamp = time.mktime(timeArray)
            if now_timestamp <= timestamp:
                coma = int((timestamp - now_timestamp) / (24 * 60 * 60))
                return "距离下次节日【<font color=\"#FF0000\"> {} </font>】还有<font color=\"#F5BCA9\"> {}</font> 天".format(value,
                                                                                                                  coma)
    return ""


def getBirthDayOfMa():
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)

    # 定义农历日期
    # day = sxtwl.fromLunar(2022, 1, 6)
    # 公历的年月日
    # s = "公历:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())

    dt = datetime(now.year, now.month, now.day)
    birthday = datetime(now.year, 10, 4)
    day = int((birthday.timestamp() - dt.timestamp()) / (24 * 60 * 60))
    print('生日:', day)
    return day


def getExpressLoveDay():
    # 2020-09-04 00:00:00  1599148800
    unixTimeStamp = 1599148800
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)
    day = int((now.timestamp() - unixTimeStamp) / (24 * 60 * 60))
    print(day)
    print('相爱的天:', day)
    return day


class DailyWord:
    sid = ''
    note = ''
    content = ''
    pic = ''

    def __init__(self) -> None:
        pass

    def isValide(self) -> bool:
        if self.sid != "":
            return True
        return False

    def getDailyWordHtml(self) -> str:
        return "每日一句 :<br>{}<br>{}<br><img src=\"{}\">".format(self.content, self.note, self.pic)


def getDailyWord() -> DailyWord:
    url = "http://open.iciba.com/dsapi"
    r = requests.get(url)
    r.encoding = 'utf-8'
    result = r.json()
    dw = DailyWord()
    if result.get('sid'):
        sid = result['sid']
        n = result['note']
        c = result['content']
        pic = result['fenxiang_img']
        dw.sid = sid
        dw.note = n
        dw.content = c
        dw.pic = pic
    return dw


def sendDailyWordToWechatWork(dw: DailyWord):
    if dw.isValide:
        webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxxxxxx"
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        message = {
            "msgtype": "news",
            "news": {
                "articles": [{
                    "title": "每日一句",
                    "description": dw.content,
                    "url": dw.pic,
                    "picurl": dw.pic
                }]
            }
        }
        message_json = json.dumps(message)
        info = requests.post(url=webhook, data=message_json, headers=header)
    return


# @mdTex 企业微信支持的 markdown 格式文字
def sendAlarmMsg(mdTex):
    wechatwork(mdTex)


# 企业微信推送
def wechatwork(tex):
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxxxxx"
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    message = {
        "msgtype": "markdown",
        "markdown": {
            "content": tex
        }
    }
    print(message)
    message_json = json.dumps(message)
    try:
        info = requests.post(url=webhook, data=message_json, headers=header)
    except (NewConnectionError, MaxRetryError, ConnectTimeoutError) as e:
        print("unable to connect to wechat server, err:", e)
    except Exception as e2:
        m = print("send message to wechat server, err:", e2)
        sendAlarmMsg(m)


# 微信推送
def wxPusher(tex):
    url = "http://wxpusher.zjiecode.com/api/send/message"
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    message = {
        "appToken": "AT_Sgj4zgnRC7aFHeHkVfTJsbVSOrdohnCN",
        "content": tex,
        "summary": "刘三石的星河绵绵",
        "contentType": 2,
        # "topicIds":[25530],
        "uids": ["UID_yJGK9gN7hSSO3N82sLXafTqPQo9B"
            , "UID_2s4xKdBcfWU6J56XObqvOVGKaVxt"  # RUIRUI
                 ],
        "url": "http://wxpusher.zjiecode.com"
    }
    message_json = json.dumps(message)

    try:
        info = requests.post(url=url, data=message_json, headers=header)
        print(info.text)
    except (NewConnectionError, MaxRetryError, ConnectTimeoutError) as e:
        m = print("unable to connect to wx, err:", e)
        sendAlarmMsg(m)
    except Exception as e:
        m = print("send message to wx , err:", e)
        sendAlarmMsg(m)


if __name__ == "__main__":
    # 我们已经相遇{}
    # 距离你的生日还{}天
    h1 = "Dear 芮芮"
    h2 = getMsgHeaderToWechat()
    # 节日日 约等于 见面日
    h3 = getNextMeetDay()

    m1_md = getMeetingDay()
    m2_bd = getBirthDayOfMa()
    # ed = getExpressLoveDay()
    mw = getWeather()
    m3_w2 = mw.getWeatherTextToWechat()

    dw1 = '''共享相册:<br>
        <a href="https://pm.qq.com/m/index.html">愿我如星君如月，夜夜流光相皎洁</a> <br><hr>'''
    dw = getDailyWord()
    dw2 = dw.getDailyWordHtml()
    dw3 = '''<hr><a href="https://docs.qq.com/sheet/DWHp4cUxQTldxU3Ni?u=b9ad63e5ce68440ba80112f218f1e231&tab=BB08J2">去有风的地方:</a><br>
            <img src="https://img-blog.csdnimg.cn/direct/fd95a70f176b4a56a5aa00cf8b67d290.jpeg" > '''

    # tex2 = "{}<br> 今天是我们相爱的<font color=\"#F5BCA9\"> {} </font>天<br>我们已经相遇<font color=\"#F5BCA9\"> {} </font>天<br>距离你的生日还有<font color=\"#F5BCA9\"> {} </font>天<br><br>{}<hr>{}".format(h2,ed, md, bd, w2, dw2)
    tex2 = '''{}<br> {}<br> {}<br> 今天是我们相遇的<font color=\"#F5BCA9\"> {} </font>天<br>距离你的生日还有<font color=\"#F5BCA9\"> {} </font>天<br>{}<hr>
    {}{}{}'''.format(h1, h2, h3,
                     m1_md, m2_bd, m3_w2,
                     dw1, dw2, dw3)

    print(tex2)
    wxPusher(tex2)

