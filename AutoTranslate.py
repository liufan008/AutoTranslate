import tkinter
import re
import json
import time
import random
import hashlib
import requests
from prettytable import PrettyTable

class Translate(object):
    def __init__(self):
        self.filename=None
        self.keylist={'title','label','footerText'}
    #有道翻译接口
    def translate(self,content):

        '''
        翻译模块
        :param content: 传入英语
        :return: 翻译结果
        '''
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        # 定义变量
        client = 'fanyideskweb'
        ctime = int(time.time() * 1000)
        salt = str(ctime + random.randint(1, 10))
        key = 'aNPG!!u6sesA>hBAW1@(-'
        sign = hashlib.md5((client + content + salt + key).encode('utf-8')).hexdigest()
        # 表单数据
        data = {}
        data['i'] = content
        data['from'] = 'EN'
        data['to'] = 'zh-CHS'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = salt
        data['sign'] = sign
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_CL1CKBUTTON'
        data['typoResult'] = 'false'
        # 请求头
        head = {}
        head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        head['Accept-Encoding'] = 'gzip, deflate'
        head['Accept-Language'] = 'zh-CN,zh;q=0.9'
        head['Connection'] = 'keep-alive'
        head['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        head[
            'Cookie'] = 'OUTFOX_SEARCH_USER_ID=-1645744815@10.169.0.84; JSESSIONID=aaa9_E-sQ3CQWaPTofjew; OUTFOX_SEARCH_USER_ID_NCOO=2007801178.0378454; fanyi-ad-id=39535; fanyi-ad-closed=1; ___rl__test__cookies=' + str(
            ctime)
        head['Host'] = 'fanyi.youdao.com'
        head['Origin'] = 'http://fanyi.youdao.com'
        head['Referer'] = 'http://fanyi.youdao.com/'
        head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5383.400 QQBrowser/10.0.1313.400'
        head['X-Requested-With'] = 'XMLHttpRequest'

        request = requests.request('POST',url,data=data,headers=head)
        # a=request.json()
        a=json.loads(request.text)
        result = a['translateResult'][0][0]['tgt']
        return result
    #读取文件
    def readList(self,url):

        xml=''
        #read txt method three
        f = open(url,"r")
        lines = f.readlines()
        for l in lines:
            xml+=l
        f.close()
        return xml
    #保存翻译后的文件
    def saveList(self,content):

        '''
        储存翻译结果
        :param content:
        :return:
        '''
        with open(self.filename,'w') as f:
            f.write(content)
        f.close()
    #遍历所有需要翻译的内容
    def tranreplace(self,xml):

        '''
        遍历需要翻译的内容
        :param xml:
        :return:
        '''
        tranxml=xml
        t=PrettyTable(["id","译前","译后"])
        id=1
        for item in self.keylist:
            rgxlable=r'<key>'+item+'</key>[^.](.*?)<string>(.*?)</string>'
            title=re.findall(rgxlable,xml)
            for i in title:
                newt=self.translate(i[1])
                tranxml=tranxml.replace(i[1],newt)
                t.add_row([str(id),i[1],newt])
                id+=1
        print(t)
        self.saveList(tranxml)

    def start(self):
        try:
            url=input('请输入需要翻译的文件路径:')
            rgx=r'[a-zA-Z]+.plist'
            self.filename=re.search(rgx,url).group()
            print(self.filename)
            content=self.readList(url)
            self.tranreplace(content)
        except Exception as e:
            pass

if __name__ == '__main__':
    print('*'*20)
    print('感谢使用')
    print('*'*20)
    tran=Translate()
    tran.start()
