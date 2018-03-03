import sys
sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\util')
from sklearn import preprocessing
from sklearn.learning_curve import learning_curve,validation_curve
import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from attributeTodict import AToD
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import time
# 此为测试部分
# 想不到列表可以存这么多东西，速度还是很快的，使用6000封即可
# 显然不能直接将字符串形式的属性投入训练，那么就需要考虑将属性转换为数组，那么显然为字典，


a = time.time()
num=3000                # 这是用来进行提取的邮件数量，按顺序提取
X=AToD().get_Xdata(num) # 获得数据，包括特征向量和类型
Xdata=X[0]              # 特征向量
Xtarget=X[1]            # 类型
xlen=2*num              # 存储邮件数量,考虑到xlen为2*num，可以取消此项，可以修改AtoD的方法

# 填充属性，使邮件的特征向量数达到20个，使用前面几个值填充
for i in range(xlen):
    l = len(Xdata[i])
    try:
        for j in range(20-l):
            Xdata[i].append(Xdata[i][j])
    except:
        while len(Xdata[i])<20:
            Xdata[i].append(-1)
        continue

Xdata = preprocessing.scale(Xdata)

clf = SVC(kernel='poly',gamma=0.5,C=1)
scores = cross_val_score(clf,Xdata,Xtarget,cv=5,scoring='average_precision')
print(scores)
b=time.time()
print(b-a)