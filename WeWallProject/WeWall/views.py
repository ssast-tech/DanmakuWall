# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
import hashlib
from bs4 import BeautifulSoup
import re
import xml.etree.cElementTree as ET
import pymysql
import yaml
import time
from WeWall import config

maxlen = config.maxlen

token = config.token
AES_TEXT_RESPONSE_TEMPLATE = """<xml><ToUserName><![CDATA[%(toUserName)s]]></ToUserName><FromUserName><![CDATA[%(FromUserName)s]]></FromUserName><CreateTime>%(timestamp)s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%(content)s]]></Content></xml>"""

yamlstr = '''
'/::)'            : '<img class="lineimg" src="./images/1.png"/>'
'/::~'            : '<img class="lineimg" src="./images/2.png"/>'
'/::B'            : '<img class="lineimg" src="./images/3.png"/>'
'/::|'            : '<img class="lineimg" src="./images/4.png"/>'
'/:8-)'           : '<img class="lineimg" src="./images/5.png"/>'
'/::<'            : '<img class="lineimg" src="./images/6.png"/>'
'/::$'            : '<img class="lineimg" src="./images/7.png"/>'
'/::X'            : '<img class="lineimg" src="./images/8.png"/>'
'/::Z'            : '<img class="lineimg" src="./images/9.png"/>'
'/::''('          : '<img class="lineimg" src="./images/10.png"/>'
'/::-|'           : '<img class="lineimg" src="./images/11.png"/>'
'/::@'            : '<img class="lineimg" src="./images/12.png"/>'
'/::P'            : '<img class="lineimg" src="./images/13.png"/>'
'/::D'            : '<img class="lineimg" src="./images/14.png"/>'
'/::O'            : '<img class="lineimg" src="./images/15.png"/>'
'/::('            : '<img class="lineimg" src="./images/16.png"/>'
"[\u56e7]"        : '<img class="lineimg" src="./images/17.png"/>'
"/:--b"           : '<img class="lineimg" src="./images/17.png"/>'
'/::Q'            : '<img class="lineimg" src="./images/18.png"/>'
'/::T'            : '<img class="lineimg" src="./images/19.png"/>'
'/:,@P'           : '<img class="lineimg" src="./images/20.png"/>'
'/:,@-D'          : '<img class="lineimg" src="./images/21.png"/>'
'/::d'            : '<img class="lineimg" src="./images/22.png"/>'
'/:,@o'           : '<img class="lineimg" src="./images/23.png"/>'
'/:|-)'           : '<img class="lineimg" src="./images/24.png"/>'
'/::!'            : '<img class="lineimg" src="./images/25.png"/>'
'/::L'            : '<img class="lineimg" src="./images/26.png"/>'
'/::>'            : '<img class="lineimg" src="./images/27.png"/>'
'/::,@'           : '<img class="lineimg" src="./images/28.png"/>'
'/:,@f'           : '<img class="lineimg" src="./images/29.png"/>'
'/::-S'           : '<img class="lineimg" src="./images/30.png"/>'
'/:?'             : '<img class="lineimg" src="./images/31.png"/>'
'/:,@x'           : '<img class="lineimg" src="./images/32.png"/>'
'/:,@@'           : '<img class="lineimg" src="./images/33.png"/>'
'/:,@!'           : '<img class="lineimg" src="./images/34.png"/>'
'/:!!!'           : '<img class="lineimg" src="./images/35.png"/>'
'/:xx'            : '<img class="lineimg" src="./images/36.png"/>'
'/:bye'           : '<img class="lineimg" src="./images/37.png"/>'
'[Bye]'           : '<img class="lineimg" src="./images/37.png"/>'
'/:wipe'          : '<img class="lineimg" src="./images/38.png"/>'
'/:dig'           : '<img class="lineimg" src="./images/39.png"/>'
'/:handclap'      : '<img class="lineimg" src="./images/40.png"/>'
'/:B-)'           : '<img class="lineimg" src="./images/41.png"/>'
'/:<@'            : '<img class="lineimg" src="./images/42.png"/>'
'/:@>'            : '<img class="lineimg" src="./images/43.png"/>'
'/::-O'           : '<img class="lineimg" src="./images/44.png"/>'
'/:>-|'           : '<img class="lineimg" src="./images/45.png"/>'
'/:P-('           : '<img class="lineimg" src="./images/46.png"/>'
'/::''|'          : '<img class="lineimg" src="./images/47.png"/>'
'/:X-)'           : '<img class="lineimg" src="./images/48.png"/>'
'/::*'            : '<img class="lineimg" src="./images/49.png"/>'
'/:8*'            : '<img class="lineimg" src="./images/50.png"/>'
'/:pd'            : '<img class="lineimg" src="./images/51.png"/>'
'/:<W>'           : '<img class="lineimg" src="./images/52.png"/>'
'/:beer'          : '<img class="lineimg" src="./images/53.png"/>'
'/:coffee'        : '<img class="lineimg" src="./images/54.png"/>'
'/:pig'           : '<img class="lineimg" src="./images/55.png"/>'
'/:rose'          : '<img class="lineimg" src="./images/56.png"/>'
'/:fade'          : '<img class="lineimg" src="./images/57.png"/>'
'/:showlove'      : '<img class="lineimg" src="./images/58.png"/>'
'/:heart'         : '<img class="lineimg" src="./images/59.png"/>'
'/:break'         : '<img class="lineimg" src="./images/60.png"/>'
'/:cake'          : '<img class="lineimg" src="./images/61.png"/>'
'/:bome'          : '<img class="lineimg" src="./images/62.png"/>'
'/:shit'          : '<img class="lineimg" src="./images/63.png"/>'
'/:moon'          : '<img class="lineimg" src="./images/64.png"/>'
'/:sun'           : '<img class="lineimg" src="./images/65.png"/>'
'/:hug'           : '<img class="lineimg" src="./images/66.png"/>'
'/:strong'        : '<img class="lineimg" src="./images/67.png"/>'
'/:weak'          : '<img class="lineimg" src="./images/68.png"/>'
'/:share'         : '<img class="lineimg" src="./images/69.png"/>'
'/:v'             : '<img class="lineimg" src="./images/70.png"/>'
'/:@)'            : '<img class="lineimg" src="./images/71.png"/>'
'[Salute]'        : '<img class="lineimg" src="./images/71.png"/>'
'/:jj'            : '<img class="lineimg" src="./images/72.png"/>'
'/:@@'            : '<img class="lineimg" src="./images/73.png"/>'
'/:ok'            : '<img class="lineimg" src="./images/74.png"/>'
'/:jump'          : '<img class="lineimg" src="./images/75.png"/>'
'/:shake'         : '<img class="lineimg" src="./images/76.png"/>'
'/:<O>'           : '<img class="lineimg" src="./images/77.png"/>'
'/:circle'        : '<img class="lineimg" src="./images/78.png"/>'
"\ue415"          : '<img class="lineimg" src="./images/79.png"/>'
"\ue40c"          : '<img class="lineimg" src="./images/80.png"/>'
"\ue412"          : '<img class="lineimg" src="./images/81.png"/>'
"\ue409"          : '<img class="lineimg" src="./images/82.png"/>'
"\ue40d"          : '<img class="lineimg" src="./images/83.png"/>'
"\ue107"          : '<img class="lineimg" src="./images/84.png"/>'
"\ue403"          : '<img class="lineimg" src="./images/85.png"/>'
"\ue40e"          : '<img class="lineimg" src="./images/86.png"/>'
'[Hey]'           : '<img class="lineimg" src="./images/87.png"/>'
'[Facepalm]'      : '<img class="lineimg" src="./images/88.png"/>'
'[Smirk]'         : '<img class="lineimg" src="./images/89.png"/>'
'[Smart]'         : '<img class="lineimg" src="./images/90.png"/>'
'[Concerned]'     : '<img class="lineimg" src="./images/91.png"/>'
'[Yeah!]'         : '<img class="lineimg" src="./images/92.png"/>'
"\ue11b"          : '<img class="lineimg" src="./images/93.png"/>'
"\ue41d"          : '<img class="lineimg" src="./images/94.png"/>'
"\ue14c"          : '<img class="lineimg" src="./images/95.png"/>'
"\ue312"          : '<img class="lineimg" src="./images/96.png"/>'
"\ue112"          : '<img class="lineimg" src="./images/97.png"/>'
'[Packet]'        : '<img class="lineimg" src="./images/98.png"/>'
"[\u767c]"        : '<img class="lineimg" src="./images/99.png"/>'
"[Rich]"          : '<img class="lineimg" src="./images/99.png"/>'
"[\u5c0f\u72d7]"  : '<img class="lineimg" src="./images/100.png"/>'
'[Pup]'           : '<img class="lineimg" src="./images/100.png"/>'
'''

def hangup(request):
    return HttpResponse("")

def receive(request):
	print('ggg')
	try:
		echostr = request.GET['echostr'];
		if checkSignature(request.GET['signature'], request.GET['timestamp'], request.GET['nonce']):
			return HttpResponse(echostr)
		else:
			return HttpResponse("error")
	except:
		xml = request.body
		print(xml)
		xml = xml.decode('utf8')
		xml_tree = ET.fromstring(xml)
		#print(str(xml_tree))
		username = xml_tree.find('FromUserName').text
		FromUserName = xml_tree.find('ToUserName').text
		#print(xml_tree.find('MsgType').text)
		if xml_tree.find('MsgType').text != 'text':
			return HttpResponse("")
		try:
			content = xml_tree.find('Content').text
		except:
			return response("对不起，暂不支持您发送的消息", username, FromUserName)
		if content == '[Unsupported Message]' or content == '【收到不支持的消息类型，暂无法显示】':
			return response("对不起，暂不支持您发送的消息", username, FromUserName)
		content = content.replace('<', '< ');
		content = content.replace('/:< @', '/:<@');
		content = content.replace('/:< W>', '/:<W>');
		content = content.replace('/:< O>', '/:<O>');
		content = content.replace('/::< ', '/::<');
		if len(content) >= maxlen:
			return response("对不起，您发送的消息过长", username, FromUserName)
		mappings = None
		mappings = yaml.load(yamlstr)
		#print(content)
		content = message_to_html(content, mappings)
		#print(content)
		db = pymysql.connect("localhost", config.db_username, config.db_password, config.db_dbname, charset='utf8mb4')
		cursor = db.cursor()
		#content = content.replace("'", "''")
		cursor.execute("INSERT INTO wewall_msg (content, userID, checked, danmu, wall) VALUES (%s, %s, true, false, false)" , (content, username))
	#	cursor.execute("dele")
		db.commit()
		cursor.execute("SELECT * FROM userid WHERE userid = %s", username);
		result = cursor.fetchone()
		if not result:
			cursor.execute("INSERT INTO userid (userid) VALUES(%s)", username);
			db.commit()
			cursor.execute("INSERT INTO usertoget (userid) VALUES(%s)", username)
			db.commit()
		db.close()
	#	return response("您的消息已发送，请等待审核", username, FromUserName)
		return response("已收到您发送的消息，请等待上墙", username, FromUserName)
		

def checkSignature(signature, timestamp, nonce):
	print(timestamp)
	sortlist = [token, timestamp, nonce];
	sortlist.sort();
	sha = hashlib.sha1()
	sha.update("".join(sortlist).encode('utf8'))
	if sha.hexdigest() == signature:
		return True
	else:
		return False

def message_to_html(message: str, lookup: dict):
    html = message
    for entry in lookup:
        html = html.replace(entry, lookup[entry])
    return html

def response(rpc_content, toUserName, FromUserName):
	timestamp = str(int(time.time()))
	resp_dict = {
			'timestamp' : timestamp,
			'toUserName': toUserName,
			'FromUserName' : FromUserName,
			'content'      : rpc_content,
		}
	resp_xml = AES_TEXT_RESPONSE_TEMPLATE % resp_dict
	print(resp_xml)
	return HttpResponse(resp_xml)

# Create your views here.
