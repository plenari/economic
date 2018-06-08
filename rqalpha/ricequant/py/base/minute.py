#coding=utf-8
import six
from talib.abstract import *
import numpy as np
import pandas as pd

def init(context):
    # 设置当前计数器为0，用于计算是否到达调仓时间。
    context.count = 0
    #设置成开盘后一两分钟执行。
    scheduler.run_daily(daily_routine_first, time_rule=market_open(minute=1))
    scheduler.run_daily(daily_routine_second, time_rule=market_open(minute=2))

def get_stock_pool(context, bar_dict):
    """
    获取当日经过筛选的股票池
    """
    universe = ['000300.XSHG', '000016.XSHG']
    #获取成分股，sum([['300'],['600']],[])可以得到['300','600']
    stocks = set(sum([index_components(index, date=context.now.date()) for index in universe], []))                      
    # 保存最初选入的股票池，用于计算比例相关筛选条件
    context.stock_pool_initial = stocks
    # 筛选财务指标
    stocks = filter_financial_indicators(context, stocks)
    # 筛选行情指标   #
    stocks = filter_market_indicator(context, stocks)
    # 筛选技术指标 #
    stocks = filter_technical_indicator(context, stocks)
    return stocks

def is_within_limit_up(bar_dict, s):#涨停不能买，
    return bar_dict[s].last < bar_dict[s].limit_up

def is_within_limit_down(bar_dict, s):#跌停不能卖
    return bar_dict[s].limit_down < bar_dict[s].last


def filter_financial_indicators(context, stocklist):
    """    筛选财务指标    """
    # 若传入的股票池为空则直接返回空股票池
    if stocklist is None or len(stocklist) == 0:
        return set()
    # 从数据库中找出符合数值硬性条件的指标，例如大于小于和区间
    #stockcode 获取股票代码
    indicator_query = query(fundamentals.stockcode)\
        .filter(fundamentals.stockcode.in_(stocklist))

    indicator_query = indicator_query.filter(
        fundamentals.financial_indicator.earnings_per_share > 5.0)
    stocklist = get_fundamentals(indicator_query).columns.tolist()#只要股票名字

    if stocklist is not None:
        stocklist = set(stocklist)
    else:#是否应该break
        stocklist = set()
    return stocklist

def get_IPO_trading_days(context, stocklist):
    """
    获得股票上市交易天数
    返回对应股票的上市天数
    """
    last_trading_day = np.array(get_previous_trading_date(context.now.date())).astype('datetime64[D]')
    #每一个index对应的值都是last_trading_day
    IPO_dates =np.array([instruments(x).listed_date for x in stocklist]).astype('datetime64[D]')
    return pd.Series((last_trading_day-IPO_dates),index=stocklist)

def filter_market_indicator(context, stocklist):
    """
    筛选行情指标
    返回筛选后的股票池
    """
    def cal_avg_value(stocklist, factor, n, fields=None):
        """
        计算某个指标n日平均值
        factor:计算的指标
        n:天数
        fields:对于换手率，需要额外指定是什么时间段的换手率（当日，5日，10日等）
        返回计算好的指标值
        """
        if factor == 'turn_over_rate':#换手率
            factor = get_turnover_rate(list(stocklist), fields=fields, count=n)
            factor = factor.mean(axis=0).sort_index()
            factor.name = 'turn_over_rate'
            return factor
        else:
            dictionary = {s: history_bars(s,bar_count=n,fields=factor,frequency="1d").mean()\
                          for s in stocklist}
            return pd.Series(dictionary).sort_index()

    stocklist = set(stocklist) if stocklist is not None else set()
    factor = get_IPO_trading_days(context, stocklist)
    factor.sort_index(inplace=True)
    factor = factor[factor > 100.0]
    stocklist.intersection_update(set(factor.index.tolist()))#求交集
    return stocklist

def determine_filter_technical_indicator_for_one_stock(context, stk, bar_count):
    """
    检查指定股票是否通过筛选。
    """
    inputs = pd.DataFrame(history_bars(stk, bar_count, '1d'))
    # 剔除可获得数据很少的股票（例如刚上市)
    if len(inputs.index) < 60:
        return False
    # 预先准备好行情数据
    inputs.set_index('datetime')
    inputs = inputs.to_dict(orient='list')

    inputs = dict([(key, np.asarray(x)) for key, x in inputs.items()])
    EMA.input_arrays = inputs    
    EMA__timeperiod_10_ = pd.DataFrame(np.asarray(EMA(**({'timeperiod': 10}))).T, \
                                       columns=EMA.info['output_names'])

    EMA.input_arrays = inputs
    EMA__timeperiod_24_ = pd.DataFrame(np.asarray(EMA(**({'timeperiod': 24}))).T, \
                                       columns=EMA.info['output_names'])

    #通过筛选规则判断股票是否通过筛
    test = EMA__timeperiod_10_['real'] - EMA__timeperiod_24_['real']
    if not ((test.iloc[-2] < 0) and (test.iloc[-1] > 0)):
        return False
    return True

def filter_technical_indicator(context, stocklist):
    """
    根据技术指标规则对股票池进行筛选
    返回经过筛选的股票池
    """
    #默认获得最近100个交易日行情数据
    bar_count = 100
    stocks_filtered = []
    #剔除上市天数过少的股票
    trading_days = get_IPO_trading_days(context, stocklist)
    stocklist = trading_days[trading_days > 30].index
    if stocklist is None or len(stocklist) == 0:
        return []

    #依次检查每一只股票是否满足筛选条件
    for stk in stocklist:
        if determine_filter_technical_indicator_for_one_stock(
                context, stk, bar_count=bar_count):
            stocks_filtered.append(stk)
    return stocks_filtered

def sort_indicators(stocklist, context, bar_count=100):
    """对股票池股票进行排序"""
    if stocklist is None or len(stocklist) == 0:
        return []
    def get_scores(series, ascending):
        """
        获取一组因子的排名分数
        series: 股票代码-因子值序列
        ascending: 是否值越大，分数越高
        返回计算好的股票代码-分数序列
        """
        series = series.astype(float)
        nans = series.apply(np.isnan)
        #这句话是什么意思？
        non_nan_series = series[~nans]
        nan_exist = nans.any()
        unique_values = np.unique(non_nan_series.values)
        if nan_exist:
            unique_score_list = pd.Series(
                np.linspace(100.0,0.0,len(unique_values) +int(nan_exist))[:-1],index=unique_values)
        else:
            unique_score_list = pd.Series(
                np.linspace(100.0, 0.0, len(unique_values)),
                index=unique_values)
        if len(unique_values) == len(series):
            scores = pd.Series(unique_score_list.values, index=series.index)
        else:
            scores = pd.Series(index=series.index)
            for value in unique_score_list.index:
                scores[series == value] = unique_score_list[value]
            scores.fillna(0, inplace=True)
        return scores
    indicator_score_dataframe = pd.DataFrame(index=stocklist)
    weights = []
    #对财务相关指标，从数据库中获得数据，直接计算出分数
    indicator_query = query().filter(fundamentals.stockcode.in_(stocklist))
    indicator_dataframe = get_fundamentals(indicator_query).T
    weights += []
    weights = np.asarray(weights, dtype='float')
    final_scores = pd.Series(np.asarray(np.matmul(indicator_score_dataframe.values,weights)),\
                             index=stocklist)
    return final_scores.sort_values(ascending=False).index.tolist()

def profit_taken_stop_loss(context, bar_dict):
    """止盈止损"""
    threshold_profit_taken = 0.2
    threshold_stop_loss = -0.05
    '''这个地方可以用dict.items()吧?'''
    for s, position in six.iteritems(context.portfolio.positions):
        '''stock position,平均持仓成本'''
        avg_cost = position.avg_price
        profit_percent = (bar_dict[s].last - avg_cost) / avg_cost
        if profit_percent > threshold_profit_taken:
            order_target_percent(s, 0.0, MarketOrder())
        elif profit_percent < threshold_stop_loss:
            order_target_percent(s, 0.0, MarketOrder())

def daily_routine_first(context, bar_dict):
    """按实际换仓"""
    # 使用计数器检查是否到达调仓时间
    if context.count % 5 == 0:
        rebalance_plan_sell(context, bar_dict)
        
def daily_routine_second(context, bar_dict):
    """每日回调函"""
    # 使用计数器检查是否到达调仓时间 
    if context.count % 5 == 0:
        rebalance_buy(context, bar_dict)
        context.count = 0
    context.count += 1

def rebalance_plan(context, bar_dict):
    """
    计算调仓仓位,
    """
    stock_pool = get_stock_pool(context, bar_dict)#返回经过筛选的股票池
    stock_pool = sort_indicators(stocklist=stock_pool, context=context)#排序？
    stock_pool = stock_pool[:10]#取前十个。
    current_holdings = set(context.portfolio.positions.keys())#当前持仓股票
    stock_pool = set(stock_pool)#要买的股票
    context.sell_all = current_holdings - stock_pool#sell
    context.buy_all = stock_pool - current_holdings#buy
    #context.adjust_position = stock_pool.intersection(current_holdings)
    context.target_percent = 1.0 / len(
        stock_pool) if len(stock_pool) > 0 else 0.0

def rebalance_sell(context, bar_dict):
    """ 调仓函数   """
    for stk in context.sell_all:
        order_target_percent(stk, 0.0, MarketOrder())


def rebalance_buy(context, bar_dict):
    """    调仓函数    """
    for stk in context.buy_all:
        order_target_percent(stk, context.target_percent, MarketOrder())

def rebalance_plan_sell(context, bar_dict):
    """    调仓函数    """
    rebalance_plan(context, bar_dict)
    rebalance_sell(context, bar_dict)

def handle_bar(context, bar_dict):
    """    每分钟回调函数    """
    # 检查止盈止损
    profit_taken_stop_loss(context, bar_dict)
    #再来一个时间止损？
