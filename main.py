import json
import time
import pymysql
import requests
import threading
from bs4 import BeautifulSoup
from selenium import webdriver


def CreateDb(host, user, password): #数据库创建
    try:
        connect = pymysql.connect(
            host=str(host),
            user=str(user),
            password=str(password),
            charset='utf8',
        )
        cursor = connect.cursor()
        cursor.execute("create database fans_db character set utf8;")

        connect.commit()
        connect.close()
        print('database created successfully.')
    except:
        print('database fans_db has exists.')


def Insert(host, user, password, fans_uid, name, sex, level, vip_status, follower, following, TimeArray):   #数据导入
    connect = pymysql.connect(
        host=str(host),
        user=str(user),
        password=str(password),
        database='fans_db',
        charset='utf8',
    )
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS info(id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, ' \
          'fans_uid VARCHAR(255) NOT NULL , name VARCHAR(255) NOT NULL, ' \
          'sex VARCHAR(255) NOT NULL , level VARCHAR(255) NOT NULL, ' \
          'vip_status VARCHAR(255) NOT NULL , follower VARCHAR(255) NOT NULL, ' \
          'following VARCHAR(255) NOT NULL , time_follow VARCHAR(255) NOT NULL) '

    cursor.execute(sql)
    sql2 = 'insert into info(fans_uid, name, sex, level, vip_status, follower, following, ' \
           'time_follow)' \
           'values(%s, %s, %s, %s, %s, %s, %s, %s);'
    data = (fans_uid, name, sex, level, vip_status, follower, following, TimeArray)

    cursor.execute(sql2, data)
    connect.commit()
    connect.close()


def GetPage(mid, n, sessdata):  # 发送主页面请求
    cookies = {
        'SESSDATA': sessdata,   # SESSDATA
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Referer': 'https://space.bilibili.com/' + str(mid) + '/fans/fans',
    }

    params = (
        ('vmid', str(mid)),  # up主uid
        ('pn', str(n)), # 页数
        ('ps', '50'),   # 每页数据条数（最大为50）
        ('order', 'desc'),
    )

    res_up = requests.get('https://api.bilibili.com/x/relation/followers',
                          headers=headers, params=params, cookies=cookies)
    return res_up


def GetFans_1(mid): # 粉丝页面1
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Origin': 'https://space.bilibili.com',
        'Connection': 'keep-alive',
        'Referer': 'https://space.bilibili.com/' + str(mid) + '/fans/fans',
        'Cache-Control': 'max-age=0',
    }
    params1 = (
        ('mid', str(mid)),
        ('jsonp', 'jsonp'),
    )
    res_fans1 = requests.get('https://api.bilibili.com/x/space/acc/info', headers=headers1, params=params1)

    return res_fans1


def GetFans_2(mid): # 粉丝页面2（需要selenium部分）
    option = webdriver.FirefoxOptions() # 浏览器设置为firefox
    option.add_argument('--headless')   # 设置为后台运行
    driver = webdriver.Firefox(options=option)
    driver.get('https://space.bilibili.com/' + str(mid))
    driver.execute_script("return document.documentElement.outerHTML")
    time.sleep(1)

    return driver


def vipJudge(vip_type): # 会员判断
    if vip_type == 0:
        vip_status = '非大会员'
    else:
        vip_status = '大会员'
    return vip_status


def timeFormat(timeStamp):  # 时间戳转换
    if timeStamp == 'NULL':
        return ' '
    else:
        timeArray = time.localtime(timeStamp)
        TimeArray = time.strftime("%Y-%m-%d", timeArray)
        return TimeArray


def thread():   # 多线程
    for entry in json_obj['data']['list']:
        t = threading.Thread(target=FansData, args=(entry,))
        threads.append(t)
    for t in range(1, 11):
        threads[t].start()
    time.sleep(10)
    for t in range(11, 21):
        threads[t].start()
    time.sleep(10)
    for t in range(21, 31):
        threads[t].start()
    time.sleep(10)


def FansData(entry):    # 数据提取处理
    times = 0
    times = times + 1
    fans_uid = entry['mid']
    name = entry['uname']
    try:
        mtime = entry['mtime']
    except:
        mtime = 'NULL'

    Res = GetFans_1(fans_uid)

    json_obj1 = json.loads(Res.text)
    sex = json_obj1['data']['sex']
    level = json_obj1['data']['level']
    vip = json_obj1['data']['vip']['type']

    start = time.perf_counter()
    driver = GetFans_2(fans_uid)
    end = time.perf_counter()
    print(times, end - start)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    following = soup.select('#n-gz')[0].text.replace(' ', '').replace('\n', '').replace('\r', '')
    follower = soup.select('#n-fs')[0].text.replace(' ', '').replace('\n', '').replace('\r', '')

    driver.close()

    Insert(host_input, user_input, passw_input, fans_uid, name, sex, level, vipJudge(vip),
           follower, following, timeFormat(mtime))
    time.sleep(0.5)


mid_input = input('输入up主uid：')
while True:
    host_input = input('数据库host：')
    user_input = input('数据库user：')
    passw_input = input('数据库password：')
    id_judge = input('是否为本人可登录账号？（y/n）：')
    if id_judge == 'y':
        SESSDATA = input('输入sessdata：')
        break
    elif id_judge == 'n':
        SESSDATA = ' '
        break

CreateDb(host_input, user_input, passw_input)
print('开始获取')

threads = []
t_list = []

for i in range(1, 6):   # 粉丝列表页数 他人账号最多提取1至5页。自己账号最大可修改为1, 21
    res = GetPage(mid_input, i, SESSDATA)
    json_obj = json.loads(res.text)
    for Entry in json_obj['data']['list']:
        t = threading.Thread(target=FansData, args=(Entry,))
        threads.append(t)

    for t in range(1, 11):
        threads[t].start()
        time.sleep(0.5)
    time.sleep(10)
    for t in range(11, 21):
        threads[t].start()
        time.sleep(0.5)
    time.sleep(10)
    for t in range(21, 31):
        threads[t].start()
        time.sleep(0.5)
    time.sleep(10)
    for t in range(31, 41):
        threads[t].start()
        time.sleep(0.5)
    time.sleep(10)
    for t in range(41, 51):
        threads[t].start()
        time.sleep(0.5)
    time.sleep(10)

    for t in threads:
        t.join()

