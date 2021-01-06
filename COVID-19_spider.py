import json
import requests
import jsonpath #解析json数据
import datetime
import pandas as pd

#格式化爬取数据的时间
def sortdate(today):
    list1 = today.split('.')
    today = datetime.date(2020, int(list1[0].replace('0', '')), int(list1[1]))
    return str(today).replace('-','/')

url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
# 获取到各个国家疫情数据
resp = requests.post(url)
# 提取数据,先把json类型转成字典
data = json.loads(resp.text)
country = jsonpath.jsonpath(data, "$..name") #世界各国名字
all_data = {} #存放各国疫情历史数据
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}  
#遍历各国疫情历史数据
for c in country:
    history_url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={0}'.format(c)  
    resp = requests.post(history_url, headers=header)
    data = json.loads(resp.text)['data']
    all_data[c] = data

dates = [] #存放时间列表
for c in all_data['美国']:
    dates.append(sortdate(c['date']))

#对字典all_data中的数据进行修改，只保留累计确诊人数即可
for c in all_data:
    for i in range(len(all_data[c])):
        all_data[c][i] = all_data[c][i]['confirm']

#将字典转化为pandas的DataFrame对象，以便保存
df = pd.DataFrame.from_dict(all_data,orient='index',columns=dates)
df.to_excel('世界各国疫情数据.xlsx')