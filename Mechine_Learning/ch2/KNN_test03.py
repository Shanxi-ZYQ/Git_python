import numpy as np
import operator
from os import listdir
from sklearn.neighbors import KNeighborsClassifier as KNN

"""
    将32 x 32的二进制图像转换为1 x 1024向量
    参数:
        filename-文件名
    返回值:
        returnVect-返回的二进制图像的1x1024向量
"""
def img2vector(filename):
    #创建返回向量
    returnVect = np.zeros((1,1024))
    #打开文件
    fr = open(filename)
    #按行读取
    for i in range(32):
        #读一行数据
        lineStr = fr.readline()
        #每行32个元素依次添加到返回向量中
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    #返回结果
    return returnVect

"""
    数字分类测试
"""
def handwritingClassTest():
    #测试集Labels
    hwLabels = []
    #返回训练集目录下的文件名
    trainingFileList = listdir('trainingDigits')
    #返回文件夹下文件的个数
    m = len(trainingFileList)
    #初始化训练的Mat矩阵
    trainingMat = np.zeros((m,1024))
    #从文件名解析训练数据类标签
    for i in range(m):
        #获得文件的名字
        fileNameStr = trainingFileList[i]
        #获得分类的数字
        classNumber = int(fileNameStr.split('_')[0])
        #将获得的类别添加到hwLabels中
        hwLabels.append(classNumber)
        #将每个文件的1x1024数据存储到trainingMat矩阵中
        trainingMat[i,:] = img2vector('trainingDigits/%s'%(fileNameStr))
    
    #构建KNN分类器
    neigh = KNN(n_neighbors=3,algorithm='auto')
    #拟合模型，trainingMat为测试矩阵，hwLabels为对应标签
    neigh.fit(trainingMat,hwLabels)
    #返回testDigits目录下的文件列表
    testFileList = listdir('testDigits')
    #错误检测计数
    errorCount = 0.0
    #测试数据的数量
    mTest = len(testFileList)
    #从文件中解析出测试集类别并进行分类
    for i in range(mTest):
        #获得文件的名字
        fileNameStr = testFileList[i]
        #获得分类的数字
        classNumber = int(fileNameStr.split('_')[0])
        #获得测试集的1x1024向量
        vectorUnderTest = img2vector('testDigits/%s'%(fileNameStr))
        #获得测试结果
        classifierResult = neigh.predict(vectorUnderTest)
        print("分类返回结果为%d\t真实的结果为%d"%(classifierResult,classNumber))
        if(classifierResult != classNumber):
            errorCount += 1.0
    print("总共错了%d个数据\n错误率为%f%%" % (errorCount, errorCount/mTest*100))

if __name__ == '__main__':
    handwritingClassTest()