from guess_level2 import *
import time

cycle_count = 0 #记录游戏局数
next_cycle = True
scores = []#保存每轮结果
while(next_cycle):
	cycle_count += 1
	begin_time = time.time()
	#玩一轮
	answer = generate_answer()
	win = False
	guess_count = 0
	while(not win):
		try:
			guess = make_guess()#猜测

			result = check_guess(answer,guess)#核对
			guess_count += 1
			win = process_result(guess_count,guess,result)#处理结果
			if(win):
				end_time = time.time()
				used_time = int(end_time - begin_time)
				scores.append((cycle_count,guess_count,used_time))
		except ValueError:
			print('输入错误')
		except IndexError:
			print('请输入四位数字')

	#要不要继续
	next_cycle = should_continue()

show_scores(scores)#显示结果