# coding: utf-8
'''
1. 获取所有股票基本数据，主要是行业分类。
2. 每天获取所有股票的市值，计算行业涨幅，计算排名。
3. 获取所有股票价格，计算计算排名
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
os.chdir(r'F:\app\anaconda\Lib\site-packages\rqalpha\myself\ricequant\industry_lstm')
#ricequant 的函数
def get_trading_dates():
    pass
def get_price():
    pass
def shenwan_industry():
    pass
def get_fundamentals():
    pass
def shenwan_instrument_industry():
    pass
def query():
    pass
def fundamentals():
    pass
def all_instruments():
    pass


def get_factors_fund_step(stocks,factor,end,days):
    '''
    少量的获取factor数据
        stocks ：股票列表
        factor:因子
        end,结束日期，
        days:向前多少天
    return :
        pd.DataFrame
        Index是日期
    '''
    q=query(eval('{}'.format(factor))).filter(
            fundamentals.eod_derivative_indicator.stockcode.in_(stocks)
            )
    facs=get_fundamentals(q,end,'{}d'.format(days))  #get_fundaments,panel
    name_factor=factor.split('.')[-1]
    facs=facs[name_factor]#dataFrame  
    return facs  
        
def get_factors_fund(stocks,factor,end,days):
    '''
    大量的获取factor数据
        stocks ：股票列表
        factor:因子
        end,结束日期，
        days:向前多少天
    return：pd.DataFrame
        index 是股票代码    
    '''
    step=100#
    if len(stocks)<=step:  
        factor_alphalens=get_factors_fund_step(factor,end,len(days))
    if len(stocks)>step:
        index_split=(np.arange(len(stocks)//step)+1)*step#if 232 [100,200]
        index_split=np.hstack([index_split,len(stocks)])#[100,200,232]
        factor_alphalens=get_factors_fund_step(stocks[:step],factor,end,len(days))
        for i in range(len(index_split)-1):
            factor_alphalensi=get_factors_fund_step(stocks[index_split[i]:index_split[i+1]],factor.end,len(days))
            factor_alphalens=pd.concat([factor_alphalens,factor_alphalensi],axis=1)
    return factor_alphalens.T



def get_all_instruments():
    '''
    1.获得激活股票列表
    return pd.DataFrame
        index 是股票代码
    '''
    all_ins=all_instruments(type='CS')
    all_ins=all_ins.query('status=="Active"')
    all_ins.set_index('order_book_id',drop=True,inplace=True)
    return all_ins.sort_index()


def get_market_cap(sid,start,end):
    '''
    返回sid的股票市值. 
    return pd.DataFrame
        Index是股票代码,Columns是日期
    '''
    days=len(get_trading_dates(start,end))
    q=query(fundamentals.eod_derivative_indicator.market_cap).filter(fundamentals.income_statement.stockcode.in_(sid))
    market_cap=get_fundamentals(q,end,'{}d'.format(days))
    return market_cap['market_cap'].T

start='2017-01-01'
end='2018-04-12'
#all_ins=get_all_instruments()
#all_cap=get_market_cap(all_ins.index.values,start,end)
#all_cap.to_csv('s{}-e{}-market_cap.csv'.format(start,end))
#all_cap=pd.read_csv('s{}-e{}-market_cap.csv'.format(start,end))


# 3. 计算所有板块
def cal_industry_increase_day(all_cap,n=1):
    '''
    计算每日相对于前n天涨跌幅。
        all_cap的index为股票，columns 为日期，
    return ，比输入少一天
        pd.DataFrame
        相对前一天的涨幅
    '''
    all_cap=all_cap.T.sort_index().T
    cap=all_cap.sum()
    cap=cap.diff(n)/cap.shift(n)
    return cap.dropna()

def cal_industry_increase_hisory(all_cap,day='2018-03-14'):
    '''
    计算与某天相比的涨幅。
        计算index为股票，columns 为日期，
        日期升序排列。   get_market_cap 的返回值
        day 为作为基准的日期
    return pd.DataFrame
    '''
    all_cap=all_cap.T.sort_index().T
    cap=all_cap.sum()
    cap=cap/cap[day]
    return cap
#4.计算所有版块的日涨幅
industry_day_increase=all_cap.groupby(all_ins.industry_code).apply(cal_industry_increase_day)

#5.行业涨幅都已经获得，就需要排名
rank=industry_day_increase.apply(np.argsort,axis=0)+1


rank_first=rank.apply(np.argmin,axis=0)
rank_first

rank_last=rank.apply(np.argmax,axis=0)
rank_last
#所以可以看出来，排名靠前的基本上在10-20，70-80之间，0-70之间的都是排名倒数的
def plot_industry(inds):
    for i in inds:
      plt.plot(industry_day_increase.loc[i],'-*',label=i)
    plt.xticks(industry_day_increase.loc[i].index,industry_day_increase.loc[i].index , rotation='vertical')
    plt.legend()
    plt.show()
plot_industry(['J66','C34'])


#6.获取涨幅最好和最差板块的股票涨幅数据

C34=all_ins.query("industry_code=='C34'").index.values
J66=all_ins.query("industry_code=='J66'").index.values

P34=get_price_change_rate(list(C34),start,end).T
P66=get_price_change_rate(list(J66),start,end).T

#按照涨幅排名
P34_rank=P34.apply(np.argsort,axis=0)+1

P34_rank.mean(axis=1).sort_values()
#按照涨幅排名
P66_rank=P66.apply(np.argsort,axis=0)+1

P66_rank.mean(axis=1).sort_values()
# ## 获取股票价格
pr34=get_price(list(C34),start,end,fields='close').T
pr66=get_price(list(J66),start,end,fields='close').T
#换成涨幅

pr34_in=pr34.apply(lambda X:X/X[0],axis=1)
pr66_in=pr66.apply(lambda X:X/X[0],axis=1)


ind=industry_day_increase.iloc[:,8:]+1

ind.cumprod(axis=1).iloc[:,-1].sort_values(ascending=False).head(4)

ind.cumprod(axis=1).iloc[:,-1].sort_values(ascending=False).tail(4)

ind_index=ind.cumprod(axis=1).iloc[:,-1].sort_values(ascending=False).index
plt.plot([int(str(i)[1:]) for i in ind_index.values],'*')
# ### 个股与板块涨幅的相关性
y=industry_day_increase.loc['J66'].values.reshape(1,-1)

P66=P66.iloc[:,1:]
corr_with_ind=P66.apply(lambda x:np.corrcoef(x.values.reshape(1,-1),y)[0][1],axis=1).dropna()
# 与C34板块相关性高的地
corr_with_ind.sort_values(ascending=False)
#  我感觉应该尽可能买这种与板块走势相关性大的股票，但是却选那些经常大涨的板块却在下跌中的板块
