import numpy as np
import matplotlib.pyplot as plt

def loadSimpData():
    dataMat = np.matrix([[1.,2.1],[1.5,1.6],[1.3,1.],[1.,1.],[2.,1.]])
    classLabels = [1.0,1.0,-1.0,-1.0,1.0]
    return dataMat,classLabels


"""
    单层决策树分类函数
    参数
        dataMatrix - 数据矩阵
        dimen - 第dimen个特征
        threshVal - 阈值
        threshIneq - 标志
    返回
        retArray - 分类结果
"""
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray = np.ones((np.shape(dataMatrix)[0],[1]))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = 1.0
    return retArray