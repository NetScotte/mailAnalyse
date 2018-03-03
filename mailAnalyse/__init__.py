import sys
sys.path.append(r'F:\学习杂件\程序\python\mailAnalyse\util')
from sklearn.cross_validation import KFold
from sklearn import svm
from mail_info import mail_info
from mail_attribute import mail_attribute

#获得属性列表并进行训练
X=[]
Y=[]
for i in range(10):
    info=mail_info(type='normal',fileName='{0}'.format(i+1))
    attribute=mail_attribute(info.get_content()).get_attribute()
    X.append(attribute)
    Y.append(1)

for i in range(10):
    info = mail_info(type='trash', fileName='{0}'.format(i+1))
    attribute = mail_attribute(info.get_content()).get_attribute()
    X.append(attribute)
    Y.append(0)

for i in range(20):
    print(X[i])

# kf=KFold(20,n_folds=3,random_state=1)
# for train,test in kf:
#     for index in train:
#         print(X[index])
#     break

