import json
import urllib.request

import pymysql

import config

"""
使用之前注意更新token和Cookie
"""

token = config.token
dirname = config.dirname

headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
headers['Cookie'] = config.Cookie
headers['Connection'] = 'keep-alive'

url = 'https://mp.weixin.qq.com/cgi-bin/user_tag?action=get_user_list&token=%s&lang=zh_CN&begin_openid=%s&begin_create_time=%s'
url_img = 'https://mp.weixin.qq.com/misc/getheadimg?fakeid=%s&token=%s&lang=zh_CN'

_url = url % (token, r'%s', r'%s')

db = pymysql.connect(host=config.database_ip, user=config.database_user,
                     password=config.database_pwd, database=config.database_name, charset='utf8mb4')
cursor = db.cursor()

for i in range(50000):
    req = urllib.request.Request(_url, headers=headers)
    rep = urllib.request.urlopen(req, timeout=60)
    s = rep.read().decode('utf-8')
    s = json.loads(s)
    try:
        wx = s['user_list']['user_info_list']
    except:
        print("over")
        break
    for k in wx:
        cursor.execute(
            "SELECT username from wewall_username where id = '%s';" % str(k['user_openid']))
        result = cursor.fetchone()
        username = k['user_name'].replace("'", "''")
        if not result:
            cursor.execute("INSERT INTO wewall_username (id, username, create_time) VALUES ('%s', '%s', '%s')" % (
                k['user_openid'], username, k['user_create_time']))
            db.commit()
        else:
            if k['user_name'] != result[0]:
                cursor.execute("UPDATE wewall_username SET username = '%s' WHERE id = '%s';" % (
                    username, k['user_openid']))
                db.commit()
                print(username)
            else:
                print("ok")
        fw = open(dirname + '%s.jpg' % k['user_openid'], 'wb')
        _url_img = url_img % (k['user_openid'], token)
        req = urllib.request.Request(_url_img, headers=headers)
        rep = urllib.request.urlopen(req, timeout=60)
        fw.write(rep.read())
        fw.close()
    print(i*20)
    _url = url % (token, wx[-1]['user_openid'], wx[-1]['user_create_time'])

db.close()
