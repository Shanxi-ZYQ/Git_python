import matplotlib.pyplot as plt
import numpy as np

"""
    加载数据集testSet.txt
"""
def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    fr.close()
    return dataMat,labelMat



"""
    sigmoid函数
    参数:
        inX-数据
    返回值:
        sigmoid函数
"""
def sigmoid(inX):
    return 1.0/(1+ np.exp(-inX))

"""
    梯度上升算法
    参数:
        dataMatIn - 数据集
        classLabels - 数据标签
    返回值:
        weights.getA() - 求得的权重数组
"""
def gradAscent(dataMatIn,classLabels):
    dataMatrix = np.mat(dataMatIn)  #转换成numpy的mat
    labelMat = np.mat(classLabels).transpose()  #进行转置运算
    m,n=np.shape(dataMatrix)    #返回dataMatrix的大小，m为行数，n为列数
    alpha = 0.001   #步长
    maxCycles = 500 #迭代步数
    weights = np.ones((n,1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)   #梯度上升矢量化公式
        error = labelMat - h
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights.getA()


"""
    根据梯度上升结果,绘制决策边界
"""


def plotDataSet(weights):
    dataMat, labelMat = loadDataSet()  # 加载数据集
    dataArr = np.array(dataMat)  # 转换成numpy数组
    n = np.shape(dataMat)[0]  # 数据的个数
    xcord1 = []
    ycord1 = []  # 正样本
    xcord2 = []
    ycord2 = []  # 负样本
    for i in range(n):
        if int(labelMat[i]) == 1:  # 如果是正样本
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=20, c='red', marker='s', alpha=.5)  # 绘制正样本
    ax.scatter(xcord2, ycord2, s=20, c='green', alpha=.5)  # 绘制负样本
    x = np.arange(-3.0,3.0,0.1)
    y = (-weights[0] - weights[1] * x)/weights[2]
    ax.plot(x,y)
    plt.title('BestFit')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


if __name__ == '__main__':
    dataMat,labelMat = loadDataSet()
    weights = gradAscent(dataMat,labelMat)
    plotDataSet(weights)