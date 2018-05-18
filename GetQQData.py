#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/4/15 0:56 
# @Author : 夏沐尧 
# @Site :  
# @File : GetQQData.py
# @Software: PyCharm

import json
import re


import requests

from threading import Thread


headers1 = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
}


# 多进程注解
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def getQQData(QQnum, g_qzonetoken, cookisstr):
    begin = 0
    itemDict = {}
    items = cookisstr.split(';')
    for item in items:  # 按照字符：进行划分读取
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    gtk = str(getGTK(itemDict))
    f = open(QQnum+'.txt', 'w',encoding='utf-8')  #首先先创建一个文件对象，打开方式为w
    index = 0
    while (True):
        response = requests.get('https://user.qzone.qq.com/proxy/domain/taotao.qq.com/' \
                                'cgi-bin/emotion_cgi_msglist_v6?uin=' + QQnum + '&ftype=0&' \
                                                                                'sort=0&pos=' + str(
            begin) + '&num=10&replynum=200&g_tk=' \
                                + str(gtk) + '&callback=_preloadCallback&code_version=1&' \
                                             'format=jsonp&need_private_comment=1&qzonetoken=' \
                                + str(g_qzonetoken) + '&g_tk=' + str(gtk), cookies=itemDict,
                                headers=headers1)
        print("请求的url-->" + 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/' \
                            'cgi-bin/emotion_cgi_msglist_v6?uin=' + QQnum + '&ftype=0&' \
                                                                            'sort=0&pos=' + str(
            begin) + '&num=10&replynum=200&g_tk=' \
              + str(gtk) + '&callback=_preloadCallback&code_version=1&' \
                           'format=jsonp&need_private_comment=1&qzonetoken=' \
              + str(g_qzonetoken) + '&g_tk=' + str(gtk))
        begin += 10
        responseText = response.text.split('_preloadCallback(')[1][:-2]
        print("本次请求数据code--->" + responseText)
        mjson = json.loads(responseText)
        msglist = mjson['msglist']
        try:
            for msglistIndex in range(0, len(msglist)):
                # 创建时间
                Db_createTime = '"' + str(msglist[msglistIndex]['created_time']) + '"'
                try:
                    # 转发文章说的话
                    Db_content = msglist[msglistIndex]['rt_con']['content']
                except:
                    # 用户自己发的文章说的话
                    Db_content = msglist[msglistIndex]["content"]
                Db_content = re.sub('\s', '', Db_content)
                Db_content = re.sub('e', '', Db_content)
                Db_content = re.sub('m', '', Db_content)
                Db_content = re.sub('2', '', Db_content)
                Db_content = re.sub('4', '', Db_content)
                Db_content = re.sub('3', '', Db_content)
                f.write(Db_content)
        except:
            print("没有数据或者发生异常。。。。")
            f.closed
            return "0"
            break




def getGTK(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff


if __name__ == '__main__':
    QQnum = "45185521"
    g_qzonetoken = "6fc214638dbe666ae670c983e66f995a37735b03008aec51a4b1d8f168cdd6399d118893cfc920158425"
    cookisstr = 'pgv_pvi=107282432; pt2gguin=o1989199876; RK=cjCdpaz0To; ptcz=62e6d7602e22c422fc2315433e94714079e2c221454328bef8aa6fe86876335f; zzpaneluin=; zzpanelkey=; pgv_si=s6390706176; _qpsvr_localtk=0.1783442580235033; uin=o1989199876; skey=@5VKg5MAwV; p_uin=o1989199876; pt4_token=jv06TGJV9T6ClvHOjwuvSIUR5Asvt*OuO9sr8bY5EtE_; p_skey=p9lr59fzdO5T3yqAaRdKqxemhh8jBcONTuNLpP93FOs_; rv2=80AA42BF21022D36BBA063C9662B24A4AF77D074FA82B5A640; property20=D51C23CA1C2783A4AD9441BBFC7F8254CEA88657E17230D976A8106C5CD033EA9B29E0E211A2CE25'
    getQQData(QQnum, g_qzonetoken, cookisstr)
    print("OK")
