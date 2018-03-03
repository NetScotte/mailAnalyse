import jieba
from mail_info import MailInfo

class MyIDF:
    def __init__(self):
        self.IDFname=''
        self.num=6000
        self.wordDict={}

    def creatIDF(self):
        for i in range(self.num):
            myinfo = MailInfo(fileName='{0}'.format(i+1))
            wordlist = jieba.cut(myinfo.get_content())
