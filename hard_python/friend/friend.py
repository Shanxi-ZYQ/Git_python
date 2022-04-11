from cmd.friend_list import show_list, find


def print_usage():
    print('欢迎使用friendBook，你可以输入以下命令:')
    print('List:显示名单')
    print('张三:查询张三')
    print('886:推出')


print_usage()


while(True):
    cmd = input('请输入命令')
    if(cmd == '886'):
        print('再见')
        break
    elif(cmd == 'List'):
        show_list()
    else:
        find(cmd)