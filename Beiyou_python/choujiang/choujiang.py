import random
import time

def chou_1(u_list):
    selected_user_info = random.choice(u_list).split()
    print(f"恭喜用户{selected_user_info[1]}中奖，学号{selected_user_info[0]}")
    return selected_user_info[0]

def chou_2(u_list):
    while 1:
        try:
            idx = int(time.time()*1000) % len(u_list)
            print(f'\r{u_list[idx]}',end='')
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
    selected_user_info = u_list[idx].split('\t')
    print(f"恭喜用户{selected_user_info[1]}中奖，学号{selected_user_info[0]}")
    return selected_user_info[0]

def chou_3(u_list):
    while 1:
        rand_x = random.randint(0,10000) / 10
        rand_y = random.randint(0,10000) / 10
        try:
            print(f'\r{rand_x},{rand_y}',end='')
            time.sleep(0.01)
        except KeyboardInterrupt:
            break

    user_distance_list = []
    for user_info in u_list:
        uid,uname,ux,uy =  user_info.split('\t')
        distance = int((int(ux) - rand_x) ** 2 + (int(uy) - rand_y) ** 2) #计算距离
        user_distance_list.append((uid, uname, distance))

    user_distance_list.sort(key=lambda x:x[2]) #lambda是在行内定义的函数，冒号前为参数冒号后是函数代码,这里将list的一个元素作为x传入lembda
    print(f"恭喜用户{user_distance_list[0][1]}中奖，学号{user_distance_list[0][0]}")
    # print(f"\r{user_distance_list}")

def main():
    with open('user.txt',encoding='utf-8') as f:
        content = f.read()
    
    user_list = content.split("\n") #用指定的分隔符将数据分开
    
    chou_1(user_list)
    chou_2(user_list)
    chou_3(user_list)


main()