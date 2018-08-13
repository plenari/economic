# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 16:58:24 2018

@author: omf
"""
import pandas as pd
import D


his=D.history_datas(instruments, start_date, end_date,fields)
fea=D.features(instruments, start_date, end_date,features)
data=pd.merge(his,fea,on=['date','instrument'],how='inner')
df=df.set_index('date',drop=True)

class conf:
    pass



def deal_instrument(df):
    '''
    一个完整的一只股票的数据
    '''
    result=[]
    
    for i,d in  enumerate(df.groupby(by='instrument')):
        d['return']=100*(d['close'].shift(-5) / df['open'].shift(-1)-1)
    

