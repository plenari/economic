#coding=utf-8
import datetime
import tushare as ts
import pandas as pd
import numpy as np
'''
每周一计算上周流入，流出情况，如果上周流入，就持有一周，
上周流出不在持有
死于网络不通畅。
'''
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init....")
    context.s1 = "601009.XSHG"
    context.holddays=5
    update_universe(context.s1)
    scheduler.run_weekly(weekly, weekday=1)
    context.buy=0
def get_previous_n_days(now,n):
    for i in range(n):
        now=get_previous_trading_date(now)
    return now

def weekly(context,bar_dict):
    #每周一运行。获取上周的数据。
    sumbuy,sumsell=0,0
    for i in range(5): 
        date=get_previous_trading_date(context.now,i).strftime('%Y-%m-%d')
        sina_tick = ts.get_tick_data('600848', date=date) #大单
        
        
        if sina_tick.volume.size>0 :
            sina_dd=sina_tick[sina_tick.volume>1000]
            print(sina_dd.shape)
            sumbuy+=sina_dd[sina_dd.type=='买盘'].volume.sum()
            sumsell+=sina_dd[sina_dd.type=='卖盘'].volume.sum()
    if sumbuy>sumsell:
        context.buy=1
    if sumbuy<sumsell:
        context.buy=0
    
def balance(context, bar_dict):
    if context.buy==0:
        order_percent(context.s1, 0.9)
    if context.buy==1:
        pass
# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    '''
    如果不该买，就不要买。但是已经有的就不要管了。就要持有五天或者，等macd.
    如果该买就要判断是否需要买。并记录买入时间。
    '''
    if context.now.weekday()==1:
        print(context.now,context.buy)
        balance(context, bar_dict) 