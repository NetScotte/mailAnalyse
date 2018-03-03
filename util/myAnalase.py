import re


# 需要忽略大小写，现在时和过去式的一些基本情况，复数等
# 此模块涉及很多字符串，字典，列表，以及文件读取的很多方法，可供以后借鉴
class MyAnalyse:
    def __init__(self):
        self.content=''                     # 用来保存待处理对象，英文文本
        self.wordlist=[]                    # 用来保存文本中的单词
        self.wordValue=[]                   # 用来保存单词对应的值，来源于网上的词频
        self.jiange=re.compile(r'\w*\s')    # 用来匹配单词，单词以空格等分开
        self.wordDict={}                    # 用来保存网上的词频
        # self.unuse=['in','at','on','between','beside','near','from','to','under','behind','across','along','among','down',
        #             'beneath','below','about','before','after','by','on','at','in','over','through','for','with','besides',
        #             'but','except','as','like','above','against','accord','despite','in spite of','not','it','itself','he',
        #             'him','i','am','is','were','are','do','she','her','herself','himself','my','myself','me','us'',''we','you',
        #             'they','them','his','and','or','do','yes']

        self.unuse=[]
        with open('../data/unword','r') as f:
            for i in f:
                i =i.strip('\n')
                self.unuse.append(i)

        # 从文件中读取从网上下载的词频
        with open('../data/wordFre.txt','r') as f:
            for i in f:
                l = i .split()
                try:
                    self.wordDict[l[3]] = float(l[7])
                except:
                    self.wordDict[l[3]] = 0.4
                    continue


    # 初始找到所有的词
    def analyse(self,content):
        if content:
            self.content=content
            self.wordlist = self.jiange.findall(content)
        self.normalword()

    # 处理词，正规化，同时统计词的词频
    def normalword(self):
        l = len(self.wordlist)
        for i in range(l):
            self.wordlist[i] = self.wordlist[i].strip(' ')          # 去掉前后的空格
            self.wordlist[i] = self.wordlist[i].strip('\n')         # 去掉换行符
            self.wordlist[i] = self.wordlist[i].strip(r'\d*')       # 去掉前后的数字，对纯数字无效
            self.wordlist[i] = self.wordlist[i].lower()             # 全部变为小写
            # 处理字符串列表中的复数
            s = self.wordlist[i]
            if s.endswith(('s', 'ing', 'ed')):
                nos = s.rstrip('s')
                noing = s.rstrip('ing')
                noed = s.rstrip('ed')
                noes = s.rstrip('es')
                inge = noing+'e'
                yies = noes.rstrip('i')+'y'
                if self.wordDict.get(nos):
                    self.wordlist[i] = nos
                if self.wordDict.get(noing):
                    self.wordlist[i] = noing
                if self.wordDict.get(noed):
                    self.wordlist[i] = noed
                if self.wordDict.get(noes):
                    self.wordlist[i] = noes
                if self.wordDict.get(inge):
                    self.wordlist[i] = inge
                if self.wordDict.get(yies):
                    self.wordlist[i] = yies

            # 以相似来处理字符串，这样效果会好一些，中间可以有一次不相同，如果相似个数大于一半，那么就一样
            # l = range(min(len(a), len(b)))
            # ab = 0
            # for i in l:
            #     if list(a)[i] != list(b)[i]:
            #         ab += 1
            #         if a == 2:
            #             break
            #     tag = i
            #
            # if tag > max(len(a), len(b)) / 2:
            #     print('a is equal b')

            if self.wordlist[i].isdigit():
                self.wordlist[i] = ''
            if self.wordlist[i] in self.unuse:
                self.wordlist[i] = ''

        l = len(self.wordlist)
        count = 0
        for i in range(l):
            i = i-count
            if not self.wordlist[i]:
                del self.wordlist[i]
                count +=1

        self.giveWeight()

    def giveWeight(self):
        self.onlyDict={}                # 用来存储当前对象的词与权重

        # 构建self.onlyDict,确定字符串的长度，确定两个的相似度，大于80%即为一个
        for i in range(len(self.wordlist)):
            s=self.wordlist[i]
            if not s in self.onlyDict:
                try:
                    self.onlyDict[s] = self.wordDict[s]
                except:
                    self.onlyDict[s] = 0.7          # 如果不存在该词，给予0.7的值
                    continue

        # 测试onlyDict
        #  print(onlyDict)

        # 对onlyDict进行排序
        newDict=dict(sorted(self.onlyDict.items(),key=lambda asd:asd[1],reverse=False))
        self.onlyDict=newDict

    def get_wordList(self,num=20):
            l=[]
            count=0
            for key in self.onlyDict:
                if count >=num:
                    break
                l.append(key)
                count +=1
            return l

    def get_wordArray(self,num=20):
        l=[]
        count = 0
        for key in self.onlyDict:
            if count >= num:
                break
            l.append(self.onlyDict[key])
            count += 1
        return l




# 此部分用于单独检测此模块的功能
if __name__ == '__main__':
    content = '''
Position: Component Engineer
Location: Beijing
Internship status: Long term
1    MAIN TASKS
·    Take full responsibility for component related issues in the organization
·    Communicate with Ericsson global engineers for component related issues
·    Enforce Ericsson, national and industry requirements about components
·    Handle other component related work
2    QUALIFICATION
·    Bachelor or master degree of first level University (Engineering background is preferred)
·    Fluent in English speaking and writing
·    Comprehensive knowledge of technologies
·    Strong communication skill
·    Plenty of knowledge about electronic components
·    Initiative and positive personal personality
·    Willing to focus on the technology field and be the specialist in the component area
·    At least 3 days available per week
·    Graduate next year preferred
If interested, please send your resume both in Chinese and English to Jin.xx.pu@ericsson.com or liyang.xx.suo@ericsson.com
    '''
    analyse = MyAnalyse()
    analyse.analyse(content)
    print(analyse.get_wordList())