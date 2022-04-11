from datetime import datetime
import requests
import json

robot_name = '小奇'

def show_time():
	dt = datetime.now()
	print(dt.strftime('今天是:%Y年%m月%d日 %H:%M:%S'))

def hello(name):
	print('hello world')
	print(f'hello {name},我是{robot_name}\n')

def ai_talk(question):
	return question.replace('你','我').replace('不','').replace('?','!')

def weather(city):
	url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=101100101'
	res = requests.get(url)
	weather_text = res.text
	weather_json = json.loads(weather_text)
	# print(weather_text)
	#loads方法将json数据转换成了dict对象
	#这里的dict对象中forecast是一个list对象，所以需要用[0]来取到list中的第一个dict
	high = weather_json['data']['forecast'][0]['high']
	low = weather_json['data']['forecast'][0]['low']
	print(f'{city}:{high}；{low}')