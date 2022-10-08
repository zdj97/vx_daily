from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from bs4 import BeautifulSoup

today = datetime.now ()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
print(app_id)
app_secret = os.environ["APP_SECRET"]
# city_code = os.environ["CITY_CODE"]
city_code='101100201'
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
# city_code = '101230508'  # 进入https://where.heweather.com/index.html查询你的城市代码
api = 'http://t.weather.itboy.net/api/weather/city/'  # API地址，必须配合城市代码使用



def get_iciba_everyday ():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get (icbapi)
    bee = eed.json ()  # 返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = '【奇怪的知识】\n' + english + '\n' + zh_CN
    return str

def getloverwords ():
    texts = []
    for i in range (1, int (random.randint (3, 83))):
        url = 'https://www.duanwenxue.com/huayu/tianyanmiyu/list_{}.html'.format (i)
        response = requests.get (url,proxies={'http':None,'https':None})
        texts.append (response.text)
    articles = []
    for text in texts:
        soup = BeautifulSoup (text, 'lxml')
        arttis = soup.find ('div', class_ = 'list-short-article').find_all ('a', {'target': "_blank"})  # 寻找情话内容
        #  通过列表推导式以及for循环获取到每个a标签里面的text内容并通过strip去除空格
        articles.extend ([arttis[i].text.strip () for i in range (len (arttis))])
    todaywords = articles[random.randint (0, len (articles) - 1)]  # 随机选取其中一条情话
    return todaywords


def get_weather_new ():
    tqurl = api + city_code
    response = requests.get (tqurl)
    d = response.json ()  # 将数据以json形式返回，这个d就是返回的json数据
    # print(d)
    if (d['status'] == 200):  # 当返回状态码为200，输出天气状况
        parent = d["cityInfo"]["parent"]  # 省
        city = d["cityInfo"]["city"]  # 市
        update_time = d["time"]  # 更新时间
        date = d["data"]["forecast"][0]["ymd"]  # 日期
        week = d["data"]["forecast"][0]["week"]  # 星期
        weather_type = d["data"]["forecast"][0]["type"]  # 天气
        wendu_high = d["data"]["forecast"][0]["high"]  # 最高温度
        wendu_low = d["data"]["forecast"][0]["low"]  # 最低温度
        shidu = d["data"]["shidu"]  # 湿度
        pm25 = str (d["data"]["pm25"])  # PM2.5
        pm10 = str (d["data"]["pm10"])  # PM10
        quality = d["data"]["quality"]  # 天气质量
        fx = d["data"]["forecast"][0]["fx"]  # 风向
        fl = d["data"]["forecast"][0]["fl"]  # 风力
        ganmao = d["data"]["ganmao"]  # 感冒指数
        tips = d["data"]["forecast"][0]["notice"]  # 温馨提示
        # cpurl = 'https://qmsg.zendee.cn/send/' + spkey  # 自己改发送方式，我专门创建了个群来收消息，所以我用的group
        # 天气提示内容
        tdwt = get_iciba_everyday () + "\n-----------------------------------------" + "\n❤【今日份天气】\n❤城市： " + parent + city + \
               "\n❤日期： " + date + "\n❤星期: " + week + "\n❤天气: " + weather_type + "\n❤温度: " + wendu_high + " / " + wendu_low + "\n❤湿度: " + \
               shidu + "\n❤PM25: " + pm25 + "\n❤PM10: " + pm10 + "\n❤空气质量: " + quality + \
               "\n❤风力风向: " + fx + fl + "\n❤感冒指数: " + ganmao + "\n❤温馨提示： " + tips + "\n❤更新时间: " + update_time
        print (tdwt)
        #data = {
        #   'msg': tdwt.encode ('utf-8')
        #}
        # requests.post (cpurl, data = data)  # 把天气数据转换成UTF-8格式，不然要报错。
    return parent, city, date, week, weather_type, shidu,pm25, pm10, quality, fx, fl, ganmao, tips, update_time


def get_weather ():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get (url).json ()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor (weather['temp'])


def get_count ():
    delta = today - datetime.strptime (start_date, "%Y-%m-%d")
    return delta.days


def get_birthday ():
    next = datetime.strptime (str (date.today ().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now ():
        next = next.replace (year = next.year + 1)
    return (next - today).days


def get_words ():
    words = requests.get ("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words ()
    return words.json ()['data']['text']



def get_random_color ():
    return "#%06x" % random.randint (0, 0xFFFFFF)


client = WeChatClient (app_id, app_secret)

wm = WeChatMessage (client)
# wea, temperature = get_weather ()
# data = {"weather": {"value": wea}, "temperature": {"value": temperature}, "love_days": {"value": get_count ()},
#         "birthday_left": {"value": get_birthday ()}, "words": {"value": get_words (), "color": get_random_color ()}}

parent, city, date, week, weather_type, shidu,pm25, pm10, quality, fx, fl, ganmao, tips, update_time=get_weather_new()
loveword=get_words()
data={'parent':{'value':parent},'city':{'value':city},'date':{'value':date},'week':{'value':week},'weather_type':{'value':weather_type},'shidu':{'value':shidu},'pm25':{'value':pm25},'pm10':{'value':pm10},'quality':{'value':quality},'fx':{'value':fx},'fl':{'value':fl},'ganmao':{'value':ganmao},'tips':{'value':tips},'update_time':{'value':update_time},'loveword':{'value':loveword}}
res = wm.send_template (user_id, template_id, data)
print (res)
