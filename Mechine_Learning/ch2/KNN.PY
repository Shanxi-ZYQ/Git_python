from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    #距离计算
    dataSetSize = dataSet.shape[0]
    # tile函数作用是按照某个方向复制元素，第一个参数是行，第二个参数是列
    # 这里在行方向复了inX向量dataSetSize次，在列方向复制了1次
    diffMat = tile(inX, (dataSetSize,1)) - dataSet  #计算目标点向量差值
    #对向量中每个数据求平方
    sqDiffMat = diffMat**2                          #差值做平方
    sqDistances = sqDiffMat.sum(axis=1)             #求和
    distances = sqDistances**0.5                    #开方

    #返回distances中元素从小到大排序后的索引值
    sortedDistIndicies = distances.argsort()
    classCount = {}
    #选择距离最小的k个点
    for i in range(k):
        #取出前k个元素的类别
        voteIlabel = labels[sortedDistIndicies[i]]
        #计算类别出现次数，get()方法返回指定键的值，如果值不在字典中返回默认值
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    
    #排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0] [0]

#解析文本记录
def file2matrix(filename):
    #打开文件
    fr = open(filename)
    #读取文件所有内容
    arrayOLines = fr.readlines()
    #得到文件行数
    numberOfLines = len(arrayOLines)
    #返回Numpy矩阵，有numberOfLine行，3列
    returnMat = zeros((numberOfLines,3))
    #返回分类标签向量
    classLabelVector = []
    #行索引
    index = 0
    for line in arrayOLines:
        #对每行数据进行格式化，strip(rm)方法，当rm为空时，默认删除空白
        line = line.strip()
        #使用split()将字符串进行切片
        listFromLine = line.split('\t')
        #取出数据的前三列，放入NumPy矩阵中
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector