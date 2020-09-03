#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
    FileName : startup.py
    Date : 2020/08/28 00:02:23
    Author : HuangJianYi
    Copyright : © 2020 HuangJianYi <vahx@foxmail.com>
    License : MIT, see LICENSE for more details.
'''


import logging
import random
import re
import time
from datetime import datetime

import emoji
import pandas
import pymysql
import requests
from bs4 import BeautifulSoup


def get_headers(url, use='pc'):
    pc_agents = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
    ]
    phone_agents = [
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    ]
    def referer(url): return re.search(
        r"^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)", url).group()
    if use == 'phone':  # 随机获取一个headers
        agent = random.choice(phone_agents)
    else:
        agent = random.choice(pc_agents)
    headers = {
        'User-Agent': agent,
        'Referer': referer(url),
        'DNT': "1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Encoding': 'gzip, deflate, br',
    }
    return headers


# 连接database
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='usbw',
    database='douban',
    charset='utf8mb4')
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示

topic_values = {'group': None, 'title': None, 'author': None,
                'link': None, 'time': None, 'topic_id': None}


def start(page=1):
    while True:
        print('已进入小组第' + str(page) + '页')
        url = 'https://www.douban.com/group/638298/discussion?start=' + \
            str((page - 1) * 25)  # 哈哈哈哈哈哈哈哈哈哈哈小组
        # print(url)
        data = requests.get(url, headers=get_headers(url))
        print('page:', page, 'resp:', data.ok)
        data.encoding = 'utf-8'
        soup = BeautifulSoup(data.text, 'html.parser')
        links = soup.select('.title')
        for link in links:
            _link = str(link.select('a')[0])
            if _link.find('title="', 0, len(_link)) > -1:

                topic_values['group'] = '哈哈哈哈哈哈哈哈哈哈哈小组'
                topic_values['title'] = link.select('a')[0]['title']  # 提取出话题标题
                topic_values['link'] = link.select('a')[0]['href']  # 提取出话题链接
                topic_values['topic_id'] = int(
                    re.sub(r"\D", "", topic_values['link']))
                sql = 'insert into hazu_copy2(group_name,title,link,topic_id) values("%s","%s", "%s", %s);' % (
                    topic_values['group'], topic_values['title'], topic_values['link'], topic_values['topic_id'])
                try:
                    cursor.execute(sql)
                except Exception as e:
                    # 每个页面有5个数据是重复的,每页一般会报错5次.
                    # 不适用insert ignore into的原因是会增加id主键的数字
                    print('事务处理失败', e)

                # 以字符串形式书写SQL语句R
                # 拼接并执行sql语句
                # cursor.executemany(sql, data)
                # local_var = cursor.executemany(sql, data)
                # print(local_var)
                # sql = 'insert ignore into hazu(group,title,link,topic_id) values(%s,%s,%s,%s);' %(group, title, href, num) # insert ignore 表示，如果中已经存在相同的记录，则忽略当前新数据；
                # print(sql)
                # cursor.execute(sql)
                # 以字符串形式书写SQL语句
                # 获取发帖时间
                # data = requests.get(href, headers=get_headers(href))
                # data.encoding = 'utf-8'
                # soup = BeautifulSoup(data.text, 'html.parser')
                # timesource = soup.select('.color-green')[0].text
                # _time = datetime.strptime(timesource, '%Y-%m-%d %H:%M:%S')

        conn.commit()
        page += 1
        time.sleep(5)
    # 关闭连接
    cursor.close()
    conn.close()


if __name__ == '__main__':
    start()
