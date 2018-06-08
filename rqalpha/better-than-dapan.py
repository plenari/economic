# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
'''
涨没有别快，跌的还快
'''
import time
import datetime
import pandas as pd
import numpy as np
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 在context中保存全局变量
    #universe = ['000300.XSHG', '000016.XSHG']
    #获取成分股，sum([['300'],['600']],[])可以得到['300','600']
    #context.stocks = set(sum([index_components(index, date=context.now.date()) for index in universe], []))
    all_stock=all_instruments(type='CS')
    all_stock=all_stock[all_stock.de_listed_date=='0000-00-00']
    context.stocks=all_stock.order_book_id.values
    
    context.maxvalue=pd.DataFrame()
    context.n=11
    context.num=20
    #stop loss
    scheduler.run_daily(profit_stop_loss_profit, time_rule=market_open(minute=1))
    scheduler.run_daily(stoploss, time_rule=market_open(minute=2))
    context.increase=pd.DataFrame()
    # 实时打印日志
    context.flag=0
    logger.info("RunInfo: {}".format(context.run_info))


# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    hs300_price=history_bars('000001.XSHE',context.n,'1d','close',False)
    get_better_than_hs300(context,get_increase(hs300_price),n=3)

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    balance(context, bar_dict)
    context.flag=1
    
# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    pass


def get_increase(p):
    '''得到序列p后一天的增幅'''
    return p[1:]/p[:-1]-1

def get_better_than_hs300(context,hs300_i,n=3):
    '''
    获得序列，并得到比大盘大的天数，然后去最大的20个平均买入股票。
    '''
    for stocki in context.stocks:
        if np.any(is_suspended(stocki,context.n)):#只要有一天停牌
            return
        
        stock_price=history_bars(stocki,context.n,'1d','close')  
        stock_i=get_increase(stock_price)
        context.increase.loc[stocki,'increase']=np.mean(stock_i>hs300_i*n)


def balance(context,bar_dict):
    '''
    写的非常乱
    '''

    tobuy=context.increase.sort_values(by='increase').index[-context.num:].values
    hold=set([i for i,j in context.portfolio.positions.items() if j.quantity>100])
    tosell=hold-set(tobuy)
    tobuy=set(tobuy)-hold
    clear_stock(context,tosell)
    cash=context.portfolio.cash
    per=cash/len(tobuy)
    for stock in tobuy:
        order_value(stock,per)
    
    
def clear_stock(context,tosell):
    for stock in tosell:
        order_target_value(stock,0)

def profit_stop_loss_profit(context, bar_dict):
    """止盈止损"""
    threshold_profit_taken = 0.2
    threshold_stop_loss = -0.05
    '''这个地方可以用dict.items()吧?'''
    for s, position in context.portfolio.positions.items():
        '''stock position,平均持仓成本'''
        avg_cost = position.avg_price
        profit_percent = (bar_dict[s].last - avg_cost) / avg_cost
        if profit_percent > threshold_profit_taken:
            order_target_percent(s, 0.0, MarketOrder())
        elif profit_percent < threshold_stop_loss:
            order_target_percent(s, 0.0, MarketOrder())
            
            
def stoploss(context,bar_dict):
    '''吊顶止损，需要每天运行。保存并更新最大值。
    如果当前值比最大值下跌9%则情况改股票。'''
    for stock in [i for i,j in context.portfolio.positions.items() if j.quantity>100]:#持仓股票
        high=bar_dict[stock].high
        current=bar_dict[stock].last#new values
        if stock in context.maxvalue.columns:#持仓股票已经记录了
            highest=context.maxvalue.stock[0]#之前最大值
            context.maxvalue.stock=[max(high,highest)]#更新最大值
        else:
            context.maxvalue.stock=[bar_dict[stock].high]
            highest=high
        #从最大值处跌去10%止损。
        if current<highest*0.9:#这个比例也可以是变化的。
            order_target_percent(stock,0)
            if stock in context.maxvalue.columns:#持仓股票已经记录了
                del context.maxvalue[stock]
            