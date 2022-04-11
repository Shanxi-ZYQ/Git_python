import sys
import time

def input_limit():
	try:
		limit = int(sys.argv[1])
	except:
		limit = 3
		print('输入错误使用默认值3')
	return limit

def process_time(start_time):
	end_time = time.time()
	use_time = round(end_time-start_time,2)
	print(f'本次游戏共使用了{use_time}秒')
	return use_time

def print_score(score,best_score):
	for c,r,t in score:
		print(f'第{c}轮，游戏结果：{r}，游戏用时：{t}秒')
	print('-----最佳成绩-----')
	if(best_score != None):
		print(f'第{best_score[0]}轮，游戏结果：{best_score[1]}，游戏用时：{best_score[2]}秒')
	else:
		print('无')
