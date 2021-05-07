import requests
import urllib
from bs4 import BeautifulSoup
import re
import json
import pymysql
import config
import time

"""
使用之前注意更新token和Cookie
"""

token = config.token
dirname = config.dirname

headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
headers['Cookie'] = config.Cookie
headers['Connection'] = 'keep-alive'

url = 'https://mp.weixin.qq.com/cgi-bin/user_tag?action=get_user_list&token=%s&lang=zh_CN&begin_openid=%s&begin_create_time=%s&limit=1'
url_img = 'https://mp.weixin.qq.com/misc/getheadimg?fakeid=%s&token=%s&lang=zh_CN'

db = pymysql.connect(host=config.database_ip, user=config.database_user, password=config.database_pwd, database=config.database_name, charset='utf8mb4')
cursor = db.cursor()

turn = 1

while True:
    print('ns:' + str(turn))
    turn = turn + 1
    cursor.execute("SELECT * FROM usertoget")
    result = cursor.fetchall()
    for row in result:
        cursor.execute("SELECT create_time FROM wewall_username WHERE id = '%s'"%row[0])
        begin_create_time = cursor.fetchone()
        if not begin_create_time:
            continue
        begin_create_time = begin_create_time[0]
        print(begin_create_time)
        req = urllib.request.Request(url%(token, row[0], begin_create_time), headers=headers)
        rep = urllib.request.urlopen(req, timeout=5)
        s = rep.read().decode('utf-8')
        s = json.loads(s)
        print(s)
        try:
            wx = s['user_list']['user_info_list']
        except:
            continue
        req = urllib.request.Request(url%(token, wx[0]['user_openid'], wx[0]['user_create_time']) + '&backfoward=0', headers=headers)
        rep = urllib.request.urlopen(req, timeout=5)
        s = rep.read().decode('utf-8')
        s = json.loads(s)
        print(s)
        try:
            wx = s['user_list']['user_info_list']
        except:
            continue
        if wx[0]['user_openid'] != row[0]:
            continue
        cursor.execute("UPDATE wewall_username SET username = %s WHERE id = %s", (wx[0]['user_name'], row[0]))
        db.commit()
        cursor.execute("DELETE FROM usertoget WHERE userid = %s",row[0])
        db.commit()
        fw = open(dirname + '%s.jpg'%row[0], 'wb')
        req = urllib.request.Request(url_img%(row[0], token), headers = headers)
        rep = urllib.request.urlopen(req, timeout = 5)
        fw.write(rep.read())
        fw.close()
        print(wx[0]['user_name'])
    db.commit()
    time.sleep(0.5)

db.close()
