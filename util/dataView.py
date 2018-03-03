from mail_info import MailInfo
from mail_attribute import MailAttribute
import pickle
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class dataAnalyse:
    def __init__(self):
        self.num=2000             # 统计数据来源的邮件数量
        self.sender = {}        # 统计key,value
        self.ip = {}
        self.word = {}
        self.readData()         # 如果需要更新数据请手动调用initData

    # 如果已经保存了文件，可以跳过此步
    def initData(self):
        for i in range(self.num):
            file = 'F:/学习杂件/程序/python/mailAnalyse/data/normal/'+str(i+1)
            mail = MailInfo()
            mail.analyseMail(file)
            ip = mail.get_ip()
            sender = mail.get_sender()
            attr = MailAttribute(mail.get_content()).get_attribute()
            # 积累key,value
            try:
                self.ip[ip] += 1
            except:
                self.ip[ip] = 1

            try:
                self.sender[sender] += 1
            except:
                self.sender[sender] = 1

            for i in attr:
                try:
                    self.word[i] += 1
                except:
                    self.word[i] = 1

        self.dataRank()

    # 对各个字典进行排序,分析数据。可以强化功能ip的分析
    def dataRank(self):

        # 统计10个ip,对于ip的分析，可以增加相似度比较，如果前三个相似，前两个相似都可以打印出来作为结果
        newDict = dict(sorted(self.ip.items(), key=lambda asd: asd[1], reverse=True))
        i = 0
        self.ip = {}
        for key in newDict:
            if i<10:
                self.ip[key] = newDict[key]
                i += 1
            else:
                break

        # 统计10个sender
        newDict = dict(sorted(self.sender.items(), key=lambda asd: asd[1], reverse=True))
        i = 0
        self.sender={}
        for key in newDict:
            if i<10:
                self.sender[key] = newDict[key]
                i +=1
            else:
                break

        # 统计30个词语
        newDict = dict(sorted(self.word.items(), key=lambda asd: asd[1], reverse=True))
        i = 0
        self.word = {}
        for key in newDict:
            if i <300:
                self.word[key] = newDict[key]
                i += 1
            else:
                break

        self.saveData()

    # 数据保存
    def saveData(self):
        with open('F:/学习杂件/程序/python/dataset/data/ipRank','wb') as f:
            pickle.dump(self.ip , f)

        with open('F:/学习杂件/程序/python/dataset/data/senderRank','wb') as f:
            pickle.dump(self.sender,f)

        with open('F:/学习杂件/程序/python/dataset/data/wordRank','wb') as f:
            pickle.dump(self.word,f)


    def readData(self):
        with open('F:/学习杂件/程序/python/dataset/data/ipRank', 'rb') as f:
            self.ip = pickle.load(f)

        with open('F:/学习杂件/程序/python/dataset/data/senderRank', 'rb') as f:
            self.sender = pickle.load(f)

        with open('F:/学习杂件/程序/python/dataset/data/wordRank', 'rb') as f:
            self.word = pickle.load(f)

    # 图形化展示
    def senderShow(self):
        labels = []
        sizes = []
        for key in self.sender:
            labels.append(key)
            sizes.append(self.sender[key])

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')

        plt.show()


    def wordShow(self):
        wc = WordCloud(font_path='C:/Windows/Fonts/STXINGKA.TTF',background_color='white')
        wc.generate_from_frequencies(self.word)
        plt.imshow(wc)
        plt.axis('off')
        plt.show()


    def ipShow(self):
        labels = []
        sizes = []
        for key in self.ip:
            labels.append(key)
            sizes.append(self.ip[key])

        # explode = (0, 0.1, 0, 0)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')

        plt.show()

# 来源于官网的参考文件
# import matplotlib.pyplot as plt
#
# # Pie chart, where the slices will be ordered and plotted counter-clockwise:
# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# sizes = [15, 30, 45, 10]
# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
#
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#
# plt.show()


if __name__ == '__main__':
    d = dataAnalyse()
    # d.initData()
    # d.wordShow()
    d.ipShow()