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

# 此为测试部分
# 想不到列表可以存这么多东西，速度还是很快的，使用6000封即可
# 显然不能直接将字符串形式的属性投入训练，那么就需要考虑将属性转换为数组，那么显然为字典，


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

# 如何优化：改变训练数据，改变正规化方式，改变算法，改变算法参数
# 正规化数据，去掉此正规化后，结果为0.915,正规化后为0.955
# Xdata=[]
# Xdata.append([3, 5, -16, 2, 4, 40, 1, 12, 8, 118, 33, 21, 2, 1, 8, 1, 2, 25, 4, 400])
# Xdata.append([623, 7, 5, 233, 8, 0, 75, 142, 623, 7, 5, 233, 8, 0, 75, 142, 623, 7, 5, 233])
# Xdata.append([4, 2, 14, 10, 58, 134, 25, 2, 2, 3, 6, 2, 5, 748, 2, 6, 2, 2, 6, 39])
# for i in range(3):
#     l = len(Xdata[i])
#     try:
#         for j in range(20-l):
#             Xdata[i].append(Xdata[i][j])
#     except:
#         while len(Xdata[i])<20:
#             Xdata[i].append(-1)

Xdata = preprocessing.scale(Xdata)


# with open('../data/SVCmode', 'wb') as f:
#     pickle.dump(clf, f)
# # 模块2
# # 参数部分,不知为何，速度不是一般的慢
# param_range = np.logspace(-6,-2.3,5)
# train_loss, test_loss = validation_curve(clf,Xdata,Xtarget,param_name='gamma',param_range=param_range,
#                                          cv=5,scoring='accuracy')

# 创建学习模型
# SVC部分
clf = SVC(kernel='poly',gamma=0.5,C=1)
X_train,X_test,Y_train,Y_test = train_test_split(Xdata,Xtarget,test_size=0.3)
clf.fit(X_train,Y_train)
# print(clf)


# 决策树部分：
# 准确率真高，不知是否存在过渡学习,基本百分百呀
# clf = DecisionTreeClassifier()
# X_train,X_test,Y_train,Y_test = train_test_split(Xdata,Xtarget,test_size=0.3)
# clf.fit(X_train,Y_train)
# print(clf)
# 评分部分
# scores = cross_val_score(clf,Xdata,Xtarget,cv=5,scoring='accuracy')
# print(scores.mean())


# KNN部分,
# clf = KNeighborsClassifier()
# X_train,X_test,Y_train,Y_test = train_test_split(Xdata,Xtarget,test_size=0.3)
# clf.fit(X_train,Y_train)
# print(clf)

# 评分部分
scores = cross_val_score(clf,Xdata,Xtarget,cv=5,scoring='average_precision')
print(clf.predict(Xdata[10]),Xtarget[:10])



# 真实使用,使用数据分割后的测试数据进行
# with open('../data/machineModel/machineModel','rb') as f:
#     clf = pickle.load(f)

# loss = []
# wroNum=0
# for i in range(200):
#     pred = clf.predict(Xdata[i])
#     if pred - Xtarget[i] == 0:
#         loss.append(1)
#     else:
#         loss.append(0)
#         wroNum += 1
#
# x = range(200)
# plt.scatter(x,loss)
# plt.show()
#
# plt.bar(0,200-wroNum)
# plt.bar(1,wroNum)
# plt.xticks([0,1],[r'$right$','r$error$'])
# plt.show()

#模块4
# 学习曲线观察,可以看出是否过学习
# param_range = np.logspace(-6,-2.3,5)
# train_sizes,train_loss, test_loss = learning_curve(clf,Xdata,Xtarget,
#                                          cv=10,scoring='accuracy',train_sizes=[0.1,0.25,0.5,0.75,1])
#
# train_loss_mean = -np.mean(train_loss,axis=1)
# test_loss_mean = -np.mean(test_loss,axis=1)
#
# # 可视化图形
# plt.plot(train_sizes, train_loss_mean, 'o-', color="r",				# train_size,train_loss_mean都是包含五个元素的列表，test类似
#          label="Training")
# plt.plot(train_sizes, test_loss_mean, 'o-', color="g",
#         label="Testing")
#
# plt.xlabel("Training examples")
# plt.ylabel("Loss")
# plt.legend(loc="best")
# plt.show()