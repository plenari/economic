# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 14:06:08 2018

@author: omf
"""
# 0. 基础参数配置
class conf:
    # 设置用于训练和回测的开始/结束日期
    start_date = '2012-01-01'
    split_date = '2018-01-01'
    end_date = '2018-07-25'
    
    #特征
    symbols=[]#股票池
    fields=['open', 'close', 'high', 'low', 'total_turnover']
    features_=None#财务特征最后一个名字
    features=None#财务特征完整名字
    tailbs=[]#talib特征
    
    #因子载荷
    exposures=['volatility','beta','momentum','size','yield','growth','value','leverage','liquidity']
    
    #数据处理 相关
    feature_back_days = 30    # 每个input的长度，使用过去30天的数据
    time_step = 30    # 每个input的长度，使用过去30天的数据
    return_days=5##预期五日收益
    
    #lstm
    batch_size = 100
    epoch=30
    
    
    