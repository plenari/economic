#coding=utf-8
from lstm import lstm
import numpy as np
import pandas as pd
import tensorflow as tf
import datetime
import matplotlib.pylab as plt
import os
from sklearn.model_selection import train_test_split

os.chdir(r'F:\app\anaconda\Lib\site-packages\rqalpha\myself\ricequant\industry_lstm')
# 3. 计算所有板块
def cal_industry_increase_day(all_cap,n=1):
    '''
    计算每日相对于前n天涨跌幅。
        all_cap的index为股票，columns 为日期，
    return ，比输入少一天
        pd.DataFrame
        相对前一天的涨幅
    '''
    all_cap=all_cap.T.sort_index().T
    cap=all_cap.sum(axis=0)
    cap=cap.diff(n)/cap.shift(n)
    cap=cap.dropna()
    #不知道什么时候返回series
    return cap

start='2017-01-01'
end='2018-04-11'
ins=pd.read_csv(r's{}-e{}-instruments.csv'.format(start,end),index_col=0)
close=pd.read_csv(r's{}-e{}-close.csv'.format(start,end),index_col=0)
cap=pd.read_csv(r's{}-e{}-market_cap.csv'.format(start,end),index_col=0)
#筛选相同的股票列表
sids=sorted(list(set(set(ins.index)&set(close.index)&set(cap.index))))
ins=ins.loc[sids]
close=close.loc[sids]
cap=cap.loc[sids]
close=close.fillna(0)
cap=cap.fillna(0)

#4.计算所有版块的日涨幅
industry_day_increase=cap.groupby(ins.industry_name).apply(cal_industry_increase_day).unstack()
#如果行业涨幅是Nan，就用-0.1代替
industry_day_increase=industry_day_increase.fillna(-0.1)
#5.行业涨幅都已经获得，就需要排名
rank_industry=industry_day_increase.apply(np.argsort,axis=0)
#预测后一天的排名

X=rank_industry.iloc[:-1]
Y=rank_industry.iloc[1:]
x=X.T.values/80
y=Y.T.values/80

#Xtrain,Xtest,ytrain,ytest=train_test_split(x,y,test_size=0.25,shuffle=False)
#Xtrain,Xtest,ytrain,ytest=Xtrain.T,Xtest.T,ytrain.T,ytest.T


def create_x(x,y,step=20):
    '''从二维时间序列构建成三维的时间序列
    x:   np.array
        index应该是时间,columns是因子，也就是我的排名
        沿着那个轴产生一个row,step，inputs维度的数据
    return :
        如果 x.shape=300,80
        return [300-step,step,80]
    '''
    
    x,y=np.array(x),np.array(y)
    #把x改成需要的形状
    new_x=np.zeros([x.shape[0]-step,step,x.shape[1]])
    #把y改成需要的形状
    new_y=np.zeros([x.shape[0]-step,y.shape[1]])
    for i in range(new_x.shape[0]):
        '''
        '''  
        new_x[i]=x[i:i+step]
        new_y[i]=y[i+step]
    return new_x,new_y

x2,y2=create_x(x,y)  
xtrain,ytrain=x2[:-50],y2[:-50]
xtest,ytest=x2[-50:],y2[-50:]

#clf = lstm()
'''
clf.fit(xtrain, ytrain)
re=clf.pred(Xtrain,ytrain)
print(np.array(re).mean())


'''

