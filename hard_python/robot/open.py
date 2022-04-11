

def robot():
	#字符串可以用三引号，使用三引号的字符串可以跨行
	print(r'''
      \_/
     (* *)
    __)#(__
   ( )...( )(_)
   || |_| ||//
>==() | | ()/
    _(___)_
   [-]   [-]MJP''')

def ask():
	name = input('你是?\n')
	#input默认输入字符串类型，使用int可以转换成int类型
	age = int(input('请问你多大了?\n'))

	if(age < 30):
		print('你真年轻\n')
	elif(age < 70):
		print('你真成熟\n')
	else:
		print('你真长寿\n')

	return name

def today():
