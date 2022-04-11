import random
import time
import sys
from guess_level1 import *


guess_limit = input_limit()

score = [] #记录结果
best_score = None

cycle = 0;#第几轮
while(True):
	cycle +=1
	#在1到10之间随机选取一个数(包括10)
	answer = random.randint(1,10)
	is_right = False
	start_time = time.time()
	for i in range(guess_limit):
		try:
			guess = int(input('请猜一个1到10之间的数字\n'))
		except ValueError:
			print('请输入数字')
			continue
		if(answer == guess):
			is_right = True
			break
		elif(answer > guess):
			print('太小了',end = ' ')
		elif(answer < guess):
			print('太大了',end = ' ')	
		if(i == guess_limit-1):
			pass
		else:
			print('请继续猜')

	if(is_right):
		print('恭喜你，猜对了')
		flag = '成功'
	else:
		print('你已经耗尽了次数')
		flag = '失败'

	use_time = process_time(start_time)
	#记录结果
	score.append((cycle,flag,use_time))
	if(is_right):
		best_score = min(score,key=lambda x:x[2] if x[1]=='成功' else 99999)

	con = input('请问还继续吗？Y/N\n')
	if(con != 'Y' and con != 'y'):
		print('再见')
		break

print('-----游戏结果-----')
print_score(score,best_score)
