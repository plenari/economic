# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:31:40 2018
@author: omf

单独训练price
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
#from price import pull_price
#from utils import get_all_instruments
from data import construct_data_lstm
from model import lstm_train,lstm_predict
#1. 获取信息
#conf.symbols_df=index_components('000300.XSHG')
#股票池沪深300成分股
#conf.symbols=index_components('000300.XSHG')
#2.获取数据
#price=pull_price(conf.symbols,start_date=conf.start_date,end_date=conf.end_date,fields=conf.fields)
#price.to_csv('price.csv')
price=pd.read_csv('price.csv',index_col=0)

del price['total_turnover']
del price['volume']

conf.symbols=list(set(price.symbol))

#3. 转换数据
print('construct_data_lstm....')
lstm_price=construct_data_lstm(conf,price)
#4.分割数据
lstm_train_tal=lstm_price.query('date <= "%s"' % conf.split_date)
lstm_test_tal=lstm_price.query('date >= "%s"' % conf.split_date)
#5. 训练模型
print('lstm_train....')
lstm_model=lstm_train(lstm_train_tal,conf)

#6. 验证集
lstm_predict(lstm_model,lstm_train_tal,'train')
lstm_predict(lstm_model,lstm_test_tal,'test')


#factor_name_need=change_factor_names(factor_name_need,data.columns.values)
#随时更新特征内容
#conf.features_=factor_name_need
#conf.features=[i.split('.')[-1] for i in factor_name_need]
