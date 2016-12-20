import requests
import re

def getXsrf(data):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"', flags=0)
    match = cer.search(data)
    return match

sess = requests.session()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
res = sess.get('http://www.zhihu.com/')
xsrf = getXsrf(res.text)
payload = {
    'email':'2994794579@qq.com',
    'password':'venus950526',
    '_xsrf':xsrf,
    'captcha_type':'cn',
    'remember_me':'true'
}
url = 'https://www.zhihu.com/login/email'
r = sess.post(url, data= payload, headers= headers)
print (r.text)