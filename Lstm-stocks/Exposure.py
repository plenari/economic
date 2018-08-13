# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 12:20:53 2018

@author: omf
获取有暴露因子有关的数据
"""
try:
    import rqdatac 
    from rqdatac import *
    rqdatac.init()
except:
    pass

import pandas as pd
import numpy as np

def get_exposure(symbols,exposure,start_date,end_date):
    '''
    获取暴露因子    
    '''
    exposure=get_factor_exposure(symbols,factors=exposure,start_date=start_date,end_date=end_date)    
    
    exposure=exposure.to_frame().reset_index().rename(columns={'order_book_id':'symbol'})
    
    return exposure

#exposure=get_exposure(symbols,exposure=conf.exposure,start_date=conf.start_date,end_date=conf.end_date)    
def construct_exposure_lstm(data,exposures,time_step=30):
    '''
    data为 包含因子和价格的数据
    exposures为特征列表    
    将以上数据转换成lstm的形式    
    '''   
    result=[]
    for i,df in  enumerate(data.groupby(by='symbol')):
        
        ins,df=df
        df=df.set_index('date').sort_index()
        
        for index in range(df.shape[0]-time_step+1):
            '''
            对每只股票进行变换。
            '''   
            df_=df[index:index+time_step]  
            X,y=df_[exposures],df_['return_c']           
                
            #X=X.apply(lambda x: np.clip(x,x.mean()-3*x.std(),x.mean()+3*x.std() ))
            #X=X.apply(lambda x:preprocessing.scale(x))
            #当前日期
            current_date=X.index.values[-1]
            #当期收益
            y=y[current_date]
            #添加到结果
            result.append([X.values.tolist(),y,ins,current_date])
            
    result=pd.DataFrame(result,columns=['X','y','instrument','date'])   
    result.dropna(inplace=True)
    return result
