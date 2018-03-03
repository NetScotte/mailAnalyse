from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import pickle
from attributeTodict import AToD



class create:
    def __init__(self,num=3000):
        self.num = num              # 这是用来进行提取的邮件数量，按顺序提取
        self.target = None          # 在初始化数据时赋值
        self.data = None
        self.clf = None
        self.param = []
        with open('../data/machineModel/machineParam','r') as f:
            for i in f:
                self.param.append(i.strip('\n'))

    
    def initData(self):
        X = AToD().get_Xdata(self.num)  # 获得数据，包括特征向量和类型
        Xdata = X[0]                        # 特征向量
        Xtarget = X[1]                       # 类型
        xlen = 2 * self.num                  # 存储邮件数量,考虑到xlen为2*num，可以取消此项，可以修改AtoD的方法

        # 填充属性，使邮件的特征向量数达到20个，使用前面几个值填充
        for i in range(xlen):
            l = len(Xdata[i])
            try:
                for j in range(20 - l):
                    Xdata[i].append(Xdata[i][j])
            except:
                while len(Xdata[i]) < 20:
                    Xdata[i].append(-1)
                continue

        # 对于KNN,decision,此部分可以不要，有了这一步应该更好吧
        Xdata = preprocessing.scale(Xdata)
        self.data = Xdata
        self.target = Xtarget

    def train(self):
        if self.param[0] == 'SVC':
            if not self.param[2] == 'auto':
                self.param[2] = int(self.param[2])
            self.param[3] = int(self.param[3])
            self.SVCmodel()
        if self.param[0] == 'KNN':
            self.param[2] = int(self.param[2])
            self.param[3] = int(self.param[3])
            self.KNNmodel()
        if self.param[0] == 'Decision':
            self.param[2] = int(self.param[2])
            self.param[3] = int(self.param[3])
            self.Decisionmodel()

        self.saveModel()
        s = '{0}--{1}--{2}--{3} has been train success'.format(self.param[0],self.param[1],\
                                                               self.param[2],self.param[3])
        return s

    def SVCmodel(self):
        # 给出以下几个参数和数据，都是核心的参数的数据
        # gamma: 0.25, 0.5, 0.75, 1
        # C: 1, 3, 5, 7, 10
        # kernel: linear, rbf, poly, sigmoid
        # 最佳参数为kernel=poly , C=1 , gamma=0.5可能为auto
        # self.clf = SVC(kernel='poly',gamma=0.5,C=1)
        self.clf = SVC(kernel=self.param[1],gamma=self.param[2],C=self.param[3])
        X_train,X_test,Y_train,Y_test = train_test_split(self.data,self.target,test_size=0.3)
        self.clf.fit(X_train,Y_train)
        # with open('../data/machineModel/SVC','w') as f:
        #     pickle.dump(clf,f)


    def KNNmodel(self):
        # 参数部分
        # 最佳参数为weights=distance , neighbors=5
        # self.clf = KNeighborsClassifier(weights='distance',n_neighbors=5)
        self.clf = KNeighborsClassifier(weights=self.param[1],n_neighbors=self.param[2])
        X_train, X_test, Y_train, Y_test = train_test_split(self.Xdata, self.Xtarget, test_size=0.3)
        self.clf.fit(X_train, Y_train)
        # with open('../data/machineModel/KNN','w') as f:
        #     pickle.dump(self.clf,f)


    def Decisionmodel(self):
        # 参数部分
        # 最佳参数为max_depth=5,min_samples_leaf=5,min_samples_split=2
        # self.clf = DecisionTreeClassifier(max_depth=5,min_samples_leaf=5,min_samples_split=2)
        self.clf = DecisionTreeClassifier(max_depth=self.param[1],min_samples_leaf=self.param[2],min_samples_split=self.param[3])
        X_train,X_test,Y_train,Y_test = train_test_split(self.Xdata,self.Xtarget,test_size=0.3)
        self.clf.fit(X_train,Y_train)
        # with open('../data/machineModel/Decision','w') as f:
        #     pickle.dump(clf,f)

    # 此部分未在界面中实现，用于后台调试
    def modelSelection(self):
        # 关于模型的评价，可以在tain模块中使用相应的评分，过学习观察，实际测试等测试对应例子，这里不在重复给出
        # 使用评测工具，选择模型
        # SVC的参数部分
        # parameters = {'kernel': ('linear','poly', 'rbf','sigmoid'), 'C': [1,5,10],'gamma':[0.25,0.5,0.75]}
        # svr = SVC()

        # KNN参数部分
        # parameters = {'algorithm':('auto','ball_tree','kd_tree','brute'),'weights':('uniform','distance'),'n_neighbors':[5,10,15,20]}
        # svr = KNeighborsClassifier()


        # decision参数部分
        parameters = {'max_depth':[3,5,10,15],'min_samples_leaf':[3,5,10,15],'min_samples_split':[2,3,4]}
        svr = DecisionTreeClassifier()



        clf = GridSearchCV(svr, parameters,scoring='f1')
        clf.fit(self.data,self.target)
        print(clf.best_estimator_)

        # 基于给定模型评分
        # 模型测试poly,C=1 , gamma=0.4评分最高为0.9725
        # s = SVC(kernel='poly',C=1,gamma=0.4)
        # s.fit(self.data,self.target)
        # scores = cross_val_score(s,self.data,self.target,cv=5,scoring='accuracy')
        # print(scores.mean())

    def saveModel(self):
        if not self.clf is None:
            with open('../data/machineModel/machineModel','wb') as f:
                pickle.dump(self.clf,f)


if __name__ =='__main__':
    c = create()
    c.initData()      # 使用这两句之前，应该手动为self.param设置合适的值
    c.train()
    print(c.clf)