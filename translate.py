import requests,re,execjs,json
def makeExexjs():
    with open('./fanyi.js','r')as f:
        js=f.read()
    return execjs.compile(js)
class TransLate():
    def __init__(self):
        self.sess=requests.session()
        self.sess.headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36x-requested-with: XMLHttpRequest'
        }
        self.sess.get("https://fanyi.baidu.com/?aldtype=16047")
        r=self.sess.get("https://fanyi.baidu.com/?aldtype=16047")
        self.token=re.search(r"token\: '(.+?)',",r.text).group(1)
        # print("token",self.token)
        self.gtk=re.search(r"window\.gtk = '(.+?)'",r.text).group(1)
        # print("gtk",self.gtk)      
        self.Exexcjs=makeExexjs()   
    def landte(self,quary):
        data={'query':quary}    
        respon=self.sess.post("https://fanyi.baidu.com/langdetect",data).json()
        return respon['lan']
    def transapi(self,quary,lang,t_lang):
        fromdata={
            "from": lang,
            "to": t_lang,
            "query":quary,
            "transtype": "realtime",
            "simple_means_flag":"3",
            'sign': self.Exexcjs.call('e',quary,self.gtk),
            "token": self.token,
            "domain": 'common'
        }        
        result=self.sess.post('https://fanyi.baidu.com/v2transapi?from=en&to=zh',data=fromdata)
        print(result.json()['trans_result']['data'][0]['dst']) 
langList_baidu ={
        'zh': '中文', 'jp': '日语', 'jpka': '日语假名', 'th': '泰语', 'fra': '法语', 'en': '英语', 'spa': '西班牙语',
        'kor': '韩语', 'tr': '土耳其语', 'vie': '越南语', 'ms': '马来语', 'de': '德语', 'ru': '俄语', 'ir': '伊朗语',      
}  
def printlist(langList_baidu):
    for index,i in enumerate(langList_baidu):
        print(index,i,langList_baidu[i])
while 1:
    quary=input('请输入文字')
    a=TransLate()
    lang=a.landte(quary)
    print("输入语种为：",lang)
    printlist(langList_baidu)
    t_lang=input("请输入想翻译的语言")
    a.transapi(quary,lang,t_lang)


