from math import log

"""
    数据集
"""


def createDataSet():
    dataSet = [
        [0, 0, 0, 0, 'no'],
        [0, 0, 0, 1, 'no'],
        [0, 1, 0, 1, 'yes'],
        [0, 1, 1, 0, 'yes'],
        [0, 0, 0, 0, 'no'],
        [1, 0, 0, 0, 'no'],
        [1, 0, 0, 1, 'no'],
        [1, 1, 1, 1, 'yes'],
        [1, 0, 1, 2, 'yes'],
        [1, 0, 1, 2, 'yes'],
        [2, 0, 1, 2, 'yes'],
        [2, 0, 1, 1, 'yes'],
        [2, 1, 0, 1, 'yes'],
        [2, 1, 0, 2, 'yes'],
        [2, 0, 0, 0, 'no']
    ]
    labels = ['年龄','有工作','有自己的房子','信贷情况']
    return dataSet,labels


"""
    函数功能:计算经验熵
    参数:
        数据集
    返回值:
        经验熵
"""


def calcShannonEnt(dataSet):
    numEntires = len(dataSet)  # 返回数据集行数
    labelCounts = {}  # 保存每个标签(label)的出现次数的字典
    for featVec in dataSet:  # 对每组特征向量进行统计
        currentLabel = featVec[-1]  # 提取标签(label)信息
        if currentLabel not in labelCounts.keys():  # 如果标签(label)没有放入统计次数的字典,添加进去
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1  # Label计数
    shannonEnt = 0.0  # 经验熵
    for key in labelCounts:  # 计算经验熵
        prob = float(labelCounts[key])/numEntires  # 选择该标签的概率 p
        shannonEnt -= prob * log(prob, 2)  # 利用公式计算熵,-Σ p*logp
    return shannonEnt

"""
    按照给定特征划分数据集
    参数:
        dataSet-待划分的数据集
        axis-划分数据集的特征
        value-需要返回的特征值
"""
def splitDataSet(dataSet,axis,value):
    retDataSet = [] #创建返回的数据集列表
    for featVec in dataSet: #遍历数据集
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis] #去掉axis特征
            reducedFeatVec.extend(featVec[axis+1:]) #将符合条件的添加到返回的数据集
            retDataSet.append(reducedFeatVec)
    return retDataSet


"""
    选择最优特征
    参数:
        dataSet - 数据集
    返回值:
        bestFeature - 最优特征,信息增益最大的特征
"""
def chooseBsetFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1 #特征数量
    baseEntropy = calcShannonEnt(dataSet)   #计算数据集的经验熵
    bestInfoGain = 0.0  #信息增益
    bestfeature = -1    #最优特征索引值
    for i in range(numFeatures):    #遍历所有特征
        featList = [example[i] for example in dataSet]  #获取dataSet的第i个所有特征
        uniqueVals = set(featList)  #创建set集合
        newEntropy = 0.0    #经验条件熵
        for value in uniqueVals:    #计算信息增益
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/ float(len(dataSet)) #计算划分后的子集的概率,条件概率
            newEntropy += prob*calcShannonEnt(subDataSet) #计算经验条件熵
        infoGain = baseEntropy - newEntropy #信息增益
        print("第%d个特征的信息增益为%.3f"%(i,infoGain))
        if(infoGain > bestInfoGain):    #选择最优特征
            bestInfoGain = infoGain
            bestfeature = i
    return bestfeature

if __name__ == '__main__':
    dataSet,features = createDataSet()
    print("最优特征索引值:"+str(chooseBsetFeatureToSplit(dataSet)))