#coding=utf-8
from lstm import lstm
import numpy as np
import pandas as pd
import tensorflow as tf
import datetime
import matplotlib.pylab as plt
import os

os.chdir(r'F:\app\anaconda\Lib\site-packages\rqalpha\myself\ricequant\industry_lstm')

    
#clf = lstm()


##开始计算数据
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

def cal_industry_increase_hisory(all_cap,day='2018-03-14'):
    '''
    计算与某天相比的涨幅。
        计算index为股票，columns 为日期，
        日期升序排列。   get_market_cap 的返回值
        day 为作为基准的日期
    return pd.DataFrame
    '''
    all_cap=all_cap.T.sort_index().T
    cap=all_cap.sum(axis=0)
    cap=cap/cap[day]
    return cap


start='2017-01-01'
end='2018-04-11'
#ins=pd.read_csv(r's{}-e{}-instruments.csv'.format(start,end),index_col=0)
#close=pd.read_csv(r's{}-e{}-close.csv'.format(start,end),index_col=0)
#cap=pd.read_csv(r's{}-e{}-market_cap.csv'.format(start,end),index_col=0)
#筛选相同的股票列表
#sids=sorted(list(set(set(ins.index)&set(close.index)&set(cap.index))))
#ins=ins.loc[sids]
#close=close.loc[sids]
#cap=cap.loc[sids]
#close=close.fillna(0)
#cap=cap.fillna(0)

#4.计算所有版块的日涨幅
#industry_day_increase=cap.groupby(ins.industry_name).apply(cal_industry_increase_day).unstack()
#如果行业涨幅是Nan，就用-0.1代替
#industry_day_increase=industry_day_increase.fillna(-0.1)
#5.行业涨幅都已经获得，就需要排名
rank_industry=industry_day_increase.apply(np.argsort,axis=0)

train=
test=rank_industry.iloc[]


clf = lstm()
trainX=np.random.randn(1000,15,20)
trainY=np.round(np.random.randint(0,6,1000))
clf.fit(trainX, trainY)
re=clf.pred(np.random.randn(10,15,20))
print(np.array(re).mean())





