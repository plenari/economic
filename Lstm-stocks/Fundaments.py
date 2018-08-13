# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 14:04:17 2018
@author: omf
-------------------
财务数据特征，为什么全是0

"""
try:
    import rqdatac 
    from rqdatac import *
    rqdatac.init()
except:
    pass
from conf import conf
import pandas as pd
import numpy as np
import os


def str_join(strs_list):
    '''
    strs_list:list  strs:
    
    >>> str_join(['a','b','c'])
    'a,b,c'
    '''
    stri=''
    for i in strs_list:
        stri+=i+','
    return stri

def chunck_list(array,nums):
    '''
    array:1Dlist 
    nums:every chunck has nums element except last one
    除了最后一个列表，都有相同的元素
    >>>chunck_list([1,2,3,4],3)    
    [[1,2,3],[4]]    
    '''    
    return [array[i:i+nums] for i in range(0,len(array),nums)]


def get_factors_fundament(symbols,factors,start_date,end_date):
    '''
    获取股票内的因子数据,针对少量的,可直接获取。
    返回major是date，minor是symbols
    '''
    trading_days=len(get_trading_dates(start_date,end_date))   
    
    QUERY=query(
         *eval('{}'.format(factors))
        ).filter(
            fundamentals.eod_derivative_indicator.stockcode.in_(symbols)
        )
    facs=get_fundamentals(QUERY,end_date,'{}d'.format(trading_days))
    try:
        facs=facs.to_frame().reset_index()  
    except Exception as e:
        return None
    return facs

def get_factors_fundaments(symbols,factors,start_date,end_date,per_sym=50,per_factor=5):
    '''
    获取股票和财务因子,大批量,get_factors_fundament    
    factors:list,如下：
        ['fundamentals.income_statement_TTM.financial_expenseTTM',
         'fundamentals.income_statement_TTM.administration_expenseTTM',
         'fundamentals.income_statement_TTM.np_parent_company_ownersTTM',
         'fundamentals.income_statement_TTM.ni_from_value_changeTTM',]
        
    per_sym :每次获取多少只股票
    per_factor:每次获取多少个因子
    
    '''   
    symbols=chunck_list(symbols,per_sym)#分组
    factors=chunck_list(factors,per_factor)#分组
    
    for i,symbol in enumerate(symbols):   
        for j,factor in enumerate(factors):
            factor=str_join(factor)
            if j ==0:
                '''第一次直接获取'''
                df=get_factors_fundament(symbol,factor,start_date,end_date)                
            else:
                df_=get_factors_fundament(symbol,factor,start_date,end_date)
                if isinstance(df,pd.DataFrame):
                    '''
                    之后每次获取都要组合, 将每次获得的数据都merge
                    '''
                    df=pd.merge(df,df_,on=['major','minor'],how='outer')                
    
    df=df.rename(columns={'major':'date','minor':'symbol'},copy=False)     
    df=df.dropna(axis=1,how='all')#若整列都是nan,删除
    
    return df 

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

def main_feature(conf):
    '''
    一步调用    
    '''
    facs=get_factors_fundaments(conf.symbols,conf.feature,conf.start_date,conf.end_date) 
    return facs

def merge_price_factor(price,factor):
    '''
    price:pd.DataFrame
    factor:pd.DataFrame
    
    '''
    #合并价格和因子数据
    data=pd.merge(price,factor,on=['date','symbol'],how='inner')   
    #删除列方向nan大于30%列
    data=data.dropna(axis=1,thresh=int(0.7*data.shape[0]))
    #删除行方向nan大于20%行
    data=data.dropna(axis=0,thresh=int(0.8*data.shape[1]))
    #还有nan却没被删除的，对该股票时间排序，然后用前一天补全，其余填充0
    data=data.groupby('symbol').apply(lambda x:x.sort_values('date').fillna(method='ffill')).fillna(0.0)
    #重置索引
    data.index=data.index.droplevel()
    
    return data