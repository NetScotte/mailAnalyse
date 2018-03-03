import sys
sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\util')
sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\Gui')
from mail_info import MailInfo
from judge_ip import Judge
from rule import Rule
from mail_attribute import MailAttribute
from attributeTodict import AToD
from judge_content import JudgeContent
from pltView import SVCView
from dataView import dataAnalyse
from createMachine import create


# 该模块为用户界面与后台分析处理模块之间的传递和组装工具
class ToolKit:
    def __init__(self):
        self.showcontent=''
        self.subject = ''

    # 获取文件内容，用于在主界面的textEdit中展示
    def fileContent(self,filename=None):
        try:
            mail = MailInfo()
            mail.analyseMail(filename)
            content = mail.get_content()
            subject = mail.get_subject()
            sender = mail.get_sender()
            # self.showcontent = 'subject:' + subject + '\r\n' + \
            #                    'from:' + sender + '\r\n' + \
            #                    'content:' + '\r\n' + \
            #                    content
            # self.subject = subject
            if content is None and subject is None and sender is None:
                return self.showcontent
            else:
                self.showcontent = 'subject:'+subject+'\r\n'+ \
                                'from:'+ sender + '\r\n'+ \
                                'content:'+'\r\n' + \
                                    content
                self.subject = subject
        except:
            return self.showcontent

        return self.showcontent

    # 调用各个分析工具，进行分析判断。
    # 包括根据黑白名单分析，根据ip分析，根据内容使用SVC分析，工作量大
    # True表示normal,False表示trash
    def analyse(self,filename=None):
        message = {}

        # 调用mailAnalyse中的各个模块，进行分析和返回结果
        mail = MailInfo()
        mail.analyseMail(filename)
        ip = mail.get_ip()                  # 使用ip进行联网判断
        sender = mail.get_sender()         # 使用sender进行黑白名单判断
        c = mail.get_content()        # 使用content进行机器学习的判断

        # 判断是否存在于名单中，存在直接返回，否则进行下一步
        try:
            r = Rule()
            judgeResult = r.find(sender)
            if judgeResult:
                r.content(c)
            message['rule'] = r.getInfo()
            if judgeResult is False:
                return str(message),judgeResult
            elif judgeResult is True:
                return str(message),judgeResult
        except:
            message['rule'] = 'wrong'

        # 判断是否被网站列为黑名单，正常则进行下一步，由于COOKIE问题，最容易出现问题
        try:
            judge = Judge()
            judgeResult = judge.is_spam(ip)
            message['ipInfo'] = judge.get_info()
            if not judgeResult:
                return str(message),judgeResult
        except:
            message['ipInfo'] = 'wrong'

        # 通过机器学习进行内容的判断
        try:
            strAttribute = MailAttribute(c).get_attribute()
            strAttribute = r.filter(strAttribute)
            numAtrribute = AToD().transfer_array(strAttribute)
            judgeResult = JudgeContent().judge(numAtrribute)
            message['machineJudge'] = str(judgeResult)
        except:
            message['machineJudge'] = 'wrong'

        # 组织信息，以便显示
        if judgeResult :
            info = 'rule:  '+message['rule']+'\r\n'+\
                'ipInfo:  '+message['ipInfo']+'\r\n'+\
                'machineJudge: normal'
        else:
            info = 'rule:  ' + message['rule'] + '\r\n' + \
                   'ipInfo:  ' + message['ipInfo'] + '\r\n' + \
                   'machineJudge:  trash'

        return info,judgeResult

    # 用于显示数据分析能力的图表
    def trainView(self,sender):
        X = AToD().get_Xdata(3000)  # 获得数据，包括特征向量和类型
        v = SVCView(X)
        if sender == 'scatter view':
            v.scatterView()
        if sender == 'bar view':
            v.barView()
        if sender == 'learn view':
            v.learnView()
        if sender =='create':
            c = create(3000)
            c.initData()
            s = c.train()
            return s

    # 用于统计邮件信息
    def dataView(self,sender):
        try:
            d = dataAnalyse()
            if sender == 'word cloud':
                d.wordShow()
            if sender =='sender rank':
                d.senderShow()
            if sender =='ip rank':
                d.ipShow()
        except:
            pass

if __name__ == '__main__':
    tool = ToolKit()
    filePath = 'F:/学习杂件/程序/python/dataset/data/trash/1'
    # message , judgeResult = tool.analyse(filePath)
    # print(message)
    # print(judgeResult)

    # fname = 'F:/学习杂件/程序/python/mailAnalyse/data/normal/3'
    # tool = ToolKit()
    text = tool.fileContent(filePath)
    print(text)