import re
from email.header import decode_header

'''
提取源ip地址，发送者邮箱地址，以及邮件正文
增加提取标题和发件人等信息
'''

class MailInfo:
    def __init__(self, type = 'trash', fileName = '2'):
        # 均为字符对象
        self.ip = ''
        self.sender = ''
        self.content = ''
        self.subject = ''
        self.filePath = '../data/'+type+'/'+fileName

    # 当给定文件内容后，用于分析其内容
    def analyseMail(self,filePath=None):
        if filePath is None:
            filePath = self.filePath

        rec_pattern = re.compile(r'Received:')                      # 匹配ip地址出现的字段
        sub_pattern = re.compile(r'Subject:.*')                       # 匹配主题出现的字段
        fro_pattern = re.compile(r'From:.*')                          # 匹配发送者出现的字段
        ip_pattern = re.compile(r'(\d{1,3}\.){3,3}\d{1,3}')        # 匹配字段中的ip地址
        sen_pattern = re.compile(r'<.*>')                         # 匹配字段中的<发送者邮箱>
        blank_pattern = re.compile(r'^$')                           # 匹配空行
        extra_pattern = re.compile(r'水木社区')

        # 定义正文开始标识和正文内容列表
        tag = 0
        lcontent = []
        senstr=''
        ipstr = ''
        # 逐行处理文件
        # 针对'F:\学习杂件\程序\python\dataset\data\trash\2'
        # 如果filepath为该值，则出现错误
        # 如果是../data/trash/2则正确
        with open(filePath, mode='rb') as f:
            for i in f:
                i=i.decode('gbk', errors='ignore')
                if tag == 0:
                    if rec_pattern.match(i) and not ipstr:
                        ipstr = ip_pattern.search(i)
                    if fro_pattern.match(i):
                        senstr = fro_pattern.search(i).group(0)
                    if sub_pattern.match(i):
                        try:
                            initialSub = sub_pattern.match(i).group(0).strip('Subject:')
                            bSub = decode_header(initialSub)[0][0]
                            code = decode_header(initialSub)[0][1]
                            self.subject = bSub.decode(code,'ignore').strip('Re:')
                        except:
                            continue
                    if blank_pattern.match(i):
                        tag = 1
                else:
                    if not extra_pattern.search(i):
                        lcontent.append(i)

            if sen_pattern.search(senstr):
                self.sender = sen_pattern.search(senstr).group(0).strip('<>')
            else:
                self.sender = senstr.strip('From: ')
            if ipstr:
                self.ip=ipstr.group(0)
            if lcontent:
                self.content=''.join(lcontent)

    def get_ip(self):
        return self.ip

    def get_sender(self):
        return self.sender

    def get_content(self):
        return self.content

    def get_subject(self):
        return self.subject


# 这里可以用来测试邮件信息的获取，包括发件人，邮件正文，邮件起始ip等
if __name__ == "__main__":
    testinfo = MailInfo()
    for i in range(1,101):
        if i % 10 ==0:
            file_path = 'F:/学习杂件/程序/python/dataset/data/trash/%s'% i
            testinfo.analyseMail(file_path)
            print('number:', i)
            print('发送人：', testinfo.get_sender())
            print('主题：', testinfo.get_subject())
            print('ip:', testinfo.get_ip())