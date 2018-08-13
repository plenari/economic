# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:18:35 2018
@author: omf
------------------------
talib
"""

try:
    import rqdatac 
    from rqdatac import *
    rqdatac.init()
except:
    pass
import talib
from conf import conf
import pandas as pd
import numpy as np
from sklearn import preprocessing


def get_all_talib_func_inputs():
    '''
    得到talib所有函数及其输入内容
    过滤掉了，输入real0，real，close0等函数
    
    return :
        {'AD': 'high, low, close, volume',
         'ADOSC': 'high, low, close, volume',
         'ATR': 'high, low, close',}   
    
    '''
    func_inputs={}
    talibs=[i for i in dir(talib) if i.upper()==i and not i.startswith('__')]
    for i,tal in enumerate(talibs):
        doc=eval('talib.{}.__doc__'.format(tal))
        doc=[i.strip() for i in  doc.split('\n\n') if i.strip().startswith('{}'.format(tal))][0]
        
        if '[' in doc:
            c=doc.split('[')[0].split('(')[1]
        else:
            c=doc.split(')')[0].split('(')[1]
    
        func_inputs[tal]=c
    
    #删除掉real 或者0出现的地方
    notneed=[]
    for i in func_inputs:        
        j=func_inputs[i]
        if 'real' in j or '0' in j :
            notneed.append(i)
            
    for  i in notneed:
        func_inputs.pop(i)
    return func_inputs




def cal_talib(df):
    '''    
    按照symbls分组计算talib所有指标，调用cal_talib_single实现
    '''
    for i,df_ in enumerate(df.groupby('symbol')):
        ins,df_=df_    
        if i==0:
            '''第一只股票是基准，之后的都跟这个合并
            '''
            tal=cal_talib_single(df_,ins)
        else:
            '''
            之后股票数据都和这个合并
            '''
            tal_=cal_talib_single(df_,ins)
            
            tal=pd.concat([tal,tal_],axis=0)        
    tal=tal.dropna(axis=1,how='all').reset_index(drop=True)
    return tal


def cal_talib_single(df,ins,normal=True):
    '''
    ins：计算单只股票的talib指标
    df ,必须包含以下变量。
    '''
    open,high =df.open.values,df.high.values, 
    low, close=df.low.values, df.close.values
    volume=df.volume.values
    
    tals=pd.DataFrame()
    func_inputs=get_all_talib_func_inputs()
    for i,j in func_inputs.items():
        '''
        计算所有的技术指标
        '''
        func=getattr(talib,i)
        returns=func(*eval(j))
        if isinstance(returns,np.ndarray):     
            '''
            如果是ndarray,就判断方差是否大于某一个值，
            然后是否保存到数据内
            '''
            if np.std(returns)>0.9*0.1:#
                if normal:
                    tals[i]=preprocessing.scale(returns)
                else:
                    tals[i]=returns
            else:
                continue
            
    tals['symbol']=ins
    tals['date']=df.date.values
    return tals


def talib_main(price):
    '''
    提示函数怎么使用
    '''
    tal=cal_talib(price)
    #删掉有效值少于0.9的列
    tal=tal.dropna(thresh=0.9*tal.shape[0],axis=1).fillna(0.0)
    #和价格合并
    tal=pd.merge(price,tal,on=['date','symbol'],how='inner')
    return tal





