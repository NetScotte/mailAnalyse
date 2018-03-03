import os
from distutils.sysconfig import get_python_lib
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(get_python_lib(), 'PyQt5','Qt', 'plugins', 'platforms')
import sys
sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\interface')
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDockWidget, QAction, QFileDialog,
                             QTextEdit, QMessageBox, QListWidget)
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtGui import QIcon
import re
from set import MySetting
from train import MyTraining
from interface import ToolKit


# 一个拓展部件,通过实验探索，只能知道源的确切信息，对于目的地的具体行数不清楚，故
# 测试时间已过，那么就使用subject

class myListWidget(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def dropEvent(self, e):
        if e.source() == self:
            e.ignore()
        else:
            super().dropEvent(e)
            e.setDropAction(Qt.MoveAction)          # 这两句可以实现
            e.accept()
        # 以下可以获取到源项所在的行数等信息，可以获取源部件,e.source().currentRow()


# 定义程序的主界面，启动程序
class MainGui(QMainWindow):

    windowsList = []            # 用于存储窗口，否则无法打开，会出现闪退的现象
    currentFile = ''             # 存储用于分析的文件名
    currentNormal = []            # 存储normal列表中subject对应的文件名，以便分析和展现
    currentTrash = []             # 存储trash列表中subject对应的文件名，以便分析和展现

    def __init__(self):
        super(MainGui, self).__init__()

        self.mainWindow()
        self.setWindowTitle('mailAnalyse')
        self.setWindowIcon(QIcon('../img/web.jpg'))
        self.resize(800, 600)
        self.show()

    # 窗口默认展开的界面
    def mainWindow(self):

        # 设置菜单行为
        # 设置打开文件
        openAction = QAction(QIcon('../img/web.jpg'), 'open', self)
        openAction.setShortcut('ctrl+o')
        openAction.setStatusTip('open a file')
        openAction.triggered.connect(self.openAction)

        # 检查文件
        checkAction = QAction(QIcon('../img/web.jpg'), 'check', self)
        checkAction.setShortcut('ctrl+q')
        checkAction.setStatusTip('check the file')
        checkAction.triggered.connect(self.checkAction)

        # 训练视图
        trainAction = QAction(QIcon('../img/web.jpg'),'train',self)
        trainAction.setShortcut('ctrl+t')
        trainAction.setStatusTip('view training')
        trainAction.triggered.connect(self.trainAction)

        # 程序设置
        setAction = QAction(QIcon('../img/web.jpg'), 'setting', self)
        setAction.setShortcut('ctrl+alt+s')
        setAction.setStatusTip('Edit setting')
        setAction.triggered.connect(self.setAction)

        # 菜单项
        menu = self.menuBar()
        file = menu.addMenu('&file')
        train = menu.addMenu('&train')
        setting = menu.addMenu('&setting')

        # 菜单的Action
        file.addAction(openAction)
        file.addAction(checkAction)
        train.addAction(trainAction)
        setting.addAction(setAction)

        # 状态栏
        self.statusBar()

        # 内容显示区和邮件类型栏
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.createDockWindows()

    # 打开行为模式
    def openAction(self):
        try:
            fname = QFileDialog.getOpenFileName(self,'open file',r'F:/学习杂件/程序/python/mailAnalyse/data')
            if re.compile(r'normal').findall(fname[0]) or re.compile(r'trash').findall(fname[0]):
                self.contentShow(fname[0])
                self.currentFile = fname[0]
            else:
                self.showMessage('not a fit file')
        except:
            self.showMessage('wrong with fileOpen')


    # 检查文件行为模式
    def checkAction(self):
        try:
            tool = ToolKit()
            message,judgeResult = tool.analyse(self.currentFile)

            # 需要添加进度条和subject与内容的对应
            # 最好是多线程
            # true表示normal
            if self.currentFile in self.currentTrash or self.currentFile in self.currentNormal:
                self.showMessage(message)
                return None

            if judgeResult:
                self.currentNormal.append(self.currentFile)
                self.normalSub.append(self.subject)
                self.normalList.addItem(self.subject)
            else:
                self.currentTrash.append(self.currentFile)
                self.trashSub.append(self.subject)
                self.trashList.addItem(self.subject)

            self.showMessage(message)
        except:
            pass

    # 显示设置界面
    def setAction(self):
        setWindows = MySetting()
        MainGui.windowsList.append(setWindows)
        setWindows.move(self.x()+40,self.y()+40)
        setWindows.show()


    # 显示数据分析统计界面，主要为各种图表
    def trainAction(self):
        trainWindows = MyTraining()
        MainGui.windowsList.append(trainWindows)
        trainWindows.move(self.x()+150,self.y()+150)
        trainWindows.show()


    # 右侧列表
    def createDockWindows(self):
        # 正常邮件部分
        dock = QDockWidget("normal",self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # 设置属性,
        self.normalList = myListWidget(dock)
        self.normalList.setDragEnabled(True)
        self.normalList.setAcceptDrops(True)

        # 添加列表内容
        # 默认打开一些正常邮件，显示内容为主题，点击主题时，获得文件名，进而展现内容
        self.normalSub = self.getSubject('normal')
        self.normalList.addItems(self.normalSub)
        dock.setWidget(self.normalList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        # 垃圾邮件部分
        dock = QDockWidget("trash",self)
        self.trashList = myListWidget(dock)
        self.trashList.setDragEnabled(True)
        self.trashList.setAcceptDrops(True)

        self.trashSub = self.getSubject('trash')
        self.trashList.addItems(self.trashSub)
        dock.setWidget(self.trashList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        self.normalList.itemClicked.connect(self.normalShow)
        self.trashList.itemClicked.connect(self.trashShow)

        self.normalList.itemChanged.connect(self.normalChange)
        self.trashList.itemChanged.connect(self.trashChange)

    # currentRowChanged 源被触发
    # currentItemChanged 源被触发
    # itemEntered 源被触发
    # itemChanged 目的被触发

    def getSubject(self,type='normal'):
        tool = ToolKit()
        l = []
        if type == 'normal':
            for i in range(3):
                filePath = 'F:/学习杂件/程序/python/mailAnalyse/data/normal/' + str(i + 1)
                tool.fileContent(filePath)
                l.append(tool.subject)
                self.currentNormal.append(filePath)
        else:
            for i in range(3):
                filePath = 'F:/学习杂件/程序/python/mailAnalyse/data/trash/' + str(i + 1)
                tool.fileContent(filePath)
                l.append(tool.subject)
                self.currentTrash.append(filePath)
        return l


    # 弹窗显示消息
    def showMessage(self,s='it is a bug'):
        message = QMessageBox()
        message.setText(s)
        message.exec_()

    # 显示列表中对应的邮件
    def normalShow(self):
        item = self.sender().currentRow()
        self.contentShow(self.currentNormal[item])
        self.currentFile = self.currentNormal[item]

    def trashShow(self):
        item = self.sender().currentRow()
        self.contentShow(self.currentTrash[item])
        self.currentFile = self.currentTrash[item]

    # 此时源处和目的处均有动静，已经知道了原处的位置，剩下就是当前的,dropEvent发生在itemchange之后
    # 移动到normalList时触发
    def normalChange(self,e):
        text = e.text()
        # 通过subject，发现源和目地行数
        srow = self.trashSub.index(text)
        drow = self.normalList.row(e)

        # 在文件名列表中增减
        f = self.currentTrash[srow]
        self.currentNormal.insert(drow,f)
        self.currentTrash.remove(f)

        self.trashSub.remove(text)
        self.normalSub.insert(drow,text)
        # 以下对于行数的获取比较有用
        # pd = self.normalList.row(e)     # 获取
        # ps = self.trashList.
        # print(pd,ps)
        # c = self.currentTrash[self.trashList.item]
        # print(c)
        # self.currentNormal.insert(p,c)
        # del self.currentTrash[self.trashList.item]
        # self.normalList.item = None

    def trashChange(self,e):
        text = e.text()
        # 通过subject，发现源和目地行数
        srow = self.normalSub.index(text)
        drow = self.trashList.row(e)

        # 在文件名列表中增减
        f = self.currentNormal[srow]
        self.currentTrash.insert(drow,f)
        self.currentNormal.remove(f)
        # subject也需要变化
        self.normalSub.remove(text)
        self.trashSub.insert(drow,text)

    # 给定文件时，在textEdit中显示信息
    def contentShow(self,fname=None):
        try:
            tool = ToolKit()
            text = tool.fileContent(fname)
            self.subject = tool.subject
            if text == '':
                raise
            self.textEdit.setText(text)
        except:
            self.showMessage('wrong with showing content')


# 用于测试该程序
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    

    with open('./img/coffee.qss', 'r') as f:
        app.setStyleSheet(f.read())
    gui = MainGui()
    gui.show()
    sys.exit(app.exec_())
