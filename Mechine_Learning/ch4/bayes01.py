from functools import reduce
import numpy as np
"""
    实验样本
    返回值:
        postingList - 实验样本切分的词条
        classVec - 类别标签向量
"""
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],                #切分的词条
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1] #1表示侮辱性词汇，0表示非侮辱性词汇
    return postingList,classVec

"""
    根据vocabList词汇表,将inputSet向量化,向量的每个元素为1或0
    参数:
        vocabList - 其他函数返回的词汇表
        inputSet - 切分的词条列表
    返回值:
        returnVec - 文档向量,词集模型
"""
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0] * len(vocabList)    #创建要返回的向量
    for word in inputSet:               #遍历每个词条
        if word in vocabList:           #如果词条在词汇表中，就置1
            returnVec[vocabList.index(word)] = 1
        else: print('该单词%s不在词典中' %word)
    return returnVec

"""
    将切分的实验样本词条整理成不重复的词条列表
    参数:
        dataSet-整理的样本数据集
    返回值:
        vocabSet-返回不重复的词条列表
"""
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

"""
    训练朴素贝叶斯分类器
    参数:
        trainMatrix-训练矩阵
        trainCategory-训练类别标签向量
    返回值:
        p0Vect-侮辱类的条件概率组数据
        p1Vect-非侮辱类的条件概率数组
        pAbusive-文档属于侮辱类的概率
"""
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix) #计算训练的文档数目
    numWords = len(trainMatrix[0])  #计算每篇文档的词条数
    pAbusive = sum(trainCategory)/float(numTrainDocs)   #文档属于侮辱类的概率:侮辱类文档数量/文档总数
    p0Num = np.ones(numWords); p1Num = np.ones(numWords)  #创建numpy.zero数组，词条出现数初始为0
    p0Denom = 2.0; p1Denom = 2.0    #分母初始化为0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:   #统计属于侮辱类的条件概率所需的数据
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:                       #统计属于非侮辱类的条件概率所需数据
            p0Num += trainMatrix[1]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num/p1Denom
    p0Vect = p0Num/p0Denom
    return p0Vect,p1Vect,pAbusive   #返回属于侮辱类的条件概率数组,属于非侮辱类的条件概率数组，文档属于侮辱类的概率

"""
    使用朴素贝叶斯分类器进行分类
    参数:
        vec2Classify-待分类的词条数组
        p0Vec - 侮辱类的条件概率数组
        p1Vec -  非侮辱类的条件概率数组
        pClass1 - 文档属于侮辱类的概率
    返回值:
        0-属于非侮辱类
        1-属于侮辱类
"""
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec)+np.log(pClass1)
    p0 = sum(vec2Classify*p0Vec)+np.log(1.0-pClass1)
    print('p0:',p0)
    print('p1:',p1)
    if p1>p0:
        return 1
    else:
        return 0

"""
    测试朴素贝叶斯分类器
"""
def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNB0(np.array(trainMat),np.array(listClasses))    #训练朴素贝叶斯分类器
    testEntry = ['love','my','dalmation']   #测试样本
    thisDoc = np.array(setOfWords2Vec(myVocabList,testEntry))   #测试样本向量化
    if classifyNB(thisDoc,p0V,p1V,pAb):
        print(testEntry,'属于侮辱类')
    else:
        print(testEntry,'属于非侮辱类')
    testEntry = ['stupid','garbage']
    thisDoc = np.array(setOfWords2Vec(myVocabList,testEntry))
    if classifyNB(thisDoc,p0V,p1V,pAb):
        print(testEntry,'属于侮辱类')
    else:
        print(testEntry,'属于非侮辱类')


if __name__ == '__main__':
    testingNB()