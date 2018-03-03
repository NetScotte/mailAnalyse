import pickle


# 想不到列表可以存这么多东西，速度还是很快的，使用6000封即可
# 显然不能直接将字符串形式的属性投入训练，那么就需要考虑将属性转换为数组，那么显然为字典，
class AToD:
    def __init__(self,num=3000):
        assert num<8000
        self.num = num       # 进行提取的邮件类别数量，按顺序提取，此数字为正常邮件和垃圾邮件的界限
        self.Xdict = {}      # 存放词语和对应值，用于将字符向量转为数值向量
        self.X = []          # 开始存放的是字符特征向量，后来利用词典转化为存放数值特征向量，数量为self.num

    # 从已保存的文件中读取词语与特征值的字典
    def get_wdict(self):
        with open('../data/Xdict','rb') as f:
            self.Xdict = pickle.load(f)
        return self.Xdict

    # 获取大量数值形式的特征向量,num表示需要的每类邮件的数量，不能超过预存储的6000封
    def get_Xdata(self,num=3000):
        assert num<6000
        with open('../data/Xarray','rb') as f:
            self.X = pickle.load(f)

        # 有两列，第一列表示数值向量，第二列表示类别，1 表示正常，0表示垃圾,交叉获取正常邮件和垃圾邮件
        rx=[[],[]]
        for i in range(num):
            rx[0].append(self.X[i])
            rx[1].append(1)
            rx[0].append(self.X[6000+i])
            rx[1].append(0)
        return rx

    # 传入字符串向量，返回其数值向量，数值与训练时获得的信息有关
    def transfer_array(self,attritube):
        self.get_wdict()
        if isinstance(attritube,list):
            for i in range(len(attritube)):
                    attritube[i] = self.Xdict[attritube[i]]
        return attritube

    # 获得字频self.Xdict列表和属性列表X，以及normal,trash,文件来自于attributeTofile.py
    def pro_file(self):
        # 正常邮件部分，
        with open('../data/normalList', 'rb') as f:         # normalList为邮件的词语特征向量，字符形式
            normal = pickle.load(f)
            for i in range(self.num):
                self.X.append(normal[i])
                nlen = len(normal[i])
                for j in range(nlen):
                    if normal[i][j] in self.Xdict:
                        self.Xdict[normal[i][j]] += 1
                    else:
                        self.Xdict[normal[i][j]] = 1

        # 垃圾邮件部分
        with open('../data/trashList', 'rb') as f:
            trash = pickle.load(f)
            for i in range(self.num):
                self.X.append(trash[i])
                tlen = len(trash[i])
                for j in range(tlen):
                    if trash[i][j] in self.Xdict:
                        self.Xdict[trash[i][j]] -= 1
                    else:
                        self.Xdict[trash[i][j]] = -1

        for i in range(2 * self.num):
            alen = len(self.X[i])
            for j in range(alen):
                self.X[i][j] = self.Xdict[self.X[i][j]]

        self.write_all()

    # 将相关信息写入文件，以便以后使用
    def write_all(self):
        # 将self.num封数值特征向量存储到文件中，
        with open('../data/Xarray', 'wb') as f:
            pickle.dump(self.X, f)

        # 将包含单词和权重的字典保存到文件中
        with open('../data/Xdict', 'wb') as f:
            pickle.dump(self.Xdict, f)


# # 这是数据准备阶段的文件生成部分
# if __name__ == '__main__':
#     mywork = AToD(6000)
#     mywork.pro_file()
#     # 以下用来检测文件是否可用
#     with open('../data/Xarray','rb') as f:
#         x=pickle.load(f)
#         print(x[6000:6010])
#
#
#     # with open('../data/Xdict','rb') as f:
#     #     y=pickle.load(f)
#     #     count=0
#     #     for i in y:
#     #         count+=1
#     #         print(i)
#     #         if count>=10:
#     #             break


# 测试此部分功能
if __name__ =='__main__':
    l = ['小虫子', '铁床', '拐棍', '尿不湿', '奶嘴', '重点班', '消毒柜',\
         '童床', '普通高中', '熬粥', '奶瓶', '掏腰包', '宜家', '厨师', '考上',\
         '奶粉', '拄着', '待遇', '号称', '奖励']
    print(AToD().transfer_array(l))