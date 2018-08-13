# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 13:11:07 2018

@author: omf
就是构建lstm的数据结构
"""
import pandas as pd
import numpy as np
from sklearn import preprocessing

def construct_price_lstm(conf,data,Entire=True,shuffle=True):
    '''
    构造数据，用来lstm
    conf:simple class,包含，return_days，features，fields,feature_back_days
    data, pd.DataFrame 包含date,symbol,open,close
    ENtire:除了symbol一起处理
    shuffle:最后打顺序
    >>>
    	                       X                             	y     	instrument    	date
    0	[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1324433432.49,...	-7.047380	600004.XSHG	2016-02-19
    1	[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1324433432.49,...	-13.230802	600004.XSHG	2016-02-22
    
    '''
    conf.input_dim=data.shape[1]-2
    result=[]    
    for i,df in  enumerate(data.groupby(by='symbol')):
        '''
        按照股票分组将数据整理成时间序列
        '''    
        ins,df=df
        df=df.set_index('date')
        #计算收益#三倍标准差
        return_days=10*(df['close'].shift(-conf.return_days) / df['open'].shift(-1)-1)
        r_std,r_mean=return_days.std(),return_days.mean()
        return_days=np.clip(return_days,r_mean-3*r_std,r_mean+3*r_std)
        #
        for index in range(df.shape[0]-conf.feature_back_days+1):
            '''
            对每只股票进行变换。
            
            if this group's std is very small ,i will pass ,continue next one. 
            '''   

            #处理fields,主要是计算相对第一天的涨跌            
            if not Entire:
                #分开处理
                fie_d=df[conf.fields][index:index+conf.feature_back_days]
                fie_d=fie_d.apply(lambda x:x/x[0]-1)
                #处理feature，没有任何处理
                fea_d=df[conf.features][index:index+conf.feature_back_days]    
                fea_d=fea_d.apply(lambda x:x/x[0]-1)
                #将价格和特征合并
                X=pd.concat([fie_d,fea_d],axis=1)
                
            if Entire:
                ''',我发现财务数据缺失较多,so delete fundamentals data'''
                X=df[index:index+conf.feature_back_days]  
                if np.any(X.std()<(0.9*0.1)):
                    continue

                del X['symbol']
                
                X=X.apply(lambda x: np.clip(x,x.mean()-3*x.std(),x.mean()+3*x.std() ))
                X=X.apply(lambda x:preprocessing.scale(x))
            #当前日期
            current_date=X.index.values[-1]
            #当期收益
            y=return_days[current_date]
            #添加到结果
            result.append([X.values.tolist(),y,ins,current_date])
            
    result=pd.DataFrame(result,columns=['X','y','instrument','date'])   
    result.dropna(inplace=True)
    #
    if shuffle:
        result=result.sample(frac=1.0).reset_index(drop=True)
        
    return result
