import re

# 该模块用于判断邮件是否满足黑白名单，注白名单关键字在属性提取中体现
class Rule:
    def __init__(self):
        self.blackSender = []
        self.whiteSender = []
        self.blackWord=[]
        self.whiteWord=[]
        self.message = ''
        self.m = re.compile(r'@')           # 用来匹配邮件发送者，匹配联系人
        self.init()


    # 用来从文件中读取信息初始化前面的变量，如果文件不存在会出现异常
    def init(self):
        with open('../data/blackList','r') as f:
            for i in f:
                i = i.strip('\n')
                if self.m.findall(i):
                    self.blackSender.append(i)
                else:
                    self.blackWord.append(i)
        with open('../data/whiteList','r') as f:
            for i in f:
                i = i.strip('\n')
                if self.m.findall(i):
                    self.whiteSender.append(i)
                else:
                    self.whiteWord.append(i)


    # 判断发送者是否在名单中，如果位于黑名单，返回False,否则返回True
    def find(self,sender):
        if sender:
            if sender in self.blackSender:
                self.message = 'sender is listed in blackSender'
                return False
            if sender in self.whiteSender:
                self.message = 'sender is listed in whiteSender'
                return True
        self.message = 'allRight'
        return None

    # 判断邮件内容是否包含黑名单关键字，包含则返回False
    def content(self,c):
        for i in self.blackWord:
            m = re.compile(i)
            if m.findall(c):
                self.message += 'mail has black word'
                return False
        return None

    def filter(self,s):
        for i in self.whiteWord:
            while i in s:
                s.remove(i)
        return s

    # 返回一些信息
    def getInfo(self):
        return self.message

if __name__ == '__main__':

    # sender = ''
    # c=''
    # message={}
    #
    # r = Rule()
    # judgeResult = r.find(sender)
    # if not judgeResult is False:
    #     r.content(c)
    # message['rule'] = r.getInfo()
    # if judgeResult is False:
    #     print(str(message), judgeResult)
    # elif judgeResult is True:
    #     print(str(message), judgeResult)

    r = Rule()
    print(r.whiteWord)
    print(r.whiteSender)
    print(r.blackWord)
    print(r.blackSender)