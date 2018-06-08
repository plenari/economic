#coding=utf-8
# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import pandas as pd
import numpy as np
import datetime
import math
'''
这个里的和程序里的设置不一样。
格雷厄姆企业主投资法的最初版本从财务状况、盈利稳定、股息记录、利润增长、股价高低五个方面加以考虑。
后世将五条标准归纳为更具普适性的七条准则。这七条准则要求股票具备合理估值、稳定的盈利历史记录,并通过财务结构强调资产具备可实现价值。
格雷 厄姆企业主投资法的“七条准则”,明确清晰,各项标准基本均可量化。
严格按照原始的“七条准则”测试后发现大多数在A股选不出足够股票数量。
因此, 我们结合中国市场和经验,在遵循企业主投资法的原则基础上,对相应准则进行适当的放 宽额调整
在格雷厄姆原书五条标准基础之上,后世剔除了一些例如 1996 盈利基准等一些 细节要求,
从而形成了如下 7 条更具操作性和普适性的调准,我们称之为格雷厄 姆企业主投资策略的通用版本:
A.股票的市盈率低于市场平均水平 pe
B.股票的市净率小于 1.2 
C.企业的流动资产至少是流动负债的 1.5 倍 
D.企业的总借款不超过净流动资产的 1.1 倍 
E.最近五年净利润大于 0 
F.最近一期现金股利大于 0 
G.盈利(TTM)大于三年前的盈利

结合中国投资市场的实际情况之后,在研究和回测中对部分原始标准进行调整: 
B 改为:股票的市净率小于 2.5
C 改为:企业的流动资产至少是流动负债的 1.2 倍
D 改为:企业的总借款不超过净流动资产的 1.5 倍
E 改为:最近五年至少四年净利润大于 0
G 改为:盈利(TTM)至少为三年前的盈利的 80%
'''
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):#这里用g，和用context一样吗？
    #g也是简单对象？
    context.index2 = 'SSE50.INDX'#'000001.XSHG' # 上证50指数
    #g.index8 = '399333.XSHE'  # 中小板R指数
    context.index_growth_rate_20=-0.01#指数增长率
    context.num_stocks=5#股票数目
    
# 获取前n个单位时间当时的收盘价
def get_close_price(security, n, unit='1d'):#更加费劲
    '''
    n天前收盘数据
    '''
    return history_bars(security,n, unit, 'close')[0]
    
# 获取股票n日以来涨幅，根据当前价计算
def get_growth_rate(security, n=31):
    '''
    获取31天交易日的增长率
    '''
    lc = get_close_price(security, n)
    #可以在日盘里获取分钟线吗?
    c = get_close_price(security, 1, '1m')#current 当前的收盘价，
    if not np.isnan(lc) and not np.isnan(c) and lc != 0:
        return (c - lc) / lc
    else:
        #log.error("数据非法, security: %s, %d日收盘价: %f, 当前价: %f" %(security, n, lc, c))
        return 0

def clear_position(context,bar_dict):# 清空卖出所有持仓
    '''
    if we have stock sell all stock.
    '''
    for stock in get_holding(context):#.keys():可以有，也可以没有。
        order_target_percent(stock, 0)
        
# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    '''
    per day 
    '''
    if context.now.hour == 14 and context.now.minute == 50:
        if get_growth_rate(context.index2,31) <= context.index_growth_rate_20:#涨幅小于某个值
            rebalance(context, bar_dict)#调仓，
            
def before_trading(context):
    '''
    '''
    fundamental_df = get_fundamentals(
        query(
            fundamentals.eod_derivative_indicator.pb_ratio,#B市净率
            fundamentals.eod_derivative_indicator.pe_ratio,#A市盈率
            fundamentals.financial_indicator.inc_earnings_per_share,#基本每股收益(同比增长率)
            fundamentals.financial_indicator.inc_profit_before_tax,#利润总额(同比增长率
            fundamentals.financial_indicator.quick_ratio,#速动比率
            #速动比率是指速动资产对流动负债的比率。它是衡量企业流动资产中可以立即变现用于偿还流动负债的能力。
            fundamentals.financial_indicator.earnings_per_share,#每股收益EPS - 基本
            fundamentals.financial_indicator.book_value_per_share,#每股净资产BPS
        )
        .filter(
            fundamentals.eod_derivative_indicator.pe_ratio<15
        )
        .filter(
            fundamentals.eod_derivative_indicator.pb_ratio<1.5
        )
        .filter(
            fundamentals.financial_indicator.inc_earnings_per_share>0
        )
        .filter(
            fundamentals.financial_indicator.inc_profit_before_tax>0
        )
        .filter(
            fundamentals.financial_indicator.current_ratio>2#C流动比率
        )
        .filter(
            fundamentals.financial_indicator.quick_ratio>1#速冻比例，
        )
        .order_by(
            fundamentals.eod_derivative_indicator.market_cap.asc()#市值升序，也就是小市值。
        ).limit(
            context.num_stocks
        )
    )
    context.fundamental_df = fundamental_df
    context.stocks = context.fundamental_df.columns.values
    logger.info(context.stocks)

def get_holding(context):
    return [ i for i,j in context.portfolio.positions.items() if j.quantity>0]
    
def rebalance(context,bar_dict):
    '''
    
    '''
    for stock in get_holding(context):
        if stock not in context.stocks:
            order_target_percent(stock, 0)
    weight = update_weights(context, context.stocks)
    for stock in context.stocks:
        if weight != 0 and stock in context.stocks:
            order_target_percent(stock,weight)
            logger.info('buy {}'.format(stock))
    
def update_weights(context,stocks):
    if len(stocks) == 0:
        return 0 
    else:
        weight = .95/len(stocks)
        return weight