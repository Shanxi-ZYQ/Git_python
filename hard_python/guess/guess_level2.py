import random


def generate_answer():#产生一个四位数答案
	# return random.randint(1000,9999)
	return 9527

def make_guess():#猜测
	return int(input('请输入你的答案'))

# def check_guess(answer,guess):#核对
# 	# a_number = check_guess_a(answer,guess)
# 	count = check_guess_b(answer,guess)
# 	a_number = count[0]
# 	b_number = count[1]
# 	return f'{a_number}A{b_number}B'

#返回数字和位置都正确的数字的个数
# def check_guess_a(answer,guess):
# 	count = 0
# 	answer_str = str(answer)
# 	guess_str = str(guess)
# 	for index, char in enumerate(answer_str):
# 		if(guess_str[index] == char):
# 			count += 1
# 	return count

#A表示位置和数字都正确的数位个数，B表示数字正确位置不正确的数位个数，取A则不在记入B
def check_guess(answer,guess):#核对答案
	count = 0
	answer_str = str(answer)
	guess_str = str(guess)
	a_count = 0
	b_count = 0

	a_index = []
	for index, char in enumerate(answer_str):
		if(guess_str[index] == char):
			a_index.append(index)
			a_count +=1

	for char in guess_str:
		if (char in answer_str and answer_str.index(char) not in a_index):
			b_count +=1
	return f'{a_count}A{b_count}B'

def process_result(guess_count,guess,result):#处理结果
	if(result == '4A0B'):
		print(f'{result} 恭喜你，成功了')
		return True
	else:
		print(f'{result} 猜错了')
	return False

def should_continue():#是否继续
	con = input('是否继续？Y/N')
	if(con == 'y' or con == 'Y'):
		return True
	else:
		print('再见')
	return False

def show_scores(scores):#显示结果
	print('----游戏结果----')
	for sc in scores:
		print(f'第{sc[0]}轮,猜测{sc[1]}次,用时{sc[2]}秒')

if __name__ == '__main__':
	assert(check_guess_a(9999,8899) == 2)
	assert(check_guess_b(9977,8899) == 2)