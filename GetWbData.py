#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/2/26 21:56 
# @Author : 夏沐尧 
# @Site :  
# @File : GetWbData.py
# @Software: PyCharm

import json
import re

from imp import reload


import requests

from threading import Thread

headers = {
    'User-Agent': 'Mozillhttps://m.weibo.cn/u/3217179555?uid=3217179555&luicode=20000174a/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}


# 多进程注解
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper

def getData(WbId):
    f = open(WbId+'.txt', 'w',encoding='utf-8')  #首先先创建一个文件对象，打开方式为w
    for i in range(1,50):
        print("当前页数--->"+str(i))
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + WbId + '&page=' + str(i)
        response = requests.get(url, headers=headers)
        if (len(response.text) > 0):
            mjson = json.loads(response.text)
            if (len(mjson['data']) > 0):
                for mblogIndex in range(0, len(mjson['data']['cards'])):
                    if (len(mjson['data']['cards'][mblogIndex]) > 4):
                        # 用户说话
                        re_talktext = mjson['data']['cards'][mblogIndex]['mblog']['text']
                        # 这里使用个正则过滤掉了标签内容
                        dr = re.compile(r'<[^>]+>', re.S)
                        Db_talktext = dr.sub('', re_talktext)
                        Db_talktext = str(Db_talktext).replace("\"", '\'')
                        print(Db_talktext)
                        f.write(Db_talktext)
    f.closed
    return "完成"