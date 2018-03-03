import sys
sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\interface')
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QHBoxLayout,QPushButton,QTabWidget,QMessageBox
from interface import ToolKit

class MyTraining(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('train')
        self.view = QTabWidget()
        self.view.addTab(self.train(),'train view')
        self.view.addTab(self.data(),'data view')
        self.setCentralWidget(self.view)

    def train(self):
        w = QWidget()
        layout= QHBoxLayout()
        scatterButton = QPushButton('scatter view')
        barButton = QPushButton('bar view')
        learnButton = QPushButton('learn view')
        createButton = QPushButton('create')

        scatterButton.clicked.connect(self.trainAction)
        barButton.clicked.connect(self.trainAction)
        learnButton.clicked.connect(self.trainAction)
        createButton.clicked.connect(self.trainAction)

        layout.addWidget(scatterButton)
        layout.addWidget(barButton)
        layout.addWidget(learnButton)
        layout.addWidget(createButton)
        w.setLayout(layout)

        return w

    def data(self):
        w = QWidget()
        layout = QHBoxLayout()
        wordButton = QPushButton('word cloud')
        senderButton = QPushButton('sender rank')
        ipButton = QPushButton('ip rank')

        wordButton.clicked.connect(self.dataAction)
        senderButton.clicked.connect(self.dataAction)
        ipButton.clicked.connect(self.dataAction)

        layout.addWidget(wordButton)
        layout.addWidget(senderButton)
        layout.addWidget(ipButton)
        w.setLayout(layout)

        return w

    def trainAction(self):
        sender = self.sender().text()
        tool = ToolKit()
        s = tool.trainView(sender)
        if s:
            self.showMessage(s)


    def dataAction(self):
        sender = self.sender().text()
        tool = ToolKit()
        tool.dataView(sender)

    def showMessage(self, s):
        message = QMessageBox()
        message.setText(s)
        message.exec_()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    train = MyTraining()
    train.show()
    sys.exit(app.exec_())