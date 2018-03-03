from matplotlib import pyplot as plt
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.learning_curve import learning_curve
import numpy as np
import pickle

# 利用matplotlib.pyplot，展现机器学习的各种能力
# 如果需要多种学习模型和参数，那么就应该在这里设置读取文件，另外判断check那里也需要读取文件
# 从文件中加载模型，因此只要创建的文件保存到一个文件即可

class SVCView:
    def __init__(self,dataList):                    # 必须传递数据
        self.Xdata = dataList[0]                    # 特征向量
        self.Xtarget = dataList[1]                  # 类型
        self.xlen = len(self.Xtarget)           # 存储邮件数量,考虑到xlen为2*num，可以取消此项，可以修改AtoD的方法
        self.dataNormal()

    def dataNormal(self):
        # 填充属性，使邮件的特征向量数达到20个，使用前面几个值填充
        for i in range(self.xlen):
            l = len(self.Xdata[i])
            try:
                for j in range(20 - l):
                    self.Xdata[i].append(self.Xdata[i][j])
            except:
                while len(self.Xdata[i]) < 20:
                    self.Xdata[i].append(-1)
                continue

        Xdata = preprocessing.scale(self.Xdata)
        self.Xdata = Xdata

    # 散点图，预测正确的y坐标为1，预测错误y坐标为0
    # 如果发生以外，可以将文件改为../data/SVCmode ,
    # scatterVIew均只展现部分数据的预测。训练和实际的预测不同，多在于数据的预处理部分
    def scatterView(self):
        loss = []
        with open('../data/machineModel/machineModel', 'rb') as f:
            clf = pickle.load(f)
            for i in range(200):
                pred = clf.predict(self.Xdata[i])
                if pred - self.Xtarget[i] == 0:
                    loss.append(1)
                else:
                    loss.append(0)

        x = range(200)
        plt.scatter(x,loss)
        plt.show()

    # 两个条形图，一个是预测正确的数量，一个是预测错误的数量
    def barView(self):
        # 进行测试，并统计结果
        wroNum = 0
        with open('../data/machineModel/machineModel', 'rb') as f:
            clf = pickle.load(f)
            for i in range(200):
                pred = clf.predict(self.Xdata[i])
                if not pred - self.Xtarget[i] == 0:
                    wroNum += 1

        # 此处准确率不可观，不知是否可以优化

        # 展示图形
        plt.bar(1,200-wroNum)
        plt.bar(2,wroNum)
        plt.xticks([1,2],[r'$right$','r$error$'])
        plt.show()

    # 此处展示的是不同的机器学习模型，不同的参数的判断效果，需要使用的数据较多
    def learnView(self):
        # 学习曲线观察,可以看出是否过学习
        with open('../data/machineModel/machineModel', 'rb') as f:
            clf = pickle.load(f)

        train_sizes,train_loss, test_loss = learning_curve(clf,self.Xdata,self.Xtarget,
                                                 cv=10,scoring='accuracy',train_sizes=[0.1,0.25,0.5,0.75,1])

        train_loss_mean = -np.mean(train_loss,axis=1)
        test_loss_mean = -np.mean(test_loss,axis=1)

        # 可视化图形
        plt.plot(train_sizes, train_loss_mean, 'o-', color="r",				# train_size,train_loss_mean都是包含五个元素的列表，test类似
                 label="Training")
        plt.plot(train_sizes, test_loss_mean, 'o-', color="g",
                label="Testing")

        plt.xlabel("Training examples")
        plt.ylabel("Loss")
        plt.legend(loc="best")
        plt.show()


if __name__ == '__main__':
    import sys
    sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\util')
    from attributeTodict import AToD
    X = AToD().get_Xdata(100)  # 获得数据，包括特征向量和类型
    v = SVCView(X)
    v.scatterView()