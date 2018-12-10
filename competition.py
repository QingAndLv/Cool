from numpy import *
import matplotlib.pyplot as plt
import math
def datahandel(file):
    with open(file,'r') as file:
        featnum=len(file.readline().split('\t'))
        datamat=[]
        labelmat=[]
        for eachline in file.readlines():
            dataline=[]
            datas=eachline.split('\t')
            if featnum == 39:
                for i in range(featnum-1):
                    dataline.append(float(datas[i]))
                datamat.append(dataline)
                labelmat.append(float(datas[-1]))
            else:
                for i in range(featnum):
                    dataline.append(float(datas[i]))
                datamat.append(dataline)
    return datamat,labelmat
def draw(predict,labelmat):
    x=[-3,-2,1,2,3]
    y = [-3, -2, 1, 2, 3]
    fig=plt.figure('线性回归')
    #一行一列第一块
    ax=fig.add_subplot(111)
    ax.scatter(labelmat,predict)
    ax.plot(x,y,'r')
    plt.show()
class regression():
    def standregres(datamat,labelmat):
        deter=mat(datamat).T*mat(datamat)
        # 此段检测行列式是否为零，若有为零的则得使用岭回归
        # if linalg.det(deter)==0:
        #     print('cannot do inverse')
        #     return 1
        # return 0
        w=deter.I*mat(datamat).T*mat(labelmat).T
        return w
    def locregres(datamat2,datamat,labelmat,k=1):
        predic=[]
        datanum=len(datamat)
        sinmat=eye((len(datamat[0])))
        lam=0.001
        for eachtest in datamat2:
            weights=eye((datanum))
            xmat=mat(datamat)
            for j in range(datanum):
                diff=eachtest-xmat[j,:]
                weights[j,j]=math.exp(math.sqrt(diff*diff.T)/(-2*k**2))
            xTx=xmat.T*(weights*xmat)+lam*sinmat
            if linalg.det(xTx)==0:
                print('cannot do inverse')
            w=xTx.I*(xmat.T*(weights*mat(labelmat).T))
            predic.append(float(eachtest*w))
            # print(w)
        return predic
    def lineregres(datamat,datamat2,labelmat):
        xmean=mat(datamat).T*ones((len(labelmat),1))/len(labelmat)#n行1列的矩阵
        re2=0
        ymean=sum(labelmat)/len(labelmat)
        re1=mat(datamat).T*mat(labelmat).T/len(labelmat)#n行1列的矩阵
        for i in range(len(labelmat)):
            re2+=float(mat(datamat[i])*mat(datamat[i]).T)
        m=(re1-ymean*xmean)/(re2/len(labelmat)-xmean.T*xmean)#n行1列
        c=ymean*ones((len(datamat[0]),1))-mat(array(m)*array(xmean))#n行1列
        predic=datamat2*m+c
        return predic
def error(predict,labelmat):
    num=0
    for i in range(len(labelmat)):
        num+=(float(predict[i])-float(labelmat[i]))**2
    return num/len(labelmat)
datamat,labelmat=datahandel(r'C:\Users\tcf\Desktop\zhengqi_train.txt')
datamat2,labelmat2=datahandel(r'C:\Users\tcf\Desktop\zhengqi_test.txt')
# datamat=delete(datamat,(19,21,29,5,11,25,22),axis=1)
# datamat=column_stack((datamat,array(ones((len(datamat),1)))))
datamat=c_[ones((len(datamat),1)),array(datamat)]
# datamat=delete(datamat,(22,20,26,30),axis=1)
# datamat2=delete(datamat2,(19,21,29,5,11,25,22),axis=1)
datamat2=c_[ones((len(datamat2),1)),array(datamat2)]
# datamat2=delete(datamat2,(22,20,26,30),axis=1)
w=regression.standregres(datamat,labelmat)
# print(w.shape)
# for i in range(len(w)):
#     print(str(w[i])+' '+str(i))
# predict=regression.lineregres(mat(datamat)[int(len(datamat)*0.2):int(len(datamat)),:],mat(datamat)[0:int(len(datamat)*0.2),:],array(labelmat)[int(len(datamat)*0.2):int(len(datamat))])
# print(w)
# w=ones((len(datamat[0]),1))
# first=error(mat(datamat)*w,labelmat)
# # print(str(first)+'\n')
# for i in range(len(w)):
#     w[i]-=0.01
#     second=(error(mat(datamat)*w,labelmat)-first)**2
#     # print(str(error(mat(datamat)*w,labelmat)))
#     w[i]+=0.02
#     third=(error(mat(datamat) * w,labelmat)-first)**2
#     # print(str(error(mat(datamat) * w,labelmat))+' '+str(i))
#     final=second+third
#     print(str(final)+' '+str(i))
#     w[i]-=0.01
# w=regression.locregres(mat(datamat)[int(len(datamat)*0.5):int(len(datamat)*0.7),:],mat(datamat)[0:int(len(datamat)*0.5),:],mat(labelmat)[0,0:int(len(datamat)*0.5)])
# print(w)
# print(mat(datamat2)*w)
# print(mat(datamat)*w)
with open(r'C:\Users\tcf\Desktop\1线性.txt','w') as f:
    # sqrt=[]
    # m=mean(labelmat)
    for i in mat(datamat2)*w:
        # f.write(str(i)+' '+str(labelmat[w.index(i)])+'\n')
        # sqrt.append((float(i)-float(labelmat[w.index(i)]))**2)
        f.write(str(i).lstrip('[').rstrip(']')+'\n')
    f.close()
#     # print(mean(sqrt))
# print(w)
# print(mat(datamat2)*w)
# draw(array(mat(datamat)*w),array(labelmat))
# print(m)C:\Python34\1\competition.py
