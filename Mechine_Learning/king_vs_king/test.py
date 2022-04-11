
import numpy as np
from libsvm.python.svm import *
from libsvm.python.svmutil import *
 
def data_read_mat(file_name):
    '''
    从文件中取出数据
    :param file_name: 文件名称
    :return: 返回一个n*7的矩阵，前6项是三个坐标，第七项是标签
    '''
    num_list = []
    '''
    一下是对数据进行读入并且处理，其中open的参数中encoding之所以设置成UTF-8-sig
    是因为如果我们把这个参数设置为UTF-8或者不设置，在读入的开头多出\ufeff这么一串
    东西，有时候会以中文字的形式出现。
    '''
    with open(file_name,"r",encoding='UTF-8-sig') as file:#python读文件
        for l in file:
            l = l.split(',')
            list_k = []
            for j in range(3):
                list_k.append(ord(l[j*2]) - ord('a'))
                list_k.append(ord(l[j*2 + 1]) - ord('0'))
            if(l[6][0] == 'd'):
                list_k.append(-1)
            else:
                list_k.append(1)
            num_list.append(list_k)
    num_mat = np.array(num_list,dtype="float")
    '''
    在此处是以numpy的二维数据矩阵的形式存储的，本以为使用numpy的数据进行运算可以使得
    训练的速度快一些。结果发现如果要往libsvm中的函数传入参数只能传入list型不能传入numpy
    的数据类型。所以，后面又把数据类型转回了list型。但是，我猜应该是有方法可以把numpy
    的数据类型传入使用的。于是我在读取数据后任然返回的是numpy的形式。
    '''
    return num_mat
def data_deal(mat,len_train,len1,len_test,len2):
    '''
    将数据进行处理，分出训练数据和测试数据
    :param mat: 大矩阵，其中包括训练数据和测试数据
    :param len_train:训练数据
    :param len1: 输入坐标
    :param len_test: 测试数据
    :param len2: 标签
    :return: 返回的依次是训练输入数据，测试输入数据，训练输入数据的标签，测试输入数据的标签
    '''
    np.random.shuffle(mat)  #先将矩阵按行打乱。然后根据要求对矩阵进行分割，第一部分就是训练集，第二部分就是测试集
    x_part1 = mat[0:len_train,0:len1]
    x_part2 = mat[len_train:,0:len1]
    y_part1 = mat[0:len_train,len1]
    y_part2 = mat[len_train:,len1]
    # 标准化
    # 根据训练集求出均值和方差
    avgX = np.mean(x_part1)
    stdX = np.std(x_part1)
    # print(avgX,stdX)
    #将训练集和测试集都进行归一化处理
    for data in x_part1:
        for j in range(len(data)):
            data[j] = (data[j] - avgX) / stdX
    for data in x_part2:
        for j in range(len(data)):
            data[j] = (data[j] - avgX) / stdX
    return x_part1,y_part1,x_part2,y_part2
def TrainModel(CScale,gammaScale,prob):
    '''
    :param CScale: 参数C的取值序列
    :param gammaScale:  参数γ的取值序列
    :param prob: 训练集合对应的标签
    :return: maxACC（最高正确率）,maxACC_C（最优参数C）,maxACC_gamma（最优参数γ）
    '''
    maxACC = 0
    maxACC_C = 0
    maxACC_gamma = 0
 
    for C in CScale:
        C_ = pow(2, C)
        for gamma in gammaScale:
            gamma_ = pow(2, gamma)
            # 设置训练的参数
            # 其中-v 5表示的是2折交叉验证
            # “-q”可以去掉这样也就可以看到训练过程
            param = svm_parameter('-t 2 -c ' + str(C_) + ' -g ' + str(gamma_) + ' -v 5 -q')
            ACC = svm_train(prob, param)  # 进行训练，但是传回的不是训练模型而是5折交叉验证的准确率
            #更新数据
            if (ACC > maxACC):
                maxACC = ACC
                maxACC_C = C
                maxACC_gamma = gamma
    return maxACC,maxACC_C,maxACC_gamma
def getNewList(L,U,step):
    l = []
    while(L < U):
        l.append(L)
        L += step
    return l
def TrainModelSVM(data,label,iter,model_file):
    '''
    模型训练并保存
    :param data: 数据
    :param label: 标签
    :param iter:训练次数，在原先的MATLAB代码中的次数是两次
    :param model_file:模型的保存位置
    :return: 返回最优参数
    '''
    #将数据转换成list型的数据。因为，在svm的函数中好像只能传入list型的数据进行训练使用
    X = data.tolist()
    Y = label.tolist()
    CScale = [-5, -3, -1, 1, 3, 5,7,9,11,13,15]  #参数C的2^C
    gammaScale = [-15,-13,-11,-9,-7,-5,-3,-1,1,3] #参数γ的取值2^γ
    cnt = iter
    step = 2 #用于重新生成CScale和gammaScale序列
    maxACC = 0 #训练过程中的最大正确率
    bestACC_C = 0 #训练过程中的最优参数C
    bestACC_gamma = 0 #训练过程中的最优参数γ
    prob = svm_problem(Y, X)  # 传入数据
    while(cnt):
        #用传入的参数序列进行训练，返回的是此次训练的最高正确率，最优参数C，最优参数γ
        maxACC_train,maxACC_C_train,maxACC_gamma_train = TrainModel(CScale,gammaScale,prob)
        #数据更新
        if(maxACC_train > maxACC):
            maxACC = maxACC_train
            bestACC_C = maxACC_C_train
            bestACC_gamma = maxACC_gamma_train
        #根据返回的参数重新生成CScale序列和gammaScale序列用于再次训练，下一次训练的C参数和γ参数的精度会比之前更高
        #step就是CScale序列和gammaScale序列的相邻两个数之间的间隔
        new_step = step*2/10
        CScale = getNewList(maxACC_C_train - step,maxACC_C_train + step + new_step,new_step)
        gammaScale = getNewList(maxACC_gamma_train - step,maxACC_gamma_train + step + new_step,new_step)
        cnt -= 1
    #获得最优参数后计算出对应的C和γ，并且训练获得“最优模型”
    C = pow(2,bestACC_C)
    gamma = pow(2,bestACC_gamma)
    param = svm_parameter('-t 2 -c ' + str(C) + ' -g ' + str(gamma))
    model = svm_train(prob, param)  # 交叉验证准确率
    svm_save_model(model_file, model) #保存模型
    return model



def main():
    data_file = r"F:\study\python\Mechine_Learning\king_vs_king\krkopt.data"  #数据存放的位置（需要修改）
    mode_file = r"F:\study\python\Mechine_Learning\king_vs_king"   #训练模型保存的位置（需要修改）
    data_mat = data_read_mat(data_file)  #从文件中读取数据并处理
    #以下是对数据训练进行分配，可以根据你的需要进行调整
    train = 5000   #5000组数据作为训练数据
    test  = len(data_mat) - 5000  #剩下的数据作为测试数据
    #————————————————————————————————————————————————————————————#
    x_len = 6   #输入数据的维度是6维，即三个棋子的坐标
    y_len = len(data_mat[0]) - x_len  #输出的数据时1维，即两种结果
    iter = 2# 训练的次数，训练的次数越多参数就调整的精度就越高
    x_train,y_train,x_test,y_test = data_deal(data_mat,train,x_len,test,y_len) #对数据进行分割
    if (input("是否需要进行训练？") == 'y'):  #如果输入y就会进行训练，否则就可以直接使用之前训练的完成的模型
        model = TrainModelSVM(x_train,y_train,iter,mode_file)  #传入输入数据，标签进行模型的训练
    else:
        model = svm_load_model(mode_file)  #直接加载现有模型
    X = x_test.tolist() #将测试集的输入集转换成list
    Y = y_test.tolist() #将测试集的输出集转换成list
    print(Y[:10])
    p_labs,p_acc,p_vals = svm_predict(Y,X,model)
 
 
if __name__ == "__main__":
    main()