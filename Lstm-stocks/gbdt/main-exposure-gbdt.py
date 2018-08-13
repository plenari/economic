# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:31:40 2018
@author: omf

price &talib
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
import lightgbm
from sklearn import metrics
#from price import main_price
from sklearn import preprocessing
from exposure import construct_exposure_lstm
#from exposure import get_exposure
#from utils import get_all_instruments

'''

#1. 获取信息
##conf.symbols_df=get_all_instruments(conf)

#股票池

#conf.symbols=index_components('000300.XSHG')[:20]
#conf.symbols=conf.symbols_df.index.values.tolist()
#2.获取数据
#price=main_price(conf)
#保存
#price.to_csv('./data/hs300_main_price.csv')

#读取
price=pd.read_csv('./data/hs300_main_price.csv',index_col=0)
conf.symbols=list(set(price.symbol))


#3. 获取因子
#exposure_data=get_exposure(conf.symbols,conf.exposures,conf.start_date,conf.end_date)
exposure_data=pd.read_csv('./data/hs300_exposure.csv',index_col=0)
#4. 组合数据
print('construct_data_lstm....')
data=pd.merge(price,exposure_data,on=['date','symbol'],how='inner')

#5.分割数据
lstm_train_tal=data.query('date <= "%s"' % conf.split_date)
lstm_test_tal=data.query('date >= "%s"' % conf.split_date)

#6. 构造模型

#train
trainx=np.array(lstm_train_tal[conf.exposures].values.tolist())
trainy=np.array(lstm_train_tal['return_c'].values.tolist())

#test
testx=np.array(lstm_test_tal[conf.exposures].values.tolist())
testy=np.array(lstm_test_tal['return_c'].values.tolist())

print('gbdt_train....')
'''

gbmc=lightgbm.LGBMClassifier(boosting_type='gbdt',Trees='rf', num_leaves=61, max_depth=-1, learning_rate=0.05, \
                            n_estimators=10000,  subsample_for_bin=1000000,  \
                            min_split_gain=1e-4, min_child_weight=0.0001,\
                            min_child_samples=20, subsample=0.6, subsample_freq=2,\
                            colsample_bytree=1.0, reg_alpha=0.01, reg_lambda=0.02, \
                            is_unbalance=True,n_jobs=-1, silent=True,\
                            )
#class_weithg='is_unbalance'
#6. 训练train
def fit_transform(model,trainx,trainy,testx,testy):
    '''
    用来训练的数据
    '''
    
    model.fit(trainx,trainy,eval_set=(testx,testy),feature_name=conf.exposures,
              eval_metric='auc',early_stopping_rounds=1000,verbose=1000)
    '''
    model.fit(trainx,trainy,eval_set=(trainx,trainy),feature_name=conf.exposures,
              eval_metric='f1_score',early_stopping_rounds=500,verbose=500)
    
    '''
    
    test_y=model.predict(testx)  
        
    
    #print('train accuract :  ',metrics.accuracy_score(trainy,gbmc.predict(trainx)))
    #print('train,f1    score    :  ',metrics.f1_score(trainy,gbmc.predict(trainx)))
    
    print('test accuract :  ',metrics.accuracy_score(testy,test_y))
    print('test,f1    score    :  ',metrics.f1_score(testy,test_y))
    
    #test_y_pred=pd.Series(test_y_pred,index=context.symbols)
    return model
gbmc=fit_transform(gbmc,trainx,trainy,testx,testy)
lightgbm.plot_importance(gbmc)
