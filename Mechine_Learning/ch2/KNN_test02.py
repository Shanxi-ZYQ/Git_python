from turtle import color
from matplotlib.font_manager import FontProperties
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import operator


def classify0(inX, dataSet, labels, k):
    #距离计算
    dataSetSize = dataSet.shape[0]
    # tile函数作用是按照某个方向复制元素，第一个参数是行，第二个参数是列
    # 这里在行方向复了inX向量dataSetSize次，在列方向复制了1次
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet  # 计算目标点向量差值
    #对向量中每个数据求平方
    sqDiffMat = diffMat**2  # 差值做平方
    sqDistances = sqDiffMat.sum(axis=1)  # 求和
    distances = sqDistances**0.5  # 开方

    #返回distances中元素从小到大排序后的索引值
    sortedDistIndicies = distances.argsort()
    classCount = {}
    #选择距离最小的k个点
    for i in range(k):
        #取出前k个元素的类别
        voteIlabel = labels[sortedDistIndicies[i]]
        #计算类别出现次数，get()方法返回指定键的值，如果值不在字典中返回默认值
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    #排序
    sortedClassCount = sorted(
        classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

"""
    打开并解析文件,对数据进行分类,1代表不喜欢,2代表魅力一般,3代表极具魅力
    参数:
        filename-文件名
    返回值:
        returnMat - 特征矩阵
        classLabelVector - 分类Label向量
"""
def file2matrix(filename):
    #打开文件
    fr = open(filename)
    #读取文件所有内容
    arrayOLines = fr.readlines()
    #得到文件行数
    numberOfLines = len(arrayOLines)
    #返回Numpy矩阵，有numberOfLine行，3列
    returnMat = np.zeros((numberOfLines,3))
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


"""
    数据归一化,避免计算距离时由于数据差异带来的权重误差
    参数:
        dataSet-特征矩阵
    返回值:
        normDataSet-归一化后的特征矩阵
        ranges- 数据范围
        minVals-数据最小值
"""
def autoNorm(dataSet):
    #获取数据最小值
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    #最大值和最小值范围
    ranges = maxVals - minVals
    #shape()方法返回参数矩阵的行列数
    normDataSet = np.zeros(np.shape(dataSet))
    #返回dataSet的行数
    m = dataSet.shape[0]
    #原始值减去最小值
    normDataSet = dataSet - np.tile(minVals,(m,1))
    #除以最大值和最小值的差
    normDataSet = normDataSet / np.tile(ranges,(m,1))
    #返回归一化数据结果
    return normDataSet,ranges,minVals


"""
    分类器测试函数
    参数:
        无
    返回值:
        normDataSet - 归一化特征矩阵
        ranges - 数据范围
        minVals - 数据最小值

"""
def datingClassTest():
    #打开文件名
    filename = "datingTestSet2.txt"
    #将返回的特征矩阵和分类向量分别存储到datingDataMat和datingLabels
    datingDataMat,datingLabels = file2matrix(filename)
    #取所有数据的百分之十
    hoRatio = 0.10
    #数据归一化，返回归一化矩阵，数据范围，数据最小值
    normMat, ranges, minVals = autoNorm(datingDataMat)
    #获得normMat行数
    m = normMat.shape[0]
    #取训练数据百分之十用于测试
    numTestVecs = int(m * hoRatio)
    #分类错误统计
    errorCount = 0.0

    for i in range(numTestVecs):
        #前numTestVecs个数据用于测试，后m-numTestVecs作为训练集
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],4)
        print("分类结果:%d\t真实类别:%d" %(classifierResult,datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print("错误率:%f%%" %(errorCount/float(numTestVecs)*100))


"""
    构建系统,输入一个三维特征,对特征进行分析
    参数:
        无
    返回值:
        无
"""
def classifyPerson():
    #输出结果
    resultList = ['讨厌','有些喜欢','非常喜欢']
    #用户输入三维特征
    percentTats = float(input('玩游戏所占时间比:'))
    ffMiles = float(input('每年获得飞行常客里程:'))
    iceCream = float(input('每周消费的冰激凌公升数:'))
    #打开文件名
    filename = "datingTestSet2.txt"
    #打开并处理数据
    datingDataMat, datingLabels = file2matrix(filename)
    #归一化
    normMat,ranges,minVals = autoNorm(datingDataMat)
    #生成NumPy数组，测试集
    inArr = np.array([ffMiles, percentTats, iceCream])
    #测试数据归一化
    norminArr = (inArr - minVals)/ranges
    #返回分类结果
    classifierResult = classify0(norminArr,normMat,datingLabels,3)
    #打印输出
    print("你可能%s这个人" % (resultList[classifierResult-1]))


"""
    数据可视化
    参数:
        datingDataMat-特征矩阵
        datingLabels-分类标签
    返回值:
        无
"""
def showdatas(datingDataMat,datingLabels):
    #设置汉字格式
    font = FontProperties(fname=r"c:\Windows\Fonts\simsun.ttc",size=14)
    #分隔fig画布，不共享x轴y轴
    #当nrow=2，nclos=2时，代表fig画布被分隔为四个区域，axs[0][0]表示第一行第一个区域
    fig,axs = plt.subplots(nrows=2,ncols=2,sharex=False,sharey=False,figsize=(13,8))

    numberOfLabels = len(datingLabels)
    LabelsColors = []
    for i in datingLabels:
        if i == 1:
            LabelsColors.append('black')
        if i == 2:
            LabelsColors.append('orange')
        if i == 3:
            LabelsColors.append('red')
    
    #画出散点数，以datingDataMat矩阵第一列，第二列数据画散点图，散点大小15，透明度0.5
    axs[0][0].scatter(x=datingDataMat[:,0],y=datingDataMat[:,1],color=LabelsColors,s=15,alpha=.5)
    #设置x轴y轴标题
    axs0_title_text = axs[0][0].set_title(
        u'每年获得飞行常客里程数与玩游戏所消耗时间占比', fontproperties=font)
    axs0_xlabel_text = axs[0][0].set_xlabel(
        u'每年获得飞行常客里程数', fontproperties=font)
    axs0_ylabel_text = axs[0][0].set_ylabel(
        u'玩游戏消耗时间占比', fontproperties=font)
    plt.setp(axs0_title_text,size=9,weight='bold',color='red')
    plt.setp(axs0_xlabel_text, size=7, weight='bold', color='black')
    plt.setp(axs0_ylabel_text, size=7, weight='bold', color='black')

    #画出散点图，以datingDataMat矩阵的第一列，第三列数据画散点数据，散点大小15，透明度0.5
    axs[0][1].scatter(x=datingDataMat[:,0],y=datingDataMat[:,2],color=LabelsColors,s=15,alpha=.5)
    #设置标题
    axs1_title_text = axs[0][1].set_title(
        u'每年获得的飞行常客里程数与每周消费的冰激凌公升数', fontproperties=font)
    axs1_xlabel_text = axs[0][1].set_xlabel(
        u'每年获得的飞行常客里程数', fontproperties=font)
    axs1_ylabel_text = axs[0][1].set_ylabel(
        u'每周消费的冰激凌公升数', fontproperties=font)
    plt.setp(axs1_title_text, size=9, weight='bold', color='red')
    plt.setp(axs1_xlabel_text, size=7, weight='bold', color='black')
    plt.setp(axs1_ylabel_text, size=7, weight='bold', color='black')

    #以datingDataMat矩阵的第二列，第三列数据画散点数据，散点大小为15，透明度0.5
    axs[1][0].scatter(x=datingDataMat[:, 1], y=datingDataMat[:,
                      2], color=LabelsColors, s=15, alpha=.5)
    #设置标题
    axs2_title_text = axs[1][0].set_title(
        u'玩视频游戏所消耗时间占比与每周消费冰激凌公升数', fontproperties=font)
    axs2_xlabel_text = axs[1][0].set_xlabel(50 
        u'玩游戏消耗时间占比', fontproperties=font)
    axs2_ylabel_text = axs[1][0].set_ylabel(
        u'每周消费的冰激凌公升数', fontproperties=font)
    plt.setp(axs2_title_text, size=9, weight='bold', color='red')
    plt.setp(axs2_xlabel_text, size=7, weight='bold', color='black')
    plt.setp(axs2_ylabel_text, size=7, weight='bold', color='black')

    #设置图例
    didntLike = mlines.Line2D([],[],color='black',marker='.',markersize=6,label='didntLike')
    smallDoses = mlines.Line2D([],[],color='orange',marker='.',markersize=6,label='smallDoses')
    largeDoses = mlines.Line2D([],[],color='red',marker='.',markersize=6,label='largeDoses')

    #添加图例
    axs[0][0].legend(handles=[didntLike,smallDoses,largeDoses])
    axs[0][1].legend(handles=[didntLike,smallDoses,largeDoses])
    axs[1][0].legend(handles=[didntLike, smallDoses, largeDoses])

    plt.show()




if __name__ == '__main__':
    # #打开文件
    # filename = "datingTestSet2.txt"
    # #打开并处理数据
    # datingDataMat,datingLabels = file2matrix(filename)
    # # showdatas(datingDataMat,datingLabels)
    # normDataSet,ranges,minVals = autoNorm(datingDataMat)
    classifyPerson()