#coding=utf-8

import rqdatac 
from rqdatac import *
rqdatac.init()
from rqalpha.api import *

import numpy as np
import pandas as pd
import lightgbm
import talib
from sklearn import metrics

def init(context):
    # 在context中保存全局变量
    context.symbols =list(get_all_ins(context).index.values)
    context.train_days=40 #用45-5日前的数据做训练
    context.test_days=5 #预测五日收益
    scheduler.run_weekly(rebalance,1)
    # 实时打印日志
    logger.info("there are : {}".format(len(context.symbols)))
    


        
def rebalance(context, bar_dict):
    '''    换仓    '''
    #训练预测
    train_x,train_y,test_x=get_data(context)
    
    test_y_pred=fit_transform(context,train_x,train_y,test_x)
    
    stocks=set(test_y_pred.sort_values(ascending=False)[:100].index.values)
    
    
    holdings = set(get_holdings(context))
    
    to_buy = stocks - holdings    
    to_sell = holdings - stocks

    for stock in to_sell:
        if bar_dict[stock].is_trading:
            order_target_percent(stock , 0)

    if len(to_buy) == 0:
        return
    
    to_buy = get_trading_stocks(to_buy, context, bar_dict)
    cash = context.portfolio.cash
    portfolio_value=context.portfolio.portfolio_value
    if len(to_buy) >0:
        average_value = portfolio_value /len(stocks)
        if average_value > portfolio_value/len(to_buy):
            average_value = portfolio_value/len(to_buy)
    
    for stock in to_buy:
        if (bar_dict[stock].is_trading) and (context.portfolio.cash>average_value):
            order_target_value(stock, average_value)    


def get_trading_stocks(to_buy, context, bar_dict):
    '''    还在交易的股票    '''
    trading_stocks=[i for i in to_buy if bar_dict[i].is_trading]
    return trading_stocks

def get_holdings(context):
    '''获取持仓    '''
    holdings=set([i for i,j in context.portfolio.positions.items() if j.quantity>100])
    return holdings  

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    pass


def get_all_ins(context):
    '''
    股票池
    '''
    all_ins=all_instruments(type='CS')#股票
    all_ins=all_ins.query('status=="Active"')#激活
    all_ins=all_ins.query('exchange=="XSHG"')#上证
    all_ins=all_ins[all_ins.symbol.apply(lambda x: not x.startswith('ST'))]#去掉st
    all_ins.set_index('order_book_id',drop=True,inplace=True)
    
    logger.info('all_instruments is done....')

    return all_ins.sort_index()
    

def get_fac(context,date):
    '''
    date,获取那天的数据
    获取当日test_days之前那天的估值因子
    '''    
    growth_ind=query(fundamentals.eod_derivative_indicator.pe_ratio,
          fundamentals.eod_derivative_indicator.pb_ratio,
          fundamentals.eod_derivative_indicator.ps_ratio,
          fundamentals.eod_derivative_indicator.peg_ratio).filter(
              financials.stockcode.in_(context.symbols)
              )
    #获取数据
    growth=get_fundamentals(growth_ind,date,'1d')
    #得到当前日期的数据
    fac=growth.iloc[:,0,:]
    #去掉na
    #fac=fac.dropna(how='all',axis=0).fillna(0.0)
    fac=fac.fillna(method='bfill').fillna(0.0)
    #logger.info('factors is done....')
    
    return fac
def get_history(context):
    ''' 竟然获取的数据不是我想要的长度 '''
    bars_count=context.test_days+context.train_days
    price=pd.DataFrame()
    for i in context.symbols:
        
        bar=history_bars(i,bars_count,'1d','close')
        if len(bar)==bars_count:
            price[i]=bar
        else:
            data=np.zeros((bars_count))
            data[-len(bar):]=bar
            price[i]=data
    return price

def get_pri(context):
    '''
    获取now前test_day和train_day
    与价格有关的数据
    '''
    #获取价格
    price=get_history(context)
    #logger.info('ALL price {}'.format(price.shape))
    #处理数据
    #price.dropna(how='all',axis=1,inplace=True)
    price=price.fillna(method='bfill').fillna(0.0)
    
    #price_train=price.query('index<="{}"'.format(split_date))#当前数据
    #price_test=price.query('index>="{}"'.format(split_date))#未来数据

    #训练用x
    price_train_x=price.iloc[:-context.test_days,:]    
    #logger.info('train price {}'.format(price_train_x.shape))
    #训练用y使用的数据
    price_train_y=price.iloc[-context.test_days:,:]    
    
    #预测用x
    price_test_x=price.iloc[-context.train_days:,:]
    #logger.info('test price {}'.format(price_test_x.shape))
    #训练数据y的涨幅
    price_train_y=price_train_y.apply(lambda x:100*(x.iloc[-1]-x.iloc[0])/x.iloc[0],axis=0)#涨幅
    
    #logger.info('price is done....type is {}'.format(type(price_train_x)))
    #context.trainx=price_train_x
    #context.trainy=price_train_y
    #context.testx=price_test_x
    return price_train_x,price_train_y,price_test_x 
    

def get_sma(price,period):
    '''
    period该周期下最近一天的移动均线
    ** 移动均线不能简单的平均,暂时先这样简单平均
    '''
    df=price.apply(lambda x: talib.SMA(x.values,timeperiod=period)[-1],axis=0)
    df.name='sma-'+str(period)
    logger.info('{} sma is done....'.format(period))
    return df 
    
def concat_fac(context,fac,price):
    '''
    fac：因子
    price:价格
    当前截面之前的价格数据
    '''
    #rsi
    period=14
    rsi=price.apply(lambda x: talib.RSI(x.values,timeperiod=period)[-1],axis=0)
    rsi.name='rsi'

    sma=pd.concat([get_sma(price,5),get_sma(price,21),get_sma(price,30)],axis=1)

    data=pd.concat([fac,sma,rsi],axis=1)
    
    return data    

def get_data(context):
    '''
    获取数据
    '''
    #获取因子数据
    date_test=get_previous_trading_date(context.now,n=context.test_days)
    
    fac_train=get_fac(context,date_test) 
    fac_test=get_fac(context,context.now)     
    logger.info('factors shape:1. {}  2. {} type is {}'.format(fac_train.shape,fac_test.shape,type(fac_train)))
    
    #获取价格数据
    price_train_x,price_train_y,price_test_x=get_pri(context)    
    logger.info('factors shape:{}{}'.format(price_train_x.shape,type(price_train_x)))
    
    train_x=concat_fac(context,fac_train,price_train_x)   
    test_x=concat_fac(context,fac_test,price_test_x)   
    
    train_y=(price_train_y>0.5).apply(int).values

    return train_x,train_y,test_x  
    
  
def fit_transform(context,train_x,train_y,test_x):
    '''
    用来训练的数据
    '''
    logger.info('{}{}{}'.format(train_x.shape,train_y.shape,test_x.shape))
    gbmc=lightgbm.LGBMClassifier(boosting_type='gbdt', num_leaves=11, max_depth=-1, learning_rate=0.3, \
                            n_estimators=500,  subsample_for_bin=1000,  \
                            min_split_gain=1e-4, min_child_weight=0.001,\
                            min_child_samples=5, subsample=0.6, subsample_freq=2,\
                            colsample_bytree=1.0, reg_alpha=0.2, reg_lambda=0.2, n_jobs=-1, silent=-1,)
    
    gbmc.fit(train_x,train_y)
    
    test_y_pred=gbmc.predict(test_x)
    
    #logger.info('train accuract :  ',metrics.accuracy_score(train_y,gbmc.predict(train_x)))
    #logger.info('f1    score    :  ',metrics.f1_score(train_y,gbmc.predict(train_x)))
        
    test_y_pred=gbmc.predict_proba(test_x)[:,0]
    
    test_y_pred=pd.Series(test_y_pred,index=context.symbols)
    return test_y_pred
    
  
    
    