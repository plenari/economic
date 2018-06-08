# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import pandas as pd
import re
import datetime
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 在context中保存全局变量
    context.s1 = "000001.XSHE"
    # 实时打印日志
    #logger.info("RunInfo: {}".format(context.run_info))
    #{'order_id': 1516860659, 'trading_datetime': datetime.datetime(2017, 3, 31, 15, 0), 'datetime': datetime.datetime(2017, 3, 31, 15, 0), 'quantity': 1000, 'unfilled_quantity': 1000, 'order_book_id': '000001.XSHE', 'side': SIDE.BUY, 'position_effect': None, 'message': '订单被拒单: 可用资金不足。当前资金: 8246.66，000001.XSHE 下单所需资金: 9170.00。', 'filled_quantity': 0, 'status': ORDER_STATUS.REJECTED, 'price': 0, 'type': ORDER_TYPE.MARKET, 'avg_price': 0, 'transaction_cost': 0, 'frozen_price': 9.17}

    context.orders=pd.DataFrame()

# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    pass

def parse_order(context,order):
    order_dict=re.search('Order\(({.*?})\)',str(order)).group(1)
    order_dict=eval(order_dict)
    context.orders=pd.concat([context.orders,\
        pd.DataFrame.from_dict(order_dict,'index').T],ignore_index=True)

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！
    orde=order_shares(context.s1, 100)
    parse_order(context,orde)
    

# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    pass