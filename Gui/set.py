from PyQt5.QtWidgets import (QApplication,QComboBox,QHBoxLayout,QGroupBox,QLabel,QWidget,
                             QLineEdit,QGridLayout,QListWidget,QPushButton,QVBoxLayout,QMessageBox)

# 该模块用于设置页面以及行为模式
class MySetting(QWidget):
    def __init__(self):
        super(MySetting,self).__init__()

        layout = QVBoxLayout()
        layout.addWidget(self.ruleBox())
        layout.addWidget(self.SVCBox())
        self.setLayout(layout)

        self.setWindowTitle('Setting')

    # 黑白名单的部分
    def ruleBox(self):

        # 组件
        rule = QGroupBox('关键字过滤')
        self.text = QLineEdit()
        self.blackButton = QPushButton('black')
        self.whiteButton = QPushButton('white')
        self.list = QListWidget(self)
        self.tag =0

        self.list.itemDoubleClicked.connect(self.delfunc)

        self.blackButton.clicked.connect(self.ruleAct)
        self.whiteButton.clicked.connect(self.ruleAct)
        # 布局
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.text)
        hlayout.addWidget(self.blackButton)
        hlayout.addWidget(self.whiteButton)
        layout = QVBoxLayout()
        layout.addLayout(hlayout)
        layout.addWidget(self.list)
        rule.setLayout(layout)

        return rule

    # 用于设置程序风格等属性，暂时保留
    def styleBox(self):
        pass


    # 用来控制机器学习，包括学习算法，参数等
    #
    def SVCBox(self):
        self.SVC = QGroupBox('机器学习')
        self.layout = QGridLayout()

        modelLab = QLabel('model:')
        self.modelCom = QComboBox()
        self.modelCom.addItem('SVC')
        self.modelCom.addItem('KNN')
        self.modelCom.addItem('Decision')
        modelLab.setBuddy(self.modelCom)
        self.modelCom.activated.connect(self.SVCfunc)

        self.param1Lab = QLabel('kernel: ')
        self.param1Edit = QComboBox()
        self.param1Edit.addItem('rbf')
        self.param1Edit.addItem('linear')
        self.param1Edit.addItem('poly')
        self.param1Edit.addItem('sigmoid')

        self.param2Lab = QLabel('gamma: ')
        self.param2Edit = QLineEdit('auto')

        self.param3Lab = QLabel('C: ')
        self.param3Edit = QLineEdit('1')

        # 以下是测试时的用例
        # self.param1Lab= QLabel('param1:')
        # self.param1Edit = QLineEdit()
        # # self.param1Lab.setBuddy(self.param1Edit)
        #
        # self.param2Lab = QLabel('param2:')
        # self.param2Edit = QLineEdit()
        # # self.param2Lab.setBuddy(self.param2Edit)
        #
        # self.param3Lab = QLabel('param3:')
        # self.param3Edit = QLineEdit()
        # # self.param3Lab.setBuddy(self.param3Edit)

        saveButton = QPushButton('save')
        saveButton.clicked.connect(self.saveModel)

        self.layout.addWidget(modelLab,0,0,1,1)
        self.layout.addWidget(self.modelCom,0,1,1,2)
        self.layout.addWidget(self.param1Lab,1,0,1,1)
        self.layout.addWidget(self.param1Edit,1,1,1,2)
        self.layout.addWidget(self.param2Lab,2,0,1,1)
        self.layout.addWidget(self.param2Edit,2,1,1,2)
        self.layout.addWidget(self.param3Lab,3,0,1,1)
        self.layout.addWidget(self.param3Edit,3,1,1,2)
        self.layout.addWidget(saveButton,4,2,1,2)
        self.SVC.setLayout(self.layout)

        return self.SVC


    # 该模块定义了双击列表中的某项后，产生的删除行为
    # 如何删除一项呢,删除了之后，原处为空了，另外在结尾增加了空
    def delfunc(self):
        item = self.list.currentRow()
        self.list.takeItem(item)
        list = []
        j=0
        # 删除黑名单中的元素
        if self.tag == 0:
            with open('../data/blackList','r') as f:
                for i in f:
                    if j==item:
                        pass
                    elif not i == '\n':
                        list.append(i)
                    j += 1

            with open('../data/blackList','w') as f:
                for i in list:
                    f.write(i)

        # 删除白名单中的元素
        if self.tag == 1:
            with open('../data/whiteList','r') as f:
                for i in f:
                    if j==item:
                        pass
                    elif not i == '':
                        list.append(i)
                    j += 1

            with open('../data/whiteList','w') as f:
                for i in list:
                    f.write(i)
            # 结尾可以没有f.flush（），不能为f.write(i+'\n')，它会自己换行
            # 为什么在其他地方，却不会换行呢：
            # 估计是添加到文件时，每个字符都带有一个\n，如果这里再加入，那么就会出现多个换行



    # 定义了列表的呈现和添加行为动作
    def ruleAct(self):
        self.list.clear()
        if self.sender().text() == 'black':
            self.tag = 0
            if not self.text.text() == '':
                with open('../data/blackList','a') as f:
                    t = self.text.text() + '\n'
                    f.write(t)
                    f.flush()
            with open('../data/blackList','r') as f:
                list=[]
                for i in f:
                    list.append(i)
                self.list.addItems(list)

        if self.sender().text() == 'white':
            self.tag = 1
            if not self.text.text() == '':
                with open('../data/whiteList','a') as f:
                    t = self.text.text()+'\n'
                    f.write(t)
                    f.flush()
            with open('../data/whiteList','r') as f:
                list=[]
                for i in f:
                    list.append(i)
                self.list.addItems(list)

        self.text.setText('')

    # 定义了
    def SVCfunc(self):
        SVCmode = self.modelCom.currentText()
        # 显示不同的参数列表
        # 构造一个布局管理器
        # 先移除：
        # self.layout.removeWidget(self.param1Lab)
        # self.layout.removeWidget(self.param1Edit)
        # self.layout.removeWidget(self.param2Lab)
        # self.layout.removeWidget(self.param2Edit)
        # self.layout.removeWidget(self.param3Lab)
        # self.layout.removeWidget(self.param3Edit)

        # 使用移除时，表现不理想
        self.param1Lab.hide()
        self.param1Edit.hide()
        self.param2Lab.hide()
        self.param2Edit.hide()
        self.param3Lab.hide()
        self.param3Edit.hide()

        # 以下显示的参数均为默认参数，即不传参给机器模型
        if SVCmode == 'SVC':
            self.param1Lab= QLabel('kernel: ')
            self.param1Edit = QComboBox()
            self.param1Edit.addItem('rbf')
            self.param1Edit.addItem('linear')
            self.param1Edit.addItem('poly')
            self.param1Edit.addItem('sigmoid')

            self.param2Lab = QLabel('gamma: ')
            self.param2Edit = QLineEdit('auto')

            self.param3Lab = QLabel('C: ')
            self.param3Edit = QLineEdit('1')



        if SVCmode =='KNN':
            self.param1Lab= QLabel('weights: ')
            self.param1Edit = QComboBox()
            self.param1Edit.addItem('uniform')
            self.param1Edit.addItem('distance')


            self.param2Lab = QLabel('neighbors: ')
            self.param2Edit = QLineEdit('5')

            self.param3Lab = QLabel('leaf size:')
            self.param3Edit = QLineEdit('30')
            self.param3Edit.setReadOnly(True)


        if SVCmode =='Decision':
            self.param1Lab= QLabel('depth ')
            self.param1Edit = QLineEdit('None')

            self.param2Lab = QLabel('leafs: ')
            self.param2Edit = QLineEdit('1')

            self.param3Lab = QLabel('splits: ')
            self.param3Edit = QLineEdit('2')

        self.layout.addWidget(self.param1Lab, 1, 0, 1, 1)
        self.layout.addWidget(self.param1Edit, 1, 1, 1, 2)
        self.layout.addWidget(self.param2Lab, 2, 0, 1, 1)
        self.layout.addWidget(self.param2Edit, 2, 1, 1, 2)
        self.layout.addWidget(self.param3Lab, 3, 0, 1, 1)
        self.layout.addWidget(self.param3Edit, 3, 1, 1, 2)


        # # 读取文件
        # param1 = self.param1Edit.text()
        # param2 = self.param2Edit.text()
        # param3 = self.param3Edit.text()
        # with open('F:/学习杂件/程序/python/dataset/data','wb') as f:
        #     f.write(SVCmode+'\n')
        #     f.write(param1+'\n')
        #     f.write(param2+'\n')
        #     f.write(param3)

    def saveModel(self):
        model = self.modelCom.currentText()
        if model == 'Decision':
            param1 = self.param1Edit.text()
        else:
            param1 = self.param1Edit.currentText()
        param2 = self.param2Edit.text()
        param3 = self.param3Edit.text()
        print(model,param1,param2,param3)
        with open('../data/machineModel/machineParam','w') as f:
            f.write(model+'\n')
            f.write(param1+'\n')
            f.write(param2+'\n')
            f.write(param3)
            f.flush()

        self.showMessage('save success')

    def showMessage(self, s):
        message = QMessageBox()
        message.setText(s)
        message.exec_()



# 用于测试该模块的可用性
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    setting = MySetting()
    setting.show()

    sys.exit(app.exec_())
