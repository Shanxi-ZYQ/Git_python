#python引入文件
import open
import order
import time

#出场
open.robot()

#提问
name = open.ask()

while(True):
	print(f'{name},有什么吩咐')
	cmd = input()
	if(cmd == 'time'):
		order.show_time()
	elif(cmd == 'hello'):
		order.hello(name)
	elif(cmd == '88'):
		print('再见，有需要随时叫我')
		time.sleep(1)
		break
	elif(cmd == '天气'):
		order.weather('太原')
	else:
		print(order.ai_talk(cmd))	
	print('----------')