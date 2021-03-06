import tkinter
import re,os
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
        sign = sign = hashlib.md5(("fanyideskweb" + content + salt +
                                   "ebSeFb%=XZ%T[KZ)c(sy!").encode('utf-8')).hexdigest()  # 22222
        # 表单数据
        data = {
            "i": content,
            "from": "AUTO",
            "to": 'AUTO',
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTIME",
            "typoResult": "false",
        }
                # 请求头
        head = {
        }
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
        head[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        head['X-Requested-With'] = 'XMLHttpRequest'
        request = requests.request('POST',url,data=data,headers=head)
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
        uri=os.path.dirname(os.path.realpath(__file__))
        folder=os.path.exists(uri+'/tran')
        if not folder:
            os.makedirs(uri+'/tran')
        with open(uri+'/tran/'+self.filename,'w') as f:
            f.write(content)
        f.close()
    #遍历所有需要翻译的内容
    def tranreplace(self,content):

        '''
        遍历需要翻译的内容
        :param xml:
        :return:
        '''
        tranxml=content
        t=PrettyTable(["id","译前","译后"])
        id=1
        for item in self.keylist:
            rgxlable=r'<key>'+item+'</key>[^.](.*?)<string>(.*?)</string>'
            title=re.findall(rgxlable,content)
            for i in title:
                print('需要翻译的内容:',i[1])
                if i[1]!='':
                    try:
                        newt=self.translate(i[1])
                        newt=newt.replace('&','')
                        newt=newt.replace('#','')
                        tranxml=tranxml.replace(i[1],newt)
                        t.add_row([str(id),i[1],newt])
                        id+=1
                        print(i[1],'----',newt)
                    except:
                        pass

        print(t)
        self.saveList(tranxml)

    def start(self):
        url=input('请输入需要翻译的文件路径:').strip()
        rgx=r'[a-zA-Z0-9]+.plist'
        self.filename=re.search(rgx,url)
        if self.filename:
            self.filename=self.filename.group()
            content=self.readList(url)

            print(content)
            try:
                self.tranreplace(content)
            except:
                pass
        else:
            if url[-1:]!='/':
                url=r=url+'/'
            files = os.listdir(url)

            for i in files:
                self.filename=re.search(rgx,i)
                if  self.filename:
                    self.filename=self.filename.group()
                    content=self.readList(url+self.filename)
                    self.tranreplace(content)

if __name__ == '__main__':
    print('*'*20)
    print('主要分享越狱插件美化等，还有自己开源的一些工具，还有一些实用的教程，本来自己留作备份，现免费分享出来')
    print('*'*20)
    tran=Translate()
    tran.start()
    print('*'*20)
    print('翻译结束，请前往程序目录线tran查看翻译结果')
    print('如有问题可添加我的微信公众号:千寻论，在里面回复问题，免费解答。')
    print('*'*20)

