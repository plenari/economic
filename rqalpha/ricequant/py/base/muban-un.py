'''
模块化各个要求，以方便调用

# 仓位管理
# 涨跌停限制
# 新股与次新股过滤
# 调仓时间定制化
# 风险管理——根据大盘择时
# 私有化定制常用绩效表现指标
# 黑名单管理，回测中不建议使用，但实盘时有必要加入
# 白名单设置，防止仓位不达标时，买入白名单股票
# 特定板块剔除（创业板，st）
'''
#from rqalpha_plus.api import *
from datetime import datetime
import numpy as np
import pandas as pd

'''
策略设计：基本面选股+股票择时+大盘风险控制(定制)
1。 根据PE要求买入市值最小的十只股票
2。 对每一只持仓股票进行技术判断，若低于10日线，则卖出
3。 根据大盘走势，对持仓进行调整，若中证500和沪深300的20天收益率全部低于0，则第二天清仓
'''
# 初始化参数设置
def init(context):
    logger.info("Initializing...")

    context.period = 10  # 自定义调仓频率
    context.days_count = 0  # 调仓间隔天数统计

    context.filter_blacklist = True#白名单
    context.filter_whitelist = False#黑名单
    # context.filter_special_industry = True#排除某些行业
    context.filter_gem = True#过滤创业板
    context.filter_new_and_subnew = True#新股与次新股过滤

    context.selected_stocks_num = 100  # 股票池容量可以设置大一些，避免停牌股的影响
    context.to_buy_stocks_num = 10  # 实际持仓上线维持在10只股票

    context.select_by_pe = True#bool 
    context.max_pe = 100#
    context.min_pe = 10#

    # 输出各类参数
    logger.info("调仓日频率: %d 日" % (context.period))
    logger.info("备选股票数目: %d" % (context.selected_stocks_num))
    logger.info("购买股票数目: %d" % (context.to_buy_stocks_num))
    logger.info("是否根据PE选股: %s" % (context.select_by_pe))
    if context.select_by_pe:
        logger.info("最大PE: %s" % (context.max_pe))
        logger.info("最小PE: %s" % (context.min_pe))

    logger.info("是否过滤创业板股票: %s" % (context.filter_gem))
    logger.info("是否过滤黑名单股票: %s" % (context.filter_blacklist))
    logger.info("")
    if context.filter_blacklist:
        logger.info("当前股票黑名单：%s" % str(filter_black_list()))

    # 加载统计模块
    context.trade_stat = trade_stat()#交易策略的 实例
    
    context.stocks = []#

# 以什么标准进行选股，投资者可以自行定义
def before_trading(context):
    if context.select_by_pe:
        df = get_fundamentals(query(fundamentals.eod_derivative_indicator.pe_ratio).filter
                              (fundamentals.eod_derivative_indicator.pe_ratio > context.min_pe).filter
                              (fundamentals.eod_derivative_indicator.pe_ratio < context.max_pe).order_by
                              (fundamentals.eod_derivative_indicator.a_share_market_val_2.asc()).limit#A股市值不含限售股，升序排列
                              (context.selected_stocks_num))
        context.stocks_pool = df.columns.values

    else:#否则直接用市值排列。
        df = get_fundamentals(query(fundamentals.eod_derivative_indicator.a_share_market_val_2.asc()).
                              limit(context.selected_stocks_num))
        context.stocks_pool = df.columns.values


def handle_bar(context, bar_dict):
    logger.info("调仓时间统计：[%d]" % (context.days_count))

    # 计算指数过去20天的涨幅
    hs300 = '000300.XSHG'  # 沪深300指数
    zz500 = '000905.XSHG'  # 中证500指数
    hs300_return = calculate_return_rate(hs300,n=20)#对数收益率
    zz500_return = calculate_return_rate(zz500,n=20)
    logger.info("当前沪深300指数的20日涨幅 [%.2f%%]" % (hs300_return * 100))
    logger.info("当前中证500指数的20日涨幅 [%.2f%%]" % (zz500_return * 100))

    # 如果沪深300和中证500月度收益率皆为负，说明整个市场环境较差，清仓
    if hs300_return <= 0 and zz500_return <= 0:
        if context.filter_whitelist:
            #买之前不需要清仓吗？
            logger.info("为了避免空仓，买入白名单股票")#可以买入分级A
            adjust_position(context, filter_white_list())
            context.days_count += 1

        else:
            if context.portfolio.positions:
                clear_position(context)
            context.days_count = 0  # 由于清空了持仓，所以此时的调仓计数需要重新设置为0

    else:
        if context.days_count % context.period == 0:
            logger.info("==> 满足条件进行调仓")
            to_buy_stocks = selected_stocks(context, bar_dict)
            logger.info("层层筛选后可买股票: %s" % (to_buy_stocks))
            adjust_position(context, to_buy_stocks)
        context.days_count += 1


        # plot("weights", context.portfolio.market_value / context.portfolio.portfolio_value)


def selected_stocks(context, bar_dict):
    stocks_list = context.stocks_pool  # 根据基本面数据构建的股票池
    stocks_list = [s for s in stocks_list if bar_dict[s].is_trading and not is_st_stock(s)]  # 排除ST股票，排除停牌股票
    stocks_list = [s for s in stocks_list if filter_limit_up_down(s, bar_dict)]  # 排除涨跌停股票

    # 排除新股和次新股
    if context.filter_new_and_subnew:
        stocks_list = [s for s in stocks_list if s in filter_new_and_subnew_stocks(context, stocks_list)]
    # 排除创业板股票
    if context.filter_gem:
        stocks_list = [s for s in stocks_list if s in filter_gem_stocks(stocks_list)]
    # 排除黑名单股票
    if context.filter_blacklist:
        stocks_list = [s for s in stocks_list if s not in filter_black_list()]
    '''
    # 排除钢铁行业股票，但目前申万行业分类还未加入回测平台
    if context.filter_special_industry:
        stocks_list = [s for s in stocks_list if s not in filter_special_industry(stocks_list, industry_name="钢铁")]
    '''
    for stock in stocks_list:
        r = calculate_return_rate(stock, n=10)  # 计算两周收益率
        if r > 0:
            context.stocks.append(stock)

    context.stocks = context.stocks[: context.to_buy_stocks_num]
    return context.stocks


# 计算过去20天某只股票和特定指数的涨跌情况
def calculate_return_rate(stock, n=20):
    #为什么用指数形式的涨幅呢？
    p = history_bars(stock, n, "1d", "close")  # It's a np.array()
    r = np.log(p[-1]/p[0])
    return r


# 调仓设置，之前我们总是等比例分配仓位，且不断调仓，但是该种方法容易卖出表现好的股票，而多买入表现较差的股票
def adjust_position(context, stocks_pool):
    '''
    #卖出现有的，买入stocks_pool 
    '''
    for stock in context.portfolio.positions:
        if stock not in stocks_pool:
            position = context.portfolio.positions[stock]  # 在每一次卖出时，根据盈亏计算胜率
            context.trade_stat.watch(stock, position)  # context.portfolio.positions[stock].quantity

            logger.info("不再满足持仓要求，将所持股票【{0}】仓位清空".format(stock))
            order_target_percent(stock, 0)

        # else:
        #     logger.info("股票{0}已经在持仓中".format(stock))
    #卖出之后是否立即能卖掉。
    holding_number = len(context.portfolio.positions)
    if context.to_buy_stocks_num > holding_number:
        #如果还有新的持仓名额。将剩余的现金等额分配
        value = context.portfolio.cash / (context.to_buy_stocks_num - holding_number)
        for stock in stocks_pool:
            if context.portfolio.positions[stock].quantity == 0:
                order_target_value(stock, value)
                #为什么这么谨慎？
                if len(context.portfolio.positions) == context.to_buy_stocks_num:  # 达到持仓限额时，停止买入
                    break


def clear_position(context):
    '''
    清空投资组合里的所有股票
    '''
    logger.info("市场不好，清空股票@_@")
    for stock in context.portfolio.positions:
        position = context.portfolio.positions[stock]
        order_target_value(stock, 0)
        # 在每次卖出时，统计被卖出的股票的盈亏情况
        context.trade_stat.watch(stock, position)


# 涨跌停限制
def filter_limit_up_down(stock, bar_dict):
    '''
    get last price between the limit_down and limit_up
    事实上这个不需要这样判断，因为涨跌停限制的东西不一样
    '''
    return bar_dict[stock].limit_down < bar_dict[stock].last < bar_dict[stock].limit_up


def filter_new_and_subnew_stocks(context, stocks_pool, days=60):
    '''
    过滤stocks_pool里的新股和次新股，默认以60天为选取标准    
    '''
    stocks_list = []
    for stock in stocks_pool:
        temp = instruments(stock).listed_date
        diff = (context.now - temp).days
        if diff > days:
            stocks_list.append(stock)
    return stocks_list

def filter_black_list():
    '''建立黑名单，比如年报、季报净利润大幅预减的公司或者即将被ST或已经被ST的公司
    '''
    blacklists = ["000037.XSHE", "000613.XSHG"]
    return blacklists



def filter_white_list():
    '''
    建立白名单制度，主要是为了满足参赛时，
    当大盘面临系统性风险时，仓位保持在最低仓位上，以蓝筹股为主
    '''
    whitelists = ["600519.XSHG", "601398.XSHG", "601318.XSHG", "000538.XSHE", "000002.XSHE"]
    return whitelists




def filter_special_industry(stocks_pool, industry_name=None):
    '''不同于黑名单的特定股票排除，此处决定是否删除特定行业的股票，比如夕阳行业股，煤炭，钢铁等
        默认不予排除
    '''
    if industry_name is None:
        return stocks_pool
    else:

def filter_gem_stocks(stocks_pool):
    '''
    默认不删除创业板股票
    '''
    return [s for s in stocks_pool if not s.startswith("300")]

def after_trading(context):
    '''
    收盘后计算相关结果
    '''
    context.trade_stat.report(context)


class trade_stat():
    '''私有化定制常用绩效指标
    '''
    def __init__(self):
        self.trade_total_count = 0  # 总的交易次数统计,记录交易次数便于统计胜率
        self.trade_success_count = 0  # 交易次数中成功的次数统计
        self.trade_continuous_growth = 0  # 收益连续为正天数统计
        self.trade_continuous_descent = 0  # 收益连续为负天数统计
        self.statis = {'win': [], 'loss': []}  # 最大盈利与最大亏损对应的股票及其幅度
        self.continuous = {"growth": 0, "descent": 0}  # 连续盈利和亏损对应的天数

    def reset(self):
        self.trade_total_count = 0
        self.trade_success_count = 0
        self.trade_continuous_growth = 0
        self.trade_continuous_descent = 0
        self.statis = {'win': [], 'loss': []}
        self.continuous = {"growth": 0, "descent": 0}

    def watch(self, stock, sale_position):
        '''暂且只针对单只股票卖出仓位统计，如果想要增加功能，需要用pd.DataFrame()来保持。
           position 和account 的market_value 不同。
           注意：watch ,其实就是sell？？,
        '''
        self.trade_total_count += 1
        amount = sale_position.quantity
        avg_cost = sale_position.avg_price  #建仓平均成本

        current_value = sale_position.market_value#现在市值
        '''如果只卖出了一半，能统计出来吗？'''
        cost = amount * avg_cost#建仓成本

        percent = round((current_value - cost) / cost * 100, 2)
        if current_value > cost:#现在市值大于建仓成本
            self.trade_success_count += 1
            win = [stock, percent]#加入那么多怎么控制？
            self.statis['win'].append(win)
        else:
            loss = [stock, percent]
            self.statis['loss'].append(loss)
            
    def stat_continuous(self, context):
        '''
        根据当日盈亏来判断,连续涨跌天数，和日内最大涨跌幅
        '''        

        if context.portfolio.daily_pnl > 0:
            self.trade_continuous_growth += 1
            self.trade_continuous_descent = 0

        elif context.portfolio.daily_pnl < 0:
            self.trade_continuous_descent += 1
            self.trade_continuous_growth = 0

        if self.trade_continuous_growth > self.continuous["growth"]:
            self.continuous["growth"] = self.trade_continuous_growth

        if self.trade_continuous_descent > self.continuous["descent"]:
            self.continuous["descent"] = self.trade_continuous_descent

        return self.continuous["growth"], self.continuous["descent"]


    # 统计单次盈利最高的股票
    def statis_most_win_percent(self):
        result = {}
        for statis in self.statis['win']:
            if {} == result:
                result['stock'] = statis[0]
                result['value'] = statis[1]
            else:
                if statis[1] > result['value']:
                    result['stock'] = statis[0]
                    result['value'] = statis[1]
        return result

    # 统计单次亏损最高的股票
    def statis_most_loss_percent(self):
        result = {}
        for statis in self.statis['loss']:
            if {} == result:
                result['stock'] = statis[0]
                result['value'] = statis[1]
            else:
                if statis[1] < result['value']:
                    result['stock'] = statis[0]
                    result['value'] = statis[1]
        return result

    # 统计总盈利金额
    def statis_total_profit(self, context):
        return context.portfolio.portfolio_value - context.portfolio.starting_cash

    # 打印胜率
    def print_win_rate(self, current_date, print_date, context):
        if str(current_date) == str(print_date):
            win_rate = 0  # 胜率每天更新，所以需要每天进行赋值归0
            if 0 < self.trade_total_count and 0 < self.trade_success_count:
                win_rate = round(self.trade_success_count / float(self.trade_total_count), 3)

            most_win = self.statis_most_win_percent()
            most_loss = self.statis_most_loss_percent()
            continuous_growth_days, continuous_descent_days = self.stat_continuous(context)

            starting_cash = context.portfolio.starting_cash
            total_profit = self.statis_total_profit(context)
            if len(most_win) == 0 or len(most_loss) == 0:
                return

            print("-")
            print('------------绩效报表------------')
            print('交易次数: {0}, 盈利次数: {1}, 胜率: {2}'.format(self.trade_total_count, self.trade_success_count,
                                                         str(win_rate * 100) + str('%')))
            print('单次盈利最高: {0}, 盈利比例: {1}%'.format(most_win['stock'], most_win['value']))
            print('单次亏损最高: {0}, 亏损比例: {1}%'.format(most_loss['stock'], most_loss['value']))
            print("最大连续盈利天数: {0}".format(continuous_growth_days))
            print("最大连续亏损天数: {0}".format(continuous_descent_days))
            print('总资产: {0}, 本金: {1}, 盈利: {2}, 盈亏比率：{3}%'.format(starting_cash + total_profit, starting_cash,
                                                                 total_profit, total_profit / starting_cash * 100))
            print('--------------------------------')
            print("-")

    def report(self, context):
        cash = context.portfolio.cash
        total_value = context.portfolio.portfolio_value
        position = 1 - cash / total_value
        logger.info("收盘后持仓概况: %s" % str(list(context.portfolio.positions)))
        logger.info("仓位概况: %.2f" % position)
        logger.info("当日盈亏: %.2f" % context.portfolio.daily_pnl)
        self.print_win_rate(context.now.strftime("%Y-%m-%d"), context.now.strftime("%Y-%m-%d"), context)
