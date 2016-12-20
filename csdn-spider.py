import requests


# 使用beautifulsoup来处理获取的html内容，这个库需要安装，还是使用pip install beautifulsoup4来安装
from bs4 import BeautifulSoup as bs
# 这个函数使用来提取流水号的
def toJson(str):
    '''
    提取lt流水号，将数据化为一个字典
    '''
    soup = bs(str)
    tt = {}
    # 提取form表单中所有的input标签，以字典的形式来保存name：value
    for inp in soup.form.find_all('input'):
        if inp.get('name') != None:
            tt[inp.get('name')] =inp.get('value')
    return tt


sess = requests.session()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

res = sess.get("http://passport.csdn.net/account/login")
soup = toJson(res.text)
payload = {
    'username':'316701882@qq.com',
    'password':'311402',
    'lt':soup["lt"],
    'execution':'e1s1',
    '_eventId':'submit'
}
url = 'https://passport.csdn.net/account/login'
r = sess.post(url, data= payload, headers= headers)
print (r.text)

