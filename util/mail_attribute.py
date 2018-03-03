import jieba.analyse
from mail_info import MailInfo
from myAnalase import MyAnalyse


class MailAttribute:
    def __init__(self, content):
        self.content=content
        self.attribute =[]
        self.array = []

    def get_attribute(self,num=20):
        self.attribute = jieba.analyse.extract_tags(self.content, topK=num, allowPOS=('ns', 'n', 'vn', 'v'))
        if self.attribute:
            word = ['来源', '水木社区', '发信人', '发信站', '标题', '信区','水木','社区']
            self.attribute=[s for s in self.attribute if s not in word]
        else:
            analyse = MyAnalyse()
            analyse.analyse(self.content)
            self.attribute = analyse.get_wordList(num)
        return self.attribute

    # 获取权重
    def get_array(self,num=20):
        self.attribute = jieba.analyse.extract_tags(self.content, topK=20,withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
        if self.attribute:
            self.array=[value for key,value in self.attribute]
        else:
            analyse = MyAnalyse()
            analyse.analyse(self.content)
            self.array = analyse.get_wordArray(num)
        return self.array


if __name__ == "__main__":
    testinfo = MailInfo()
    for i in range(1,101):
        if i % 10 ==0:
            file_path = 'F:/学习杂件/程序/python/dataset/data/trash/%s'% i
            testinfo.analyseMail(file_path)
            myclass=MailAttribute(testinfo.get_content())
            print('number:',i)
            print(myclass.get_attribute())

