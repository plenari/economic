# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 14:02:14 2018
@author: omf
----------------
获得与价格有关的数据
"""
try:
    import rqdatac 
    from rqdatac import *
    rqdatac.init()
except:
    pass

import pandas as pd
import numpy as np

def pull_price(symbols,**args):
    '''
    获取数据，并整理成需要的形状。
    与get_price参数一样
    股票列表，起止日期，参数，复权模式。
    '''
    symbols=list(symbols)  #  
    price=get_price(symbols,**args)
    price=price.to_frame().reset_index()    
    price=price.rename(columns={'major':'date','minor':'symbol'},copy=False)    
    
    if 'total_turnover' in price.columns.values:
        price.total_turnover=price.total_turnover/1e9
    
    if 'volume' in price.columns.values:
        price.volume=price.volume/1e9
    
    price=price.dropna(axis=1,how='all')
    
    return price

def main_price(conf):
    '''
    获取价格和n日收益，以及类别收益。
    收益为return，收益类别为return_c
    '''
    price=pull_price(list(conf.symbols),start_date=conf.start_date,\
                     end_date=conf.end_date,fields=conf.fields)
    price=get_returns(price,conf.return_days)
    
    return price

def get_returns(price,return_days):
    '''
    计算多只股票的收益
        price，date，symbol,close,open,
        return_days n日收益
    '''
    price=price.groupby('symbol').apply(lambda x:get_return_r(x,return_days))
    price.index=price.index.droplevel() 
    price=price.groupby('date').apply(lambda x:get_return_c(x))
    #去掉nan
    price=price.dropna(axis=0,how='any')
    
    return price

def get_return_c(df,industry=False):  
    '''
    把收益分类,0,1,2,对应百分比30,40,30
    是否按照行业,还不会写
    '''
    returns=df['return']
    '''按照当日截面的百分比,市场股票很多，只要前30%'''
    limit=returns.quantile(0.7)
    df['return_c']=[1 if i>limit else 0 for i in returns]
    #df['return_c']=np.searchsorted([0.0,1],returns)    
    return df

def get_return_r(df,return_days):  
    '''
    计算收益，用于回归
        计算五日后收盘价，比明日开盘价的收益多少个百分点
    '''
    df=df.sort_values('date')
    df['return']=100*(df['close'].shift(-return_days) / df['open'].shift(-1)-1)        
    
    return df

