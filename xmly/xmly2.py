import requests
import json
import rsa
import base64
import time
from itertools import groupby
from functools import reduce
from random import choice
import hashlib
from datetime import datetime
from dateutil import tz
import os

# 喜马拉雅极速版加了bark通知，作者github https://github.com/Zero-S1/xmly_speed
# 使用参考 xmly_speed.md
# cookies填写

cookies1 = ""  # 字符串形式 都可以识别
cookies2 = {
}  # 字典形式




cookiesList = [cookies1, ]  # 多账号准备

xmly_speed_cookie ='''_xmLog=xm_kfyn5itg692198; 1&_device=iPhone&C5D8B777-201A-479C-B7AC-B8BA5ADC9229&1.1.10; 1&_token=191084372&E05BBB60240NED25CD0345B7C50CAE4B946D667E164BB71A6945E03336FCAEEFB790BAEBE184130M329312FD3546968_; NSUP=42E33F03%2C41BA403A%2C1602028306432; XUM=C5D8B777-201A-479C-B7AC-B8BA5ADC9229; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone XR; idfa=6EF3E645-FAD6-4B47-BDDD-978DA2F2D216; impl=com.ximalaya.tingLite; ip=192.168.31.104; net-mode=WIFI; res=828%2C1792
 _xmLog=xm_kg39l8wpkqknzj; 1&_device=iPhone&414C68E7-715F-475E-9776-2D89C4595066&1.1.10; 1&_token=260149230&ECEAD9D0240N6495943F0C58479D3E5257D56E082609E807B6255BE96E2672CDA8204559F19613M0349775CAAB9335_; NSUP=42E33EDE%2C41BA3F9B%2C1602309062656; XUM=414C68E7-715F-475E-9776-2D89C4595066; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone 6s Plus; idfa=414C68E7-715F-475E-9776-2D89C4595066; impl=com.ximalaya.tingLite; ip=240e:57d:1418:4599:da:408:100:0; net-mode=WIFI; res=1242%2C2208
_xmLog=xm_kg3p14uihd7aqi;1&_device=iPad&653F94B8-410E-4C69-B4C0-41611C41B4D2&1.1.10;1&_token=260235678&E6CB9350340C69B013D876ED1BC00FEDA4BBF6DEF61B6D7159D5857895D82666839F109197D8130M38E411DCAD6CC22_;NSUP=42E33ED5%2C41BA3FBB%2C1602334359552;XUM=653F94B8-410E-4C69-B4C0-41611C41B4D2;ainr=0;c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1;device_model=iPad 4; idfa=E4B9A2E5-5B7D-4A8B-959F-120B6D8B8A2C;impl=com.ximalaya.tingLite;ip=192.168.31.68;net-mode=WIFI;res=640%2C960
Cookie: _xmLog=xm_kgdvp6hrdrrzo9; 1&_device=iPhone&C8077270-DEA9-4D94-940B-D6203F1383C5&1.1.10; 1&_token=261793732&2D1DB430340N91220D343D863B9A6338B888C3B12D932567B042D3701381A02EEE753D9193F1174M7F15A0B45D1E595_; NSUP=; XUM=C8077270-DEA9-4D94-940B-D6203F1383C5; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone 5; idfa=00000000-0000-0000-0000-000000000000; impl=com.ximalaya.tingLite; ip=240e:3b9:1435:e380:f0:503:8046:ea14; net-mode=WIFI; res=640%2C1136

'''


xmly_bark_cookie='azjFQzUeTG5hVYx7cRJRTU'
UserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 iting/1.0.12 kdtunion_iting/1.0 iting(main)/1.0.12/ios_1"
# 非iOS设备的需要的自行修改,自己抓包 与cookie形式类似

iosrule=''
def str2dict(str_cookie):
    if type(str_cookie) == dict:
        return str_cookie
    tmp = str_cookie.split(";")
    dict_cookie = {}
    for i in tmp:
        j = i.split("=")
        if not j[0]:
            continue
        dict_cookie[j[0].strip()] = j[1].strip()
    return dict_cookie




'''if "XMLY_SPEED_COOKIE" in os.environ:
    """
    判断是否运行自GitHub action,"XMLY_SPEED_COOKIE" 该参数与 repo里的Secrets的名称保持一致
    """
    print("执行自GitHub action")
    xmly_speed_cookie = os.environ["XMLY_SPEED_COOKIE"]
    '''
 
cookiesList = []  # 重置cookiesList
for line in xmly_speed_cookie.split('\n'):
    if not line:
       continue 
    cookiesList.append(line)

if not cookiesList[0]:
    print("cookie为空 跳出X")
    exit()
mins = int(time.time())
date_stamp = (mins-57600) % 86400
#print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
_datatime = datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y%m%d", )
print(_datatime)
print("今日已过秒数: ", date_stamp)
print("当前时间戳", mins)

if "XMLY_BARK_COOKIE" in os.environ:
    xmly_bark_cookie = os.environ["XMLY_BARK_COOKIE"]

def listenData(cookies):
    headers = {
        'User-Agent': UserAgent,
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json',
    }
    listentime = date_stamp
    print(listentime//60)
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        # 'activtyId': 'listenAward',
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        # 'nativeListenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }

    response = requests.post('http://m.ximalaya.com/speed/web-earn/listen/client/data',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def ans_receive(cookies, paperId, lastTopicId, receiveType):

    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    _checkData = f"""lastTopicId={lastTopicId}&numOfAnswers=3&receiveType={receiveType}"""
    checkData = rsa_encrypt(str(_checkData), pubkey_str)

    data = {
        "paperId": paperId,
        "checkData": checkData,
        "lastTopicId": lastTopicId,
        "numOfAnswers": 3,
        "receiveType": receiveType
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/receive',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def ans_restore(cookies):
    """
    看视频回复体力，type=2
    """
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    checkData = rsa_encrypt("restoreType=2", pubkey_str)

    data = {
        "restoreType": 2,
        "checkData": checkData,
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/restore',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def ans_getTimes(cookies):

    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/topic/user', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    stamina = result["data"]["stamina"]  # 答题次数
    remainingTimes = result["data"]["remainingTimes"]  # 可回复次数
    print(f"answer_stamina答题次数: {stamina}")
    print(f"answer_remainingTimes可回复次数: {remainingTimes}\n")
    return {"stamina": stamina,
            "remainingTimes": remainingTimes}


def ans_start(cookies):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/topic/start', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    paperId = result["data"]["paperId"]
    dateStr = result["data"]["dateStr"]
    lastTopicId = result["data"]["topics"][2]["topicId"]
    print(paperId, dateStr, lastTopicId)
    return paperId, dateStr, lastTopicId


def _str2key(s):
    b_str = base64.b64decode(s)
    if len(b_str) < 162:
        return False
    hex_str = ''
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2
    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]
    return modulus, exponent


def rsa_encrypt(s, pubkey_str):
    key = _str2key(pubkey_str)
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    pubkey = rsa.PublicKey(modulus, exponent)
    return base64.b64encode(rsa.encrypt(s.encode(), pubkey)).decode()


pubkey_str = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVhaR3Or7suUlwHUl2Ly36uVmboZ3+HhovogDjLgRE9CbaUokS2eqGaVFfbxAUxFThNDuXq/fBD+SdUgppmcZrIw4HMMP4AtE2qJJQH/KxPWmbXH7Lv+9CisNtPYOlvWJ/GHRqf9x3TBKjjeJ2CjuVxlPBDX63+Ecil2JR9klVawIDAQAB"


def lottery_info(cookies):
    print("\n【幸运大转盘】")
    """
    转盘信息查询
    """
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    # 查询信息
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/inspire/lottery/info', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    print(result)

    remainingTimes = result["data"]["remainingTimes"]
    print(f'lottery_remainingTimes转盘剩余次数: {remainingTimes}\n')
    if result["data"]["chanceId"] != 0 and result["data"]["remainingTimes"] == 1:
        print("免费抽奖次数")
        return
        data = {
            "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
        }
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        print(response.text)
        return
    if result["data"]["remainingTimes"] in [0, 1]:
        return
    data = {
        "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)
    # for i in range(3):
    # 获取token
    # exit()
    if remainingTimes > 0:
        headers = {
            'Host': 'm.ximalaya.com',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-cn',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/inspire/lottery/token', headers=headers, cookies=cookies)
        print("token", response.text)
        result = json.loads(response.text)
        _id = result["data"]["id"]
        data = {
            "token": _id,
            "sign": rsa_encrypt(f"token={_id}&userId={uid}", pubkey_str),
        }
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'https://m.ximalaya.com',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
        }
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/chance',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        result = json.loads(response.text)
        print("chance", result)
        try:
           data = {
            "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
        }
        
           response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
           print("action", response.text)
        except Exception as e:
           print("action", str(e))


def task_label(cookies):
    print("\n【收听时长 30 60 90 】")
    """
    任务查看
    """
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('taskLabels', '1,2'),
    )

    response = requests.get('https://m.ximalaya.com/speed/task-center/task/record',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    taskList = result["taskList"]
    print(taskList)
    for i in taskList:
        if i["taskId"] in [79, 80, 81]:  # 收听时长
            if i["status"] == 1:  # 可以领取
                print(i)
                taskRecordId = i["taskRecordId"]
                headers = {
                    'User-Agent': UserAgent,
                    'Host': 'm.ximalaya.com',
                    'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
                    'Origin': 'https://m.ximalaya.com',
                }

                response = requests.post(
                    f'https://m.ximalaya.com/speed/task-center/task/receive/{taskRecordId}', headers=headers, cookies=cookies)
                print(response.text)
                time.sleep(1)

                print("\n")


def checkin(cookies):
    print("\n【连续签到】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('time', f"""{int(time.time()*1000)}"""),
    )
    response = requests.get('https://m.ximalaya.com/speed/task-center/check-in/record',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    # print(result)
    print(f"""连续签到{result["continuousDays"]}/{result["historyDays"]}天""")
    print(result["isTickedToday"])
    if result["isTickedToday"] == False:
        print("!!!未签到")
        pass


def group(cookies):
    print("\n【拼手气参团】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/growth-groupon-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('pageNo', '1'),
        ('pageSize', '10'),
        ('isMain', 'true'),
    )

    response = requests.get('https://m.ximalaya.com/speed/web-earn/group/list',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    todayJoinGroupCount = result["data"]["todayJoinGroupCount"]
    print(f"""{todayJoinGroupCount}/10""")
    if todayJoinGroupCount != 10:
        group_getReward(cookies, None, uid, "join")  # 加团

    groupInfoList = result["data"]["groupInfoList"][:todayJoinGroupCount]
    for i in groupInfoList:
        if not i["drawConsolationAward"]:         # 看广告
            userId = uid
            group_getReward(cookies, i["id"], userId, "")
            time.sleep(1)


def group_getReward(cookies, groupId, userId, flag):
    # print("\n【拼手气 成团】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/growth-groupon-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    """
    token
    """
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/group/token', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    print(result)
    token = result["data"]["id"]
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/growth-groupon-h5/home',
    }

    """
    drawJoin
    """
    data = {
        "groupId": groupId,
        "sign": rsa_encrypt(f"token={token}&userId={userId}", pubkey_str),
        "token": token,
    }
    if flag == "join":
        data["groupType"] = 1

    response = requests.post('https://m.ximalaya.com/speed/web-earn/group/drawJoin',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print("drawJoin", response.text, "\n")


def divide(cookies):
    print("\n【瓜分】")

    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'XMSonicCacheURLHeader': '',
        'User-Agent': UserAgent,
        'Referer': 'http://m.ximalaya.com/growth-ssr-speed-welfare-center/page/divide-coin',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    }
    response = requests.get(
        f'http://m.ximalaya.com/speed/web-earn/carve/multipleInfo?ts={int(time.time()*1000)}', headers=headers, cookies=cookies)
    print(response.text)
    current = json.loads(response.text)["data"]["currentMultiple"]
    print(f"""{current}/5""")
    for i in range(5-current):
        print(i)
        response = requests.get(
            'http://m.ximalaya.com/speed/web-earn/carve/token', headers=headers, cookies=cookies)
        token = json.loads(response.text)["data"]["id"]

        data = {
            "data": rsa_encrypt(token+uid+uuid, pubkey_str),
            "token": token}
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'http://m.ximalaya.com',
            'Referer': 'http://m.ximalaya.com/growth-ssr-speed-welfare-center/page/divide-coin',
        }
        response = requests.post(
            'http://m.ximalaya.com/speed/web-earn/carve/add', headers=headers, cookies=cookies, data=json.dumps(data))
        print(response.text)
        time.sleep(1)


def ad_score(cookies, businessType, taskId):

    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain ,*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/task-center/ad/token', headers=headers, cookies=cookies)
    result = response.json()
    token = result["id"]
    data = {
        "taskId": taskId,
        "businessType": businessType,
        "rsaSign": rsa_encrypt(f"""businessType={businessType}&token={token}&uid={uid}""", pubkey_str),
    }
    response = requests.post(f'https://m.ximalaya.com/speed/task-center/ad/score',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)
    print("\n")


def ad_score_8(cookies, businessType, taskId, stage):

    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain ,*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/task-center/ad/token', headers=headers, cookies=cookies)
    result = response.json()
    token = result["id"]
    data = {
        "taskId": taskId,
        "businessType": businessType,
        "rsaSign": rsa_encrypt(f"""businessType={businessType}&token={token}&uid={uid}""", pubkey_str),
        "extendMap": {"stage": stage}
    }
    response = requests.post(f'https://m.ximalaya.com/speed/task-center/ad/score',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)
    print("\n")


def bubble(cookies):
    print("\n【bubble】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
    }

    data = {"listenTime": "41246", "signature": "2b1cc9ee020db596d28831cff8874d9c",
            "currentTimeMillis": "1596695606145", "uid": uid, "expire": False}

    response = requests.post('https://m.ximalaya.com/speed/web-earn/listen/bubbles',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    result = response.json()
    print(result)
    for i in result["data"]["effectiveBubbles"]:
        print(i["id"])
        receive(cookies, i["id"])
        time.sleep(1)
        ad_score(cookies, 7, i["id"])
    for i in result["data"]["expiredBubbles"]:
        ad_score(cookies, 6, i["id"])


def receive(cookies, taskId):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        f'https://m.ximalaya.com/speed/web-earn/listen/receive/{taskId}', headers=headers, cookies=cookies)
    print("receive: ", response.text)


def stage_(cookies):
    """阶段红包"""
    print("\n【阶段红包】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        f'https://m.ximalaya.com/speed/web-earn/task/stage-rewards-daily', headers=headers, cookies=cookies)
    result = response.json()  # ["data"]
    if "errorCode" in result:
        print(result)
        return
    result = result["data"]["stageRewards"]
    j = 1
    enable_index = [i["status"] == 1 for i in result]
    for i in enable_index:
        if i:
            headers = {
                'Host': 'm.ximalaya.com',
                'Accept': 'application/json, text/plain, */*',
                'Connection': 'keep-alive',
                'User-Agent': UserAgent,
                'Accept-Language': 'zh-cn',
                'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
                'Accept-Encoding': 'gzip, deflate, br',
            }

            params = (
                ('stage', str(j)),
            )

            response = requests.get('https://m.ximalaya.com/speed/web-earn/task/stage-reward-daily/receive',
                                    headers=headers, params=params, cookies=cookies)
            print(response.text)
            time.sleep(1)
            ad_score_8(cookies, 8, 120, j)
        j += 1

    print(enable_index)


def get_card_coin(cookies, themeId, cardIdList):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/3',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    data = {
        "cardIdList": cardIdList,
        "themeId": themeId,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCoin',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def exchangeCard(cookies, toCardAwardId, fromId):
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    data = {
        "toCardAwardId": toCardAwardId,
        "fromId": fromId,
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCard',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def card_exchangeCoin(cookies, themeId, cardIdList):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/3',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    data = {
        "cardIdList": cardIdList,
        "themeId": themeId,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCoin',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print("card_exchangeCoin: ", response.text)


def card_exchangeCard(cookies, toCardAwardId, fromRecordIdList):
    fromRecordIdList = sorted(fromRecordIdList)
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    data = {
        "toCardAwardId": toCardAwardId,
        "fromRecordIdList": fromRecordIdList,
        "exchangeType": 1,
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCard',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)

def draw_5card(cookies, drawRecordIdList):  # 五连抽
    drawRecordIdList = sorted(drawRecordIdList)
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    data = {
        "signData": rsa_encrypt(f"{''.join(str(i) for i in drawRecordIdList)}{uid}", pubkey_str),
        "drawRecordIdList": drawRecordIdList,
        "drawType": 2,
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/draw',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print("五连抽: ", response.text)


def card(cookies):
    print("\n【抽卡】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    data = response.json()["data"]
    #######
    # 5连抽
    drawRecordIdList = data["drawRecordIdList"]
    print("抽卡机会: ", drawRecordIdList)
    for _ in range(len(drawRecordIdList)//5):
        tmp = []
        for _ in range(5):
            tmp.append(drawRecordIdList.pop())
        draw_5card(cookies, tmp)
    ########
    # 手牌兑换金币
    # 1 万能卡  10 碎片
    print("检查手牌，卡牌兑金币")
    themeId_id_map = {
        2: [2, 3],
        3: [4, 5, 6, 7],
        4: [8, 9, 10, 11, 12],
        5: [13, 14, 15, 16, 17, 18],
        6: [19, 20, 21, 22],
        7: [23, 24, 25, 26, 27],
        8: [28, 29, 30, 31, 32],
        9: [33, 34, 35, 36, 37]
    }
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    data = response.json()["data"]
    userCardsList = data["userCardsList"]  # 手牌
    lstg = groupby(userCardsList, key=lambda x: x["themeId"])
    for key, group in lstg:
        if key in [1, 10]:
            continue
        themeId = key
        ids = list(group)
        tmp_recordId = []
        tmp_id = []
        for i in ids:
            if i["id"] in tmp_id:
                continue
            tmp_recordId.append(i["recordId"])
            tmp_id.append(i["id"])
        if len(tmp_recordId) == len(themeId_id_map[key]):
            print("可以兑换")
            card_exchangeCoin(cookies, themeId, tmp_recordId)
    ###############
    # 万能卡兑换稀有卡
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    data = response.json()["data"]
    userCardsList = data["userCardsList"]
    omnipotentCard = [i for i in userCardsList if i["id"] == 1]
    cityCardId = [i["id"] for i in userCardsList if i["themeId"] == 9]
    need = set(themeId_id_map[9])-set(cityCardId)

    print("万能卡: ", [i['recordId'] for i in omnipotentCard])
    for _ in range(len(omnipotentCard)//4):
        tmp = []
        for _ in range(4):
            tmp.append(omnipotentCard.pop())
        fromRecordIdList = [i['recordId'] for i in tmp]
        if need:
            print("万能卡兑换稀有卡:")
            card_exchangeCard(cookies, need.pop(), fromRecordIdList)
def getOmnipotentCard(cookies):
    print("\n 【万能卡】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    result = requests.get('https://m.ximalaya.com/speed/web-earn/card/omnipotentCardInfo',
                         headers=headers, cookies=cookies,).json()
    print(result)
    count=result["data"]["count"]
    if count == 5:
        print("今日已满")
        return
    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/1',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    data = {
        "listenTime": mins-date_stamp,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }

    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/getOmnipotentCard',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def reportTime(cookies):
    print("\n【收听获得抽卡机会】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    listenTime = mins-date_stamp
    data = {"listenTime": listenTime,
            "signData": rsa_encrypt(f"{_datatime}{listenTime}{uid}", pubkey_str), }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/reportTime',
                             headers=headers, cookies=cookies, data=json.dumps(data)).json()
    if response["data"]["upperLimit"]:
        print("今日已达上限")

def hand(cookies):
    print("\n 【猜拳】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'm.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/finger-game/home',
    }
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/mora/remainingTimes', headers=headers, cookies=cookies)
    lastTimes = response.json()["data"]
    print(lastTimes)
    for _ in range(lastTimes):
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'https://m.ximalaya.com',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/finger-game/home',
        }

        data = '{"betAmount":200,"gesture":2}'

        response = requests.post('https://m.ximalaya.com/speed/web-earn/mora/action',
                                 headers=headers, cookies=cookies, data=data)
        result = response.json()
        print(result)
        result=result["data"]
        if not result:
            return
        if result["winFlag"] == 1:
            moraRecordId = result["moraRecordId"]
            data = {"betAmount": 200,
                    "moraRecordId": moraRecordId,
                    "signData": rsa_encrypt(f"{200}{moraRecordId}{uid}", pubkey_str),
                    }

            response = requests.post(
                'https://m.ximalaya.com/speed/web-earn/mora/doubleAward', headers=headers, cookies=cookies, data=json.dumps(data))
            print(response.text)
            time.sleep(2)


def account(cookies):
    print("\n【打印当前信息】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': UserAgent,
        'Referer': 'https://m.ximalaya.com/speed/web-earn/wallet',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/account/coin', headers=headers, cookies=cookies)
    result = response.json()
    print(result)
    global iosrule
    global j
    iosrule+=f"""【账号{j}】当前剩余:{result["total"]/10000}今日获得:{result["todayTotal"]/10000}累计获得:{result["historyTotal"]/10000}"""+'\n'
    

    
def saveListenTime(cookies):
    print("\n【保存收听时长】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'mobile.ximalaya.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    listentime = date_stamp
    print(listentime//60)
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        'activtyId': 'listenAward',
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        'nativeListenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }

    response = requests.post('http://mobile.ximalaya.com/pizza-category/ball/saveListenTime',
                             headers=headers, cookies=cookies, data=data)
    print(response.text)
def read(cookies, uid):
    print("\n【阅读】")
    headers = {
        'Host': '51gzdhh.xyz',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    params = (
        ('hid', '233'),
    )
    response = requests.get(
        'https://51gzdhh.xyz/api/new/newConfig', headers=headers, params=params)
    result = response.json()
    pid = str(result["pid"])
    headers = {
        'Host': '51gzdhh.xyz',
        'content-length': '37',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    data = {"pid": str(pid), "mtuserid": uid}

    response = requests.post(
        'https://51gzdhh.xyz/api/new/hui/complete', headers=headers, data=json.dumps(data))
    result = response.json()
    print(result)
    if result["status"]==-2:
        print("无法阅读,尝试从安卓端手动开启")
        return 
    print(result["completeList"])
    if result["isComplete"]:
        print("今日完成阅读")
        return
    headers = {
        'Host': '51gzdhh.xyz',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    taskIds = set(['242', '239', '241', '240', '238', '236',
                   '237', '235', '234'])-set(result["completeList"])
    params = (
        ('userid', str(uid)),
        ('pid', pid),
        ('taskid', taskIds.pop()),
        ('imei', ''),
    )

    response = requests.get(
        'https://51gzdhh.xyz/new/userCompleteNew', headers=headers, params=params)
    result = response.json()
    print(result)
    
def ans_receive(cookies, paperId, lastTopicId, receiveType):
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    _checkData = f"""lastTopicId={lastTopicId}&numOfAnswers=3&receiveType={receiveType}"""
    checkData = rsa_encrypt(str(_checkData), pubkey_str)
    data = {
        "paperId": paperId,
        "checkData": checkData,
        "lastTopicId": lastTopicId,
        "numOfAnswers": 3,
        "receiveType": receiveType
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/receive',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)
    
def dati_taskrecord(cookies):
    print("\n【打印答题任务奖励】")
    headers = {
        'User-Agent': UserAgent,

    }
    response = requests.get('https://m.ximalaya.com/speed/web-earn/task/record?taskLabels=4&showReceived=true',
                            headers=headers, cookies=cookies)
    result = response.json()
    #print(response.text)
    if len(result['taskList'])>0:
       for ls in result['taskList']:
         if ls['taskRecordId']>0:
           response = requests.post('https://m.ximalaya.com/speed/web-earn/task/receive/'+str(ls['taskRecordId']),
                           headers=headers, cookies=cookies)
           print(response.text)
           
def homehourred(cookies):
    print("\n【打印首页时段奖励】")
    headers = {
        'User-Agent': UserAgent,}
    currentTimeMillis = int(time.time()*1000)-2
    response = requests.get(f'http://mobile.ximalaya.com/pizza-category/activity/getAward?activtyId=indexSegAward&ballKey={uid}&currentTimeMillis={currentTimeMillis}&sawVideoSignature={currentTimeMillis}+{uid}&version=2',
                            headers=headers, cookies=cookies)
    print(response.text)
    result = response.json()
    #if "ret" in result and result["ret"] == 0:
    #awardReceiveId = result["awardReceiveId"]
    for num in range(1,7):
       xg=time.strftime("%Y%m%d", time.localtime())
       response = requests.get(f'http://mobile.ximalaya.com/pizza-category/activity/awardMultiple?activtyId=indexSegAward&awardReceiveId={uid}-{xg}-6-{num}',
                            headers=headers, cookies=cookies)  
       result = response.json()
       print(response.text)
       time.sleep(1)
def homebox(cookies):
    print("\n【打印宝箱奖励】")
    headers = {
        'User-Agent': UserAgent,}
    currentTimeMillis = int(time.time()*1000)-2
    response = requests.get(f'http://mobile.ximalaya.com/pizza-category/activity/getAward?activtyId=baoxiangAward&ballKey={uid}&currentTimeMillis={currentTimeMillis}&sawVideoSignature={currentTimeMillis}+{uid}&version=2',
                            headers=headers, cookies=cookies)
    print(response.text)
    result = response.json()
    #if "ret" in result and result["ret"] == 0:
    #awardReceiveId = result["awardReceiveId"]
    for num in range(1,7):
       xg=time.strftime("%Y%m%d", time.localtime())
       response = requests.get(f'http://mobile.ximalaya.com/pizza-category/activity/awardMultiple?activtyId=baoxiangAward&awardReceiveId={uid}-{xg}-6-{num}',
                            headers=headers, cookies=cookies)  
       result = response.json()
       print(response.text)
       time.sleep(1)
       
       
       
       
def pushmsg():
  if xmly_bark_cookie.strip():
    purl = f'https://api.day.app/{xmly_bark_cookie}/喜马拉雅极速/{iosrule}'
    response = requests.post(purl)
    print(response.text)
 
    
	
	
	
	
	
	
	
def m():
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(('2'+'a45421662ad74842a3f3118aa474ac6c').encode()).hexdigest()
    print(sign)
##################################################################

#http://113.96.156.166/pizza-category/activity/getAward?activtyId=gameTimeAward&currentTimeMillis=1602054131470&gameTime=6&signature=777203037112a37f8a4be0fb1b1cc592&uid=191084372

def main(cookies):
    print("#"*20)
    print("\n")
    listenData(cookies)
    saveListenTime(cookies)
    card(cookies)
    #hand(cookies)
    #dati_taskrecord(cookies)
    homehourred(cookies)
    #read(cookies, uid)
    reportTime(cookies)
    homebox(cookies)
    getOmnipotentCard(cookies)
    #stage_(cookies)
    bubble(cookies)
    #checkin(cookies)
    print("\n【答题】")
    ans_times = ans_getTimes(cookies)

    for i in range(ans_times["stamina"]):
        paperId, dateStr, lastTopicId = ans_start(cookies)
        ans_receive(cookies, paperId, lastTopicId, 1)
        time.sleep(2)
        ans_receive(cookies, paperId, lastTopicId, 2)
        time.sleep(2)

    if ans_times["remainingTimes"] > 0:
        print("[看视频回复体力]")
        ans_restore(cookies)
        for i in range(5):
            paperId, dateStr, lastTopicId = ans_start(cookies)
            ans_receive(cookies, paperId, lastTopicId, 1)
            time.sleep(1)
            ans_receive(cookies, paperId, lastTopicId, 2)
            time.sleep(1)

    lottery_info(cookies)

    print("\n")

j=0
for i in cookiesList:
    j+=1
    print(">>>>>>>>>【账号"+str(j)+"开始】")
    cookies = str2dict(i)
    uid = cookies["1&_token"].split("&")[0]
    uuid = cookies["XUM"]
    main(cookies)
   
    #exit()

    
    
