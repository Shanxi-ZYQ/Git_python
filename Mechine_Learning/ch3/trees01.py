import pickle
from math import log
import operator

"""
    计算经验熵
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
    测试数据集
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
    按给定特征划分数据集
"""


def splitDataSet(dataSet, axis, value):
    retDataSet = []  # 创建返回的数据集列表
    for featVec in dataSet:  # 遍历数据集
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]  # 去掉axis特征
            reducedFeatVec.extend(featVec[axis+1:])  # 将符合条件的添加到返回的数据集
            retDataSet.append(reducedFeatVec)
    return retDataSet

"""
    选择最优特征
"""


def chooseBsetFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1  # 特征数量
    baseEntropy = calcShannonEnt(dataSet)  # 计算数据集的经验熵
    bestInfoGain = 0.0  # 信息增益
    bestfeature = -1  # 最优特征索引值
    for i in range(numFeatures):  # 遍历所有特征
        featList = [example[i] for example in dataSet]  # 获取dataSet的第i个所有特征
        uniqueVals = set(featList)  # 创建set集合
        newEntropy = 0.0  # 经验条件熵
        for value in uniqueVals:  # 计算信息增益
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))  # 计算划分后的子集的概率,条件概率
            newEntropy += prob*calcShannonEnt(subDataSet)  # 计算经验条件熵
        infoGain = baseEntropy - newEntropy  # 信息增益
        print("第%d个特征的信息增益为%.3f" % (i, infoGain))
        if(infoGain > bestInfoGain):  # 选择最优特征
            bestInfoGain = infoGain
            bestfeature = i
    return bestfeature


"""
    统计classList中出现最多的元素
"""
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]

"""
    创建决策树
    参数:
        dataSet-训练数据集
        labels-分类属性标签
        featLabels-存储选择的最优特征标签
    返回值:
        myTree-决策树
"""
def createTree(dataSet,labels,featLabels):
    classList = [example[-1] for example in dataSet] #取分类标签
    if classList.count(classList[0]) == len(classList): #如果类别完全相同则停止继续划分
        return classList[0]
    if len(dataSet[0]) == 1:    #遍历所有特征时返回出现次数最多的类标签
        return majorityCnt(classList)
    bestFeat = chooseBsetFeatureToSplit(dataSet)    #选择最优特征
    bestFeatLbel = labels[bestFeat] #最优特征标签
    featLabels.append(bestFeatLbel)
    myTree = {bestFeatLbel:{}}  #根据最优特征标签生成树
    del(labels[bestFeat])   #删除已经使用特征标签
    featValues = [example[bestFeat] for example in dataSet] #得到训练数据集中所有最优特征的属性值
    uniqueVals = set(featValues)    #去掉重复属性值
    for value in uniqueVals:    #遍历特征创建决策树
        myTree[bestFeatLbel][value] = createTree(splitDataSet(dataSet,bestFeat,value),labels,featLabels)
    return myTree

"""
    使用决策树进行分类
    参数:
        inputTree-已经生成的决策树
        featLabels-存储选择的最优特征标签
        testVec-测试数据列表
    返回值:
        classLabel-分类结果
"""
def classify(inputTree,featLabels,testVec):
    firstStr = next(iter(inputTree))
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ =='dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else: classLabel = secondDict[key]
    return classLabel

"""
    存储决策树
"""
def storeTree(inputTree,filename):
    with open(filename,'wb') as fw:
        pickle.dump(inputTree,fw)

if __name__ == '__main__':
    dataSet,labels = createDataSet()
    featLabels = []
    myTree = createTree(dataSet,labels,featLabels)
    storeTree(myTree,'classifierStorage.txt')