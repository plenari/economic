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
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
import numpy as  np

from sklearn import preprocessing
from Exposure import construct_exposure_lstm

#from price import main_price
#from exposure import get_exposure
#from utils import get_all_instruments

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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
#构造数据
lstm_data=construct_exposure_lstm(data,conf.exposures,time_step=conf.time_step)

#5.分割数据
lstm_train_tal=lstm_data.query('date <= "%s"' % conf.split_date)
lstm_test_tal=lstm_data.query('date >= "%s"' % conf.split_date)

#6. 构造模型
#train
trainx=np.array(lstm_train_tal['X'].values.tolist())
trainy=np.array(lstm_train_tal['y'].values.tolist())
#test
testx=np.array(lstm_test_tal['X'].values.tolist())
testy=np.array(lstm_test_tal['y'].values.tolist())


#6. 训练train
device=0
input_dim=9
hidden_dim=64
num_layers=2
num_classes=2
batch_size=300
cuda=0
seq_len=30
epochs=15
from LSTM_torch import LSTM,train_epoch
print('lstm_train....')


model=LSTM(input_dim, hidden_dim, num_layers, num_classes,batch_size,seq_len)
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.05)

model=train_epoch(model,loss_function,optimizer,trainx,trainy,testx,testy,batch_size,seq_len,input_dim,num_layers,epochs=epochs)

torch.save(model.state_dict(), 'lstm_epoch{}.pkl'.format(epochs))
#model_object.load_state_dict(torch.load('params.pkl'))

