import concurrent.futures
import multiprocessing
from rqalpha_plus import run_func
from rqalpha_plus.api import *
import numpy as np
import talib
max_workers = 4

#create para
def hx(a,b):
    #混淆两个列表。
    re=[]
    for i in a:
        for j in b:
            assert type(j)!=list
            if type(i)==list:
                ii=i.copy()
                ii.extend([j])
                re.append(ii)
                del ii
            else:
                re.append([i,j])
    return re

def get_para(plist):
    #是包含许多单层列表的列表。
    for i in map(type,plist):
        if i!=list:
            assert 1==0,'invalid argument'
    re=hx(plist[0],plist[1])        
    for i in range(2,len(plist)):            
        re=hx(re,plist[i])
    return re

#config
def config(start_date):
    '''start_date
    '''
    configi = {
      "base": {
        "matching_type": "current_bar",
        "start_date": start_date, # 回测开始日期
        "end_date": "2018-02-12", # 回测结束日期
        "benchmark": "000001.XSHG", # 基准合约
        "frequency": '1d', # 回测频率, 分钟: '1m'
        "accounts": {
                    "stock": 100000# 股票初始资金  期货："future":100000
                 }
      },
      "extra": {
        "log_level": "error",
      },
      "mod": {
        "sys_progress": {
            "enabled": False,
            "show": False,
        },
        "sys_analyser": {
            "enabled": True,
            "plot":False,
        },
        "sys_simulation": {
        "matching_type": "next_bar",
        }
      }
    }
    return configi

#run_bt
def run_bt(para):
    #type(para)==list
    fast,slow,signal,start_date=para
    def init(context):  
        context.s1 = "000001.XSHE"    
        
    def handle_bar(context, bar_dict):
        close = history_bars(context.s1,50,'1d','close')
        #dif,dea,bar
        dif,dea,bar = talib.MACD(close, fastperiod=fast, slowperiod=slow, signalperiod=signal)
        curPosition = context.portfolio.positions[context.s1].quantity
        if bar[-1]>0 and curPosition <100:  
            order_target_percent(context.s1,1) 
        if bar[-1]<0 and curPosition > 0:
            order_target_percent(context.s1,0)

    try:
        result = run_func(config=config(start_date), init=init, handle_bar=handle_bar)
    except Exception as e:
        #print(e)
        return
    return result, para
    
def main():

    fastperiod=np.arange(10,13,2)
    slowperiod=np.arange(20,24,2)
    signalperiod=np.arange(7,9,1)
    para_list=[list(fastperiod),list(slowperiod),list(signalperiod),['2017-12-12']]
    tasks=get_para(para_list)
    # 并发运行回测,先站存到list
    futures = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for task in tasks:
            future = executor.submit(run_bt, task)
            futures.append(future)
            
    #获取最后的结果
    annualized_returns = []
    for future in futures:      
        returns, paras = future.result()
        result=[returns['sys_analyser']['summary']['annualized_returns'], *paras]#
        annualized_returns.append(result)
    return annualized_returns
  
re=main()
