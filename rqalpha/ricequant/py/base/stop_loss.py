#coding=utf-8

#当前持仓
hold=set([i for i,j in context.portfolio.positions.items() if j.quantity>1])

#
def profit_stop_loss_profit(context, bar_dict):
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

#时间止损，还需要修改。
def parse_order(context,order):
    '''在初始化的地方加入这句话，context.orders=pd.DataFrame()
    然后每次调用orderd都要传入parse_order(context,order_)
    进一步修改，只需要每天收盘时运行就可以，判断持仓股票里那只增加了，或者新增了那只股票，然后保存到收盘价。
    '''

    if order.side==SIDE.BUY:
        order_dict=re.search('Order\(({.*?})\)',str(order)).group(1)
        order_dict=eval(order_dict)
        context.orders=pd.concat([context.orders,\
            pd.DataFrame.from_dict(order_dict,'index').T],ignore_index=True)
    if order.side==SIDE.SELL and context.portfolio.positions[order.order_book_id].quantity<100:
        #drop 卖掉的股票数据。
        context.orders.drop(np.where(context.orders.order_book_id==order.order_book_id),inplace=True)
        
def profit_stop_loss_time(context,bar_dict):
    '''
    #context.orders 保存所有的order
    'datetime': datetime.datetime(2017, 1, 18, 15, 0), 'quantity': 100, 'unfilled_quantity': 0, 'order_book_id': '000001.XSHE',
    side  'filled_quantity': 100, 'status': ORDER_STATUS.FILLED,  'avg_price': 9.17, 
    如果一直股票长时间不长，或者不跌，就要卖掉。
    '''
    threshold_time =30
    threshold_stop =0.05
    '''这个地方可以用dict.items()吧?'''
    for s, position in six.iteritems(context.portfolio.positions):
        '''stock position,平均持仓成本'''
        avg_cost = position.avg_price
        profit_percent = (bar_dict[s].last - avg_cost) / avg_cost                #取该股票最后一次买入的日期
        last_time_buy_stock=context.orders.query('order_book_id==@context.s1 and side==@SIDE.BUY').sort_values(by='datetime').datetime.iloc[-1]
        if profit_percent < threshold_profit_taken and (context.now-last_time_buy_stock).days>threshold_time:
            #如果收益不好，且持有时间过长，买到。
            order_target_percent(s, 0.0, MarketOrder())



def stoploss_from_high(context,bar_dict):
    '''使用方法：初始化context.maxvalue=pd.Series()
    吊顶止损，需要每天晚上运行。保存并更新最大值。
    如果当前值比最大值下跌9%则清空改股票。'''
    holds=[i for i,j in context.portfolio.positions.items() if j.quantity>1]#持仓股票
    for stock in holds:
        high=current_snapshot[stock].high#today's high values
        current=current_snapshot[stock].last#current values
        if stock in context.maxvalue.columns:#持仓股票已经记录了
            highest=context.maxvalue.stock[0]#之前最大值
            context.maxvalue.stock=[max(high,highest)]#更新最大值
        else:
            context.maxvalue.stock=[bar_dict[stock].high]
            highest=high
        #从最大值处跌去10%止损。
        if current<highest*0.9:#这个比例也可以是变化的。
            order_target_percent(stock,0)
            del context.maxvalue[stock]