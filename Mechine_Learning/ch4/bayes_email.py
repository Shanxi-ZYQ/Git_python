import re
from this import d
import numpy as np
import random

"""
    接收一个大字符串并将其解析为字符串列表
"""
def textParse(bigString):
    listOfTokens = re.split(r'\W+',bigString)   #将特殊符号作为切分标志进行切分，即非字母数组
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]    #除了单个字母，其他单词变成小写

"""
    组建词汇表
    参数:
        dataSet - 样本数据集
    返回值:
        vocabSet - 返回不重复的词典
"""
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

"""
    根据词汇表,将测试数据向量化
    参数:
        vocabList - 词汇表
        inputSet - 测试样例
    返回:
        returnVec - 文档向量,词集模型

"""
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print('表中没有%s这个单词' % word)
    return returnVec

"""
    根据词汇表,构建词袋模型
    参数:
        vocabList - 词汇表
        inputSet - 输入数据
    返回值:
        returnVec - 文档向量
"""
def bagOfWords2VecMN(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

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

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify*p1Vec)+np.log(pClass1)
    p0 = sum(vec2Classify*p0Vec)+np.log(1.0-pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

"""
    测试函数
"""
def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1,26):   #遍历25个txt文件
        wordList = textParse(open('spam/%d.txt' % i,'r').read())#读取每个垃圾邮件，并将字符串转成字符串列表
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(1)
        wordList = textParse(open('ham/%d.txt' % i, 'r').read())#读取非垃圾邮件
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(0)
    print(docList)
    vocabList = createVocabList(docList)    #创建词汇表
    trainingSet = list(range(50)); testSet = [] #创建存储训练集索引值的列表和测试集的索引值列表
    for i in range(10):                                         #从50个邮件中随机挑选40个作为训练集，10个作为测试集
        randIndex = int(random.uniform(0,len(trainingSet)))     #随机选取索引值
        testSet.append(trainingSet[randIndex])                  #添加测试集的索引值
        del(trainingSet[randIndex])                             #在训练集中删除测试集数据
    trainMat = []; trainClasses = []                            #创建训练集矩阵和训练集类别标签向量
    for docIndex in trainingSet:                                #遍历训练集
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))    #将生成的词集模型添加到训练集矩阵
        trainClasses.append(classList[docIndex])                #将类别添加到训练集类别标签向量中
    p0V,p1V,pSpam = trainNB0(np.array(trainMat),np.array(trainClasses))#训练朴素贝叶斯
    errorCount = 0 #统计分类错误
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(np.array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
            print('分类错误测试集:',docList[docIndex])
    print('错误率:%.2f%%' %(float(errorCount)/len(testSet)*100))

if __name__ == '__main__':
    spamTest()