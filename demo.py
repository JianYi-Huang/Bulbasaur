#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import time
import emoji
import random
import pandas
import pymysql
import logging
import requests
from datetime import datetime
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
    referer = lambda url: re.search(
        "^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)", url).group()
    if use == 'phone': # 随机获取一个headers
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

logging.FileHandler(filename='豆瓣哈组标题和链接.log', encoding='utf-8')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S',
                    filename='C:\\Users\\Administrator\\Desktop\\豆瓣哈组标题和链接.log', # 日志保存路径
                    filemode='w')

topic_titles = []
topic_author = []
topic_links = []
topic_times = []

def get(start_page=1, end_page=1):
    logging.info('[get] 已进入小组首页')
    while start_page <= end_page:
        logging.info('[get] 已进入小组第' + str(start_page) + '页')
        print('[get] 已进入小组第' + str(start_page) + '页')
        url = 'https://www.douban.com/group/638298/discussion?start=' + str((start_page - 1) * 25) # 哈哈哈哈哈哈哈哈哈哈哈小组
        # print(url)
        data = requests.get(url, headers=get_headers(url))
        print('resp:', data.ok)
        data.encoding = 'utf-8'
        soup = BeautifulSoup(data.text, 'html.parser')
        links = soup.select('.title')
        for link in links:
            _link = str(link.select('a')[0])
            if _link.find('title="', 0, len(_link)) > -1:
                title = link.select('a')[0]['title'] # 提取出话题标题
                href = link.select('a')[0]['href'] # 提取出话题链接
                num = int(re.sub("\D", "", href))
                print(num)
                topic_titles.append(title) # 把刚获取到的标题插进话题标题表
                topic_links.append(href) # 把刚获取到的链接插进话题链接表
                print(topic_titles)
                print(topic_links)
                # 获取发帖时间
                # data = requests.get(href, headers=get_headers(href))
                # data.encoding = 'utf-8'
                # soup = BeautifulSoup(data.text, 'html.parser')
                # timesource = soup.select('.color-green')[0].text
                # _time = datetime.strptime(timesource, '%Y-%m-%d %H:%M:%S')
                
                print('标题:', title, '链接:', href)
                # logging.info('[info] 发帖时间:' + timesource + '    标题:' + emoji.demojize(title) + '   链接:' + str(href))
        start_page += 1
        time.sleep(5)

def seve_excel():
    # df_1 = pandas.DataFrame.from_dict({'发帖时间' : pandas.Categorical(topic_times),
    #                 '作者' : pandas.Categorical(topic_author),
    #                 '标题' : pandas.Categorical(topic_titles),
    #                 '链接' : pandas.Categorical(topic_links),
    #                 }, orient='index')
    df_1 = pandas.DataFrame({'标题' : pandas.Categorical(topic_titles),
                '链接' : pandas.Categorical(topic_links),
                })
    print(df_1)
    df_1.to_excel('豆瓣哈组数据.xlsx')



def mysql_test():
    # 导入pymysql模块
    import pymysql
    # 连接database
    conn = pymysql.connect(
        host = '127.0.0.1',
        user = 'root', 
        password = 'usbw',
        database = 'douban',
        charset = 'utf8mb4')
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
    # 定义要执行的sql语句
    print(type(cursor))

    sql = 'insert into test(link,title) values(%s,%s);'
    data = [
        ('https://www.123.com', '123'), 
    ]
    # 以字符串形式书写SQL语句

    # 拼接并执行sql语句
    # cursor.executemany(sql, data)

    try:
        cursor.executemany(sql, data)
    except Exception as e:
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
    else:
        # 涉及写操作要注意提交
        conn.commit()  # 事务提交
        print('事务处理成功', cursor.rowcount)

    # 更新
    # sql = 'update test set title="2222", author="小贱" where link="01";'
    # 拼接并执行sql语句
    # cursor.execute(sql)


    # insert ignore into table_name(email,phone,user_id) values('test9@163.com','99999','9999'); # insert ignore 表示，如果中已经存在相同的记录，则忽略当前新数据；
    # insert replace into table_name(email,phone,user_id) values('test9@163.com','99999','9999'); # insert replace 表示，如果中已经存在相同的记录，则忽略当前新数据；
    
    sql = 'SELECT MAX(id) FROM test;'
    # sql = 'insert ignore into test(link, title, author) values("test9@163.com", "12345", "56789");'
    ver = cursor.execute(sql)
    data = cursor.fetchone()
    print(data)
    # 逻辑:一阶段用insert ignore直接存入全部需要存入的数据,二阶段进入链接获取图片发帖时间等信息后进行一个update操作.(二阶段只会建立在一阶段前提下进行,所以二阶段只需要进行更新数据即可.)

    '''
    SELECT MAX(Age) FROM Student {查询学生表中年级最大的}
    SELECT MIN(Age) FROM Student {查询学生表中年级最小的}
    SELECT AVG(Age) FROM Student {查询学生的平均年级}
    SELECT COUNT(*) FROM Student {查询表中的总记录}
    '''

    conn.commit()

    # 涉及写操作要注意提交
    # conn.commit()
    
    # 关闭连接
    cursor.close()
    conn.close()

if __name__ == '__main__':
    get()
    # mysql_test()