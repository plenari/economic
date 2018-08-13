# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 13:11:07 2018

@author: omf
工具
"""
try:
    import rqdatac 
    from rqdatac import *
    rqdatac.init()
except:
    pass

import pandas as pd
import numpy as np
import pickle

def get_factors(path='./data/factor.pkl',book=None):
    '''
    from path find feature in book 
    
    >>>
    feather,feature_dict
    '''
    book=['income_statement_TTM','financial_indicator_TTM','cash_flow_statement_TTM']
    with open(path,'rb') as f:
        factor_name_all=pickle.load(f)
    result=[]
    for book_ in book:
        for row in factor_name_all[book_]:    
            result.append('fundamentals.{}.{}'.format(book_,row))
            
    return result,factor_name_all

def merge(price,facs):
    '''
    把price和facs按照date和symbols合并。
    '''
    #合并价格和因子数据
    data=pd.merge(price,facs,on=['date','symbol'],how='inner')   
    #删除列方向nan大于30%列
    data=data.dropna(axis=1,thresh=int(0.7*data.shape[0]))
    #删除行方向nan大于20%行
    data=data.dropna(axis=0,thresh=int(0.8*data.shape[1]))
    #还有nan却没被删除的，对该股票时间排序，然后用前一天补全，其余填充0
    data=data.groupby('symbol').apply(lambda x:x.sort_values('date').fillna(method='ffill')).fillna(0.0)
    data.index=data.index.droplevel()
    return data

def get_all_instruments(conf,type='CS'):
    '''
    股票池
    '''
    all_ins=all_instruments(type=type)#股票
    all_ins=all_ins.query('status=="Active"')#激活
    all_ins=all_ins.query('exchange=="XSHG"')#上证
    all_ins=all_ins[all_ins.symbol.apply(lambda x: not x.startswith('ST'))]#去掉st
    all_ins.set_index('order_book_id',drop=True,inplace=True)
    
    return all_ins.sort_index()

def change_factor_names(factors,filters):
    '''
    factor：因子完整名称
    filter:因子最后一个名称    
    
    >>>change_factor_names(['a.c.v','a.a.b'],['a','b'])    
    'a.a.b'
    '''
    factors_=[]
    for i in factors:
        for j in filters:            
            if j==i.split('.')[-1]:
                #print(j,i)
                factors_.append(i)
    return factors_