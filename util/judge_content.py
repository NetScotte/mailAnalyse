from sklearn import preprocessing
import pickle

# from mail_attribute import MailAttribute
# from attributeTodict import AToD
# from mail_info import MailInfo

# 传入属性向量，值为数组，数量<=20，加载机器学习模型，进行预测

class JudgeContent:
    def __init__(self):
        self.Xdata=[]           # 存储20个属性

    def judge(self,content):
        # 数据预处理部分
        l = len(content)
        try:
            for j in range(20 - l):
                content.append(content[j])
        except:
            while len(content) < 20:
                content.append(-1)

        # 可能是训练数据进行数据预处理为一正一负，所以这里进行数据处理时，需要负的作为陪伴
        self.Xdata.append(content)
        self.Xdata.append([-14, -31, -9, -16, -11, -67, -11, -12, 1, -15, -27, -16, -10, -10, -27, 39, -7, 193, -82, -14])
        self.Xdata = preprocessing.scale(self.Xdata)

        # 加载SVC模型，进行预测
        with open('../data/SVCmode', 'rb') as f:
            clf = pickle.load(f)
            self.result = clf.predict(self.Xdata[0])

        if self.result == [0]:
            return False
        else:
            return True


## 测试功能是否正常，是否能正常预测，必须先uncomment前面的import
# if __name__ == '__main__':
#     for i in range(20):
#         filePath = 'F:/学习杂件/程序/python/dataset/data/trash/'+ str(i+100)
#         m = MailInfo()
#         m.analyseMail(filePath)
#         content = m.get_content()
#         strAttribute = MailAttribute(content).get_attribute()
#         numAtrribute = AToD().transfer_array(strAttribute)
#         judgeResult = JudgeContent().judge(numAtrribute)
#         if judgeResult:
#             print('normal')
#         if not judgeResult:
#             print('trash')