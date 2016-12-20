import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
#homepage part
sess = requests.session()
homepage = sess.get('https://my.waseda.jp/login/login',headers = headers)

#login interface
logininterface = sess.get('https://coursereg.waseda.jp/portal/simpleportal.php?HID_P14=JA', headers = headers)
def getloginbutton(html):
    pattern = re.compile(r'action=\"(.*)\" method=\"post\"')
    match = pattern.search(html)
    return match.group(1)
loginbutton = getloginbutton(logininterface.text)
loginurl = 'https://iaidp.ia.waseda.jp' + loginbutton

#login_1
logindata1 = {
    'j_username': '*******',
    'j_password': '********',
    '_eventId_proceed': 'Login'
}
login_1 = sess.post(loginurl,data=logindata1, headers=headers)

#login_2
loginurl2 = 'https://coursereg.waseda.jp/Shibboleth.sso/SAML2/POST'
def getlogindata(html):
    pattern1 = re.compile(r'name=\"RelayState\" value=\"(.*)\"')
    match1 = pattern1.search(html)
    pattern2 = re.compile(r'name=\"SAMLResponse\" value=\"(.*)\"')
    match2 = pattern2.search(html)
    return match1.group(1),match2.group(1)

RelayState,SAMLResponse = getlogindata(login_1.text)
RelayState = RelayState.replace('&#x3a;',':') #返回的url解析（为什么要编码？）

logindata2={
    'RelayState':RelayState,
    'SAMLResponse':SAMLResponse
}
login_2 = sess.post(loginurl2,headers=headers,data=logindata2)
#print (login_2.text)
#模拟点击科目登录
def getloadinfo1(html):
    pattern1 = re.compile(r'name=\"KojinNO\" value=\"(.*)\"')
    match1 = pattern1.search(html)
    pattern2 = re.compile(r'name=\"sessionid\" value=\"(.*)\"')
    match2 = pattern2.search(html)
    pattern3 = re.compile(r'name=\"HID_P3\" value=\"(.*)\"')
    match3 = pattern3.search(html)
    return match1.group(1),match2.group(1),match3.group(1)

KojinNO,sessionid,HID_P3 = getloadinfo1(login_2.text)

#print (KojinNO,sessionid,HID_P3,HID_P8)
datalast1={
    'HID_P14':'JA',
    'HID_P2':'ST',
    'HID_P3':HID_P3,
    'HID_P6':'eStudent',
    'HID_P8':'ea02',
    'JITSUGEN':'web',
    'KojinNO':KojinNO,
    'NewOldFlg':'',
    'frame':'0',
    'pageflag':'1000',
    'sessionid':sessionid,
    'status':'0',
    'url':'https://www.wnp15.waseda.jp/kyomu/epb1110.htm'
}
getback = sess.post('https://coursereg.waseda.jp/portal/simpleportal.php',headers = headers,data=datalast1)
#print (getback.text)

def getloadinfo2(html):
    regex = re.compile(r'type=\"hidden\" name=\"HID_P.*\" value=\"(.*)\"')
    list = regex.findall(html)
    return list

list = getloadinfo2(getback.text)
datalast2={
    'HID_P1':list[0],
    'HID_P2':list[1],
    'HID_P3': list[2],
    'HID_P4': list[3],
    'HID_P5': list[4],
    'HID_P6': list[5],
    'HID_P7': list[6],
    'HID_P8': list[7],
    'HID_P9': list[8],
    'HID_P10': list[9],
    'HID_P12': list[10],
    'HID_P14': list[11],
    'HID_P20': list[12],
    'HID_P11[0],': list[13]
}

courses = sess.post('https://www.wnp15.waseda.jp/kyomu/epb1110.htm',data = datalast2,headers = headers)
print (courses.text)
