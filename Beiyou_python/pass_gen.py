import random
import string
import argparse

    #todo:判断密码是否合格
def evaluate_password(password,show_info=True):   #python的命名空间隔离了全局变量与函数的局部变量
    result = False
    pass_state = 0b00000    #状态字，每位表示一个条件

    for char in password:
        if char.isupper():
            pass_state |= 0b10000   # | 表示按位进行或运算，有1为1，全0为0
        elif char.islower():
            pass_state |= 0b01000
        elif char.isdigit():
            pass_state |= 0b00100
        else:
            pass_state |= 0b00010

    if len(password)>=8:
        pass_state |= 0b00001

    #todo：输出
    if(pass_state == 0b11111):
        if show_info:
            print('密码符合要求')
        result = True
    else:
        if show_info:
            prompt = '密码不符合要求,'
            if not pass_state & 0b00001 == 0b00001:
                prompt += '长度不足8,'
            if not pass_state & 0b10000 == 0b10000:
                prompt += '没有包含大写,'
            if not pass_state & 0b01000 == 0b01000:
                prompt += '没有包含小写字母,'
            if not pass_state & 0b00100 == 0b00100:
                prompt += '没有包含数字,'
            if not pass_state & 0b00010 == 0b00010:
                prompt += '没有包含字符,'
            prompt = prompt[:-1]
            print(prompt)
    return result
        
'''
    pass_length表示需要的密码长度
'''
def create_password(pass_length, confuse=False):
    result = ''
    #先生成包含四种字符的密码前四位
    result += random.choice(string.ascii_uppercase)
    result += random.choice(string.ascii_lowercase)
    result += random.choice(string.digits)
    result += random.choice(string.punctuation)
    if confuse:
        result += 'Il'
        result += ''.join(random.sample(string.printable[:-6]*pass_length, pass_length-6))
    else:
        result += ''.join(random.sample(string.printable[:-6]*pass_length, pass_length-4))
    #对密码中的字符打乱顺序
    #random.shuffle(result) shuffle只支持对可变对象改变顺序
    result = ''.join(random.sample(result,len(result)))
    return result

def gen_password():
    all_char_set = string.printable[:-6]
    all_char_set *= 9 #表示将9个all_char_set连接在一起，每个字符都出现了9次
    result = ''.join(random.sample(all_char_set,k=9))
    return result

def main_userinputy():
    while 1:
        #todo:用户输入密码
        user_password = input("请输入密码:")
        if evaluate_password(user_password):    #函数先定义再使用
            break

def main_genpassword():
    while 1:
        user_password = gen_password()
        print(f"密码是{user_password}")
        if evaluate_password(user_password,show_info=False):    #函数先定义再使用
            break

def main():
    parser = argparse.ArgumentParser(description="Generate new password.")  #使用命令行传参数
    parser.add_argument('-l','--length',type=int, default=9, help='length of password')
    parser.add_argument('-c','--confuse',action='store_true', help='use confuse characters')
    args = parser.parse_args()

    print(f"新生成的密码为:{create_password(args.length,args.confuse)}")

main()