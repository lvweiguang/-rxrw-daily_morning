import requests
import json
import datetime
import time
#from bs4 import BeautifulSoup
#from zhdate import ZhDate
 
class SendMessage():                                                 #定义发送消息的类
    def __init__(self):                                          
        date = self.get_date()                                       #获取当前日期
  #      weather = self.get_weather()                                 #获取天气信息
        lovedate = self.get_loveday()                                #获取纪念日
        herbirthday = self.get_herbirthday()                         #获取npy生日
        mybirthday = self.get_mybirthday()                           #获取自己生日
        body =lovedate+"\n"+herbirthday+mybirthday                   
        self.dataJson ={"frist":"早上好bb！❤\n",                     #最终要发送的json
                        "date":date+'\n',
                        "body":body+" ",
                        "weather":weather+'\n城市：昆明'+'\n',        #因为还没写获取地理位置的所以城市暂时写死 后续将会改为获取当前位置并爬取对应城市的天气信息版本
                        "last":'\n今天也是爱bb🐖的一天捏！！！'      
                        }
        self.appID = 'wx9f7ff34b6704c03a'                             #appid 注册时有
        self.appsecret = '709db6067db578d616e5890a719c50f0'           #appsecret 同上
        self.template_id = 'klxUXN2aviwEwpJJSFcQSF3RDcxBXYr8dgrOgSKk4Sc'  # 模板id
        self.access_token = self.get_access_token()                   #获取 access token
        self.opend_ids = self.get_openid()                            #获取关注用户的openid
 
 
 
 

    def get_date(self):
        """
        这些都是datetime库中的用法
        若零基础可以去python的开发文档中查阅
        """
        sysdate = datetime.date.today()                 # 只获取日期
        now_time = datetime.datetime.now()              # 获取日期加时间
        week_day = sysdate.isoweekday()                 # 获取周几
        week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
        return '现在是' + str(now_time)[0:16] + ' ' + week[week_day - 1]
 
    def get_herbirthday(self):
        """
        获取npy生日 这里还用到了农历时间库
        可以去网上查阅 ZhDate库 其他基本上是datetime中的一些获取当前日期和toordinal
        没什么特别难的
        """
        today = datetime.datetime.now()                               #获取现在时间信息
        data_str = today.strftime('%Y-%m-%d')
        herbirthDay = datetime.datetime(today.year,12,7)          #将农历1.18号的时间转换为公历时间再转换为datetime类型的时间
        if herbirthDay >today :                                        #如果ta的生日日期比今天靠后则直接计算这两天的序号之差
            difference = herbirthDay.toordinal() - today.toordinal()
            return ("\n距离熊又又生日,还有 %d 天。" % (difference))
        elif herbirthDay <today:                                       #如果ta的生日日期比今天靠前则给ta的生日加上一年再计算这两天的序号之差
            herbirthDay = herbirthDay.replace(today.year+1)
            difference = herbirthDay.toordinal() - today.toordinal()
            return ("\n距离熊又又生日,还有 %d 天。" % (difference))
        else:
            return ('生日快乐bb！！')
    def get_mybirthday(self):
        """
            同上
        """
        today = datetime.datetime.now()
        data_str = today.strftime('%Y-%m-%d')
        mybirthDay = datetime.datetime(today.year,12,7)
        if mybirthDay >today :
            difference = mybirthDay.toordinal() - today.toordinal()
            return ("\n距离刘壮壮生日,还有 %d 天。" % (difference))
        elif mybirthDay <today:
            mybirthDay = mybirthDay.replace(today.year+1)
            difference = mybirthDay.toordinal() - today.toordinal()
            return ("\n距离刘壮壮生日,还有 %d 天。" % (difference))
        else:
            return ('祝我生日快乐！！')
 
    def get_loveday(self):
        """用法同上"""
        today = datetime.datetime.now()
        data_str = today.strftime('%Y-%m-%d')
        oneDay = datetime.date(2022, 4, 4)
        d =  today.toordinal()-oneDay.toordinal()
        return ("我们已经相爱 %d 天。\n%d 年 %d 个月 %d 天。\n%d 个月 %d 天。\n%d 周 %d 天。" % (d,d // 365, (d % 365) // 30, (d % 365) % 30, d // 30, d % 30, d // 7, d % 7))
 
    def get_access_token(self):
        """
        获取access_token
        通过查阅微信公众号的开发说明就清晰明了了
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.\
            format(self.appID, self.appsecret)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        return access_token
 
    def get_openid(self):
        """
        获取所有用户的openid
        微信公众号开发文档中可以查阅获取openid的方法
        """
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (self.access_token, next_openid)
        ans = requests.get(url_openid)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids
 
    def sendmsg(self):  
        """
        给所有用户发送消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(self.access_token)
 
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                        "touser": open_id,
                        "template_id": self.template_id,
                        "url": "https://www.baidu.com/",
                        "topcolor": "#FF0000",
                         #对应模板中的数据模板
                        "data": {
                            "frist": {
                                "value": self.dataJson.get("frist"),               
                                "color": "#FF99CC"                                  #文字颜色
                            },
                            "body": {
                                "value": self.dataJson.get("body"),
                                "color": "#EA0000"
                            },
                   
                            "date": {
                                "value": self.dataJson.get("date"),
                                "color": "#6F00D2"
                            },
                            "last": {
                                "value": self.dataJson.get("last"),
                                "color": "#66CCFF"
                            }
                        }
                    }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))  #将数据编码json并转换为bytes型
                response = requests.post(url, data=data)                    
                result = response.json()                                            #将返回信息json解码
                print(result)                                                       # 根据response查看是否广播成功
        else:
            print("当前没有用户关注该公众号！")
 
if __name__ == "__main__":
    sends = SendMessage()
    sends.sendmsg()
