import sys
sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\util')
import pickle
from MailInfo import MailInfo
from MailAttribute import MailAttribute

#test for pickle dump and load
# Xnormal=[['1','2'],['a','b']]
# with open('../data/normalList','wb') as f:
#     pickle.dump(Xnormal,file=f)
# with open('../data/normalList','rb') as f:
#     list=pickle.load(f)
# print(Xnormal)
# print(list)

# define the number of mail for using, 8000 for all
def creatList(num=6000):
    Xnormal=[]
    Xtrash=[]

    # tag=0
    for i in range(num):
        # if tag>=10:
        #     break
        # if i>470:
        #     tag +=1
        normal_mail=MailInfo(type='normal',fileName='{0}'.format(i+1))
        attribute=MailAttribute(normal_mail.get_content()).get_attribute()
        Xnormal.append(attribute)
        # if not attribute:
        #     print('normal{0} is empty'.format(i))
        # if i>470:
        #     print(attribute)

        trash_mail = MailInfo(type='trash', fileName='{0}'.format(i+1))
        attribute = MailAttribute(trash_mail.get_content()).get_attribute()
        Xtrash.append(attribute)
        # if not attribute:
        #     print('trash{0} is empty'.format(i))
        # if i>470:
        #     print(attribute)
        #     print()
    with open('../data/normalList','wb') as f:
        pickle.dump(Xnormal,f)

    with open('../data/trashList','wb') as f:
        pickle.dump(Xtrash,f)

if __name__ == '__main__':
    creatList()
    # with open('../data/normalList','rb') as f:
    #     Xnormal = pickle.load(f)
    #     print(Xnormal[190])
    #     print(Xnormal[191])
    #
    # with open('../data/trashList','rb') as f:
    #     Xtrash = pickle.load(f)
    #     print(Xtrash[190])
    #     print(Xtrash[191])
