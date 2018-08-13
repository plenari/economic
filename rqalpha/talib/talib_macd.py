#coding=utf-8
import talib
import numpy 
import pandas as pd
'''
macd 回测效果还可以基本跑赢大盘。
加上止损试一下。
加上均线也不行。
'''
def init(context):  
    context.s1 = "000001.XSHE"
    context.fast,context.slower,context.signal=12,26,9
    context.maxvalue=pd.DataFrame()
    #stop loss
    scheduler.run_daily(profit_stop_loss_profit, time_rule=market_open(minute=1))
    scheduler.run_daily(stoploss, time_rule=market_open(minute=2))
    context.increase=pd.DataFrame()
    # 实时打印日志
    context.flag=0
    
def handle_bar(context, bar_dict):

    close = history_bars(context.s1,85,'1d','close')
    ma61=talib.EMA(close,80)
    macd,macdsignal,macdhist = talib.MACD(close,context.fast,context.slower,context.signal)
    curPosition = context.portfolio.positions[context.s1].quantity
    if ma61[-1]>ma61[-5] and macd[-1]>0 and curPosition <100:
        order_target_percent(context.s1,1)
    if macd[-1]<0 or ma61[-1]<ma61[-5] and curPosition>100:
        order_target_percent(context.s1,0)
        
        
def profit_stop_loss_profit(context, bar_dict):
    """止盈止损"""
    threshold_profit_taken = 0.2
    threshold_stop_loss = -0.1
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
        if current<highest*0.95:#这个比例也可以是变化的。
            order_target_percent(stock,0)
            if stock in context.maxvalue.columns:#持仓股票已经记录了
                del context.maxvalue[stock]