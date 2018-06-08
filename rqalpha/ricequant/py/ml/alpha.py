# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import numpy as np 
import pandas as pd 
from numpy import abs 
from numpy import log
from numpy import sign
from scipy.stats import rankdata#对数据排名

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 初始化待买股票池
    context.stock_pool=[]
    # 初始化购买权重
    context.weight=[]
    # 获取市场所有股票
    context.stock=all_instruments(type='CS').order_book_id
    scheduler.run_daily(stoploss)
    context.drawdown= 0.1 # 回撤限度 10% 
    context.maxvalue=pd.DataFrame()#最高价
    
# 止损策略
def stoploss(context,bar_dict):#
    
    for stock in context.portfolio.positions:
        market_value=context.portfolio.positions[stock].market_value# 该股市场价值 单位（RMB）
        #如果一只股票买了两次，这里会不会有？问题
        bought_value=context.portfolio.positions[stock].avg_price#该股初始价值 单位（RMB）
        
        if stock in context.maxvalue:#已经记录最高价
            stockdic=context.maxvalue[stock]#获取最高价
            maxvalue=stockdic[0]#            
            del context.maxvalue[stock]            
            #currSP=context.initSPM*(1+math.floor((maxvalue/bought_value-1)/context.step)*context.increment) #阶梯止损算法 例： 该股市值增加10%， 止盈比例提高 5% 
            
            temp=pd.DataFrame({str(stock):[max(maxvalue,market_value)]})
            context.maxvalue=pd.concat([context.maxvalue,temp], axis=1, join='inner') # 更新其盘中最高价值和先阶段比例。 
            drawdown=1-market_value/max(maxvalue,market_value)
            
            print(str(stock)+'的成本为：' +str( bought_value) +', 最高价值为：'+str(maxvalue)+'现价值为：'+ str(market_value))
            print(str(stock) +'的现 回撤为: ' +str(drawdown*100)+ '%')
            #logger.info ( type(market_value))
            #logger.info(type(ontext.maxvalue[stock].values)))
            
            if drawdown>context.drawdown:# 现价低于 原价一定比例
                order_target_percent(stock,0)
                print(str(stock)+'回撤大于'+ str(context.drawdown*100)+ '%'+'  触发止损')
                del context.maxvalue[stock]


def createdic(context,bar_dict,stock):
    if stock not in context.maxvalue.columns:
        temp=pd.DataFrame({str(stock):[context.portfolio.positions[stock].avg_price]})    
        context.maxvalue = pd.concat([context.maxvalue, temp], axis=1, join='inner')
    print(context.maxvalue)
    
    
# 计算alpha时会使用的函数
def ts_num(df,window=10):
    return df.rolling(window).sum()

def sma(df,window=10):
    return df.rolling(window).mean()

def stddev(df,window=10):
    return df.rolling(window).std()

def correlation(x,y,window=10):#相关系数
    return x.rolling(window).corr(y)

def covariance(x,y,window=10):#协方差
    return x.rolling(window).cov(y)

def rolling_rank(na):#
    return rankdata(na)[-1]

def ts_rank(window=10):#
    return rolling(window).apply(rolling_rank)

def rolling_prod(na):#
    return na.prod(na)
    
def product(df,window=10):#厉害
    return df.rolling(window).apply(rolling_prod)

def ts_min(df,window=10):#
    return df.rolling(window).min()
    
def ts_max(df,window=10):
    return df.rolling(window).max()

def delta(df,period=1):#different
    return df.diff(period)
    
def delay(df,period=1):#延迟一天
    return df.shift(period)

def rank(df):#
    return df.rank(axis=1,pct=True)

def scale(df,k=1):##
    return df.mul(k).div(np.abs(df).sum())

def ts_argmax(df,window=10):#最大值所在的位置
    return df.rolling(window).apply(np.argmax)+1

def ts_argmin(df,window=10):#
    return df.rolling(window).apply(np.argmin)+1
    
def decay_linear(df,period=10):#
    if df.isnull().values.any():#只要有一个null
        df.fillna(method='ffill',inplace=True)#用前边？
        df.fillna(method='dfill',inplace=True)#用后边
        df.fillna(value=0,inplace=True)#
    na_lwma=np.zeros_like(df)#
    na_lwma[:period,:]=df.ix[:period,:]
    na_series = df.as_matrix()#转换成np.array
    divisor = df.as_matrix()#
    y =(np.arrange(period)+1)*1.0/divisor
    for row in range(period+1,df.shape[0]):
        x=na_series[row-period+1:row+1,:]
        na_lwma[row,:]-(np.dot(x.T,y))
    return pd.DataFrame(na_lwma,index=df.index,columns=df.columns)
    
    
# 定义计算alpha值的类
class Alphas(object):
    def __init__(self, pn_data):
        """
        :传入参数 pn_data: pandas.Panel
        """
        # 获取历史数据
        self.open = pn_data['open']
        self.high = pn_data['high']
        self.low = pn_data['low']
        self.close = pn_data['close']
        self.volume = pn_data['volume']
        self.returns = self.close.pct_change()#百分比变化
    
    #   每个因子的计算公式：
    #   alpha001:(rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) -0.5) 
    def alpha001(self):
        inner = self.close
        inner[self.returns < 0] = stddev(self.returns, 20)
        return rank(ts_argmax(inner ** 2, 5))
        
    #  alpha002:(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6)) 
    def alpha002(self):
        df = -1 * correlation(rank(delta(log(self.volume), 2)), rank((self.close - self.open) / self.open), 6)
        return df.replace([-np.inf, np.inf], 0).fillna(value=0)

    # alpha003:(-1 * correlation(rank(open), rank(volume), 10))  
    def alpha003(self):
        df = -1 * correlation(rank(self.open), rank(self.volume), 10)
        return df.replace([-np.inf, np.inf], 0).fillna(value=0)
    
    # alpha004: (-1 * Ts_Rank(rank(low), 9)) 
    def alpha004(self):
        return -1 * ts_rank(rank(self.low), 9)
    
    #  alpha006: (-1 * correlation(open, volume, 10)) 
    def alpha006(self):
        df = -1 * correlation(self.open, self.volume, 10)
        return df.replace([-np.inf, np.inf], 0).fillna(value=0)

    # alpha007: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1* 1)) 
    def alpha007(self):
        adv20 = sma(self.volume, 20)
        alpha = -1 * ts_rank(abs(delta(self.close, 7)), 60) * sign(delta(self.close, 7))
        alpha[adv20 >= self.volume] = -1
        return alpha
    
    # alpha008: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)),10)))) 
    def alpha008(self):
        return -1 * (rank(((ts_sum(self.open, 5) * ts_sum(self.returns, 5)) -
                          delay((ts_sum(self.open, 5) * ts_sum(self.returns, 5)), 10))))
    
    # alpha009:((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ?delta(close, 1) : (-1 * delta(close, 1)))) 
    def alpha009(self):
        delta_close = delta(self.close, 1)
        cond_1 = ts_min(delta_close, 5) > 0
        cond_2 = ts_max(delta_close, 5) < 0
        alpha = -1 * delta_close
        alpha[cond_1 | cond_2] = delta_close
        return alpha
    
    # alpha010: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0)? delta(close, 1) : (-1 * delta(close, 1))))) 
    def alpha010(self):
        delta_close = delta(self.close, 1)
        cond_1 = ts_min(delta_close, 4) > 0
        cond_2 = ts_max(delta_close, 4) < 0
        alpha = -1 * delta_close
        alpha[cond_1 | cond_2] = delta_close
        return alpha
    
    #  alpha012:(sign(delta(volume, 1)) * (-1 * delta(close, 1))) 
    def alpha012(self):
        return sign(delta(self.volume, 1)) * (-1 * delta(self.close, 1))
    
    # alpha013:(-1 * rank(covariance(rank(close), rank(volume), 5))) 
    def alpha013(self):
        return -1 * rank(covariance(rank(self.close), rank(self.volume), 5))

    #  alpha014:((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10)) 
    def alpha014(self):
        df = correlation(self.open, self.volume, 10)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * rank(delta(self.returns, 3)) * df

    # alpha015:(-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3)) 
    def alpha015(self):
        df = correlation(rank(self.high), rank(self.volume), 3)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * ts_sum(rank(df), 3)

    #  alpha016:(-1 * rank(covariance(rank(high), rank(volume), 5))) 
    def alpha016(self):
        return -1 * rank(covariance(rank(self.high), rank(self.volume), 5))

    # alpha017: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) *rank(ts_rank((volume / adv20), 5))) 
    def alpha017(self):
        adv20 = sma(self.volume, 20)
        return -1 * (rank(ts_rank(self.close, 10)) *
                     rank(delta(delta(self.close, 1), 1)) *
                     rank(ts_rank((self.volume / adv20), 5)))
    
    # alpha018: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open,10)))) 
    def alpha018(self):
        df = correlation(self.close, self.open, 10)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * (rank((stddev(abs((self.close - self.open)), 5) + (self.close - self.open)) +
                          df))

    #  alpha019:((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns,250)))))
    def alpha019(self):
        return ((-1 * sign((self.close - delay(self.close, 7)) + delta(self.close, 7))) *
                (1 + rank(1 + ts_sum(self.returns, 250))))

    # alpha020: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open -delay(low, 1))))
    def alpha020(self):
        return -1 * (rank(self.open - delay(self.high, 1)) *
                     rank(self.open - delay(self.close, 1)) *
                     rank(self.open - delay(self.low, 1)))

    # alpha012: ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1 * 1) : (((sum(close,2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume /adv20) == 1)) ? 1 : (-1 * 1)))) 
    def alpha021(self):
        cond_1 = sma(self.close, 8) + stddev(self.close, 8) < sma(self.close, 2)
        cond_2 = sma(self.volume, 20) / self.volume < 1
        alpha = pd.DataFrame(np.ones_like(self.close), index=self.close.index,
                             columns=self.close.columns)
        alpha[cond_1 | cond_2] = -1
        return alpha

    # alpha022:(-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20)))) 
    def alpha022(self):
        df = correlation(self.high, self.volume, 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * delta(df, 5) * rank(stddev(self.close, 20))

    # alpha023: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0) 
    def alpha023(self):
        cond = sma(self.high, 20) < self.high
        alpha = pd.DataFrame(np.zeros_like(self.close), index=self.close.index,
                             columns=self.close.columns)
        alpha[cond] = -1 * delta(self.high, 2)
        return alpha

    # alpha024: ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) ||((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close,100))) : (-1 * delta(close, 3)))  
    def alpha024(self):
        cond = delta(sma(self.close, 100), 100) / delay(self.close, 100) <= 0.05
        alpha = -1 * delta(self.close, 3)
        alpha[cond] = -1 * (self.close - ts_min(self.close, 100))
        return alpha
    
    #   alpha026:(-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3)) 
    def alpha026(self):
        df = correlation(ts_rank(self.volume, 5), ts_rank(self.high, 5), 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * ts_max(df, 3)

    # alpha028:scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close)) 
    def alpha028(self):
        adv20 = sma(self.volume, 20)
        df = correlation(adv20, self.low, 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return scale(((df + ((self.high + self.low) / 2)) - self.close))
    
    # alpha029:(min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1),5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5)) 
    def alpha029(self):
        return (ts_min(rank(rank(scale(log(ts_sum(rank(rank(-1 * rank(delta((self.close - 1), 5)))), 2))))), 5) +
                ts_rank(delay((-1 * self.returns), 6), 5))
    
    # alpha0230:(((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20)) 
    def alpha030(self):
        delta_close = delta(self.close, 1)
        inner = sign(delta_close) + sign(delay(delta_close, 1)) + sign(delay(delta_close, 2))
        return ((1.0 - rank(inner)) * ts_sum(self.volume, 5)) / ts_sum(self.volume, 20)

    # alpha031:((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 *delta(close, 3)))) + sign(scale(correlation(adv20, low, 12)))) 
    def alpha031(self):
        adv20 = sma(self.volume, 20)
        df = correlation(adv20, self.low, 12)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(self.close, 10)))), 10)))) +
                 rank((-1 * delta(self.close, 3)))) + sign(scale(df)))

    # alpha033: rank((-1 * ((1 - (open / close))^1))) 
    def alpha033(self):
        return rank(-1 + (self.open / self.close))
    
    # alpha034: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1))))) 
    def alpha034(self):
        inner = stddev(self.returns, 2) / stddev(self.returns, 5)
        inner = inner.replace([-np.inf, np.inf], 1).fillna(value=1)
        return rank(2 - rank(inner) - rank(delta(self.close, 1)))
    
    # alpha035:((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 -Ts_Rank(returns, 32))) 
    def alpha035(self):
        return ((ts_rank(self.volume, 32) *
                 (1 - ts_rank(self.close + self.high - self.low, 16))) *
                (1 - ts_rank(self.returns, 32)))

    # alpha037:(rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close))) 
    def alpha037(self):
        return rank(correlation(delay(self.open - self.close, 1), self.close, 200)) + rank(self.open - self.close)
    
    # alpha038: ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open))) 
    def alpha038(self):
        inner = self.close / self.open
        inner = inner.replace([-np.inf, np.inf], 1).fillna(value=1)
        return -1 * rank(ts_rank(self.open, 10)) * rank(inner)

    # alpha039:((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 +rank(sum(returns, 250)))) 
    def alpha039(self):
        adv20 = sma(self.volume, 20)
        return ((-1 * rank(delta(self.close, 7) * (1 - rank(decay_linear(self.volume / adv20, 9))))) *
                (1 + rank(ts_sum(self.returns, 250))))
    
    # alpha040: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10)) 
    def alpha040(self):
        return -1 * rank(stddev(self.high, 10)) * correlation(self.high, self.volume, 10)

    # alpha43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8)) 
    def alpha043(self):
        adv20 = sma(self.volume, 20)
        return ts_rank(self.volume / adv20, 20) * ts_rank((-1 * delta(self.close, 7)), 8)

    # alpha04: (-1 * correlation(high, rank(volume), 5)) 
    def alpha044(self):
        df = correlation(self.high, rank(self.volume), 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * df
    
    # alpha045: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *rank(correlation(sum(close, 5), sum(close, 20), 2)))) 
    def alpha045(self):
        df = correlation(self.close, self.volume, 2)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * (rank(sma(delay(self.close, 5), 20)) * df *
                     rank(correlation(ts_sum(self.close, 5), ts_sum(self.close, 20), 2)))

    # alpha046: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ?(-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 :((-1 * 1) * (close - delay(close, 1))))) 
    def alpha046(self):
        inner = ((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10)
        alpha = (-1 * delta(self.close))
        alpha[inner < 0] = 1
        alpha[inner > 0.25] = -1
        return alpha

    # alpha049:(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))
    def alpha049(self):
        inner = (((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10))
        alpha = (-1 * delta(self.close))
        alpha[inner < -0.1] = 1
        return alpha
    
    # alpha051:(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1)))) 
    def alpha051(self):
        inner = (((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10))
        alpha = (-1 * delta(self.close))
        alpha[inner < -0.05] = 1
        return alpha

    # alpha052: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) -sum(returns, 20)) / 220))) * ts_rank(volume, 5)) 
    def alpha052(self):
        return (((-1 * delta(ts_min(self.low, 5), 5)) *
                 rank(((ts_sum(self.returns, 240) - ts_sum(self.returns, 20)) / 220))) * ts_rank(self.volume, 5))

    # alpha053:(-1 * delta((((close - low) - (high - close)) / (close - low)), 9)) 
    def alpha053(self):
        inner = (self.close - self.low).replace(0, 0.0001)
        return -1 * delta((((self.close - self.low) - (self.high - self.close)) / inner), 9)

    # alpha054:((-1 * ((low - close) * (open^5))) / ((low - high) * (close^5))) 
    def alpha054(self):
        inner = (self.low - self.high).replace(0, -0.0001)
        return -1 * (self.low - self.close) * (self.open ** 5) / (inner * (self.close ** 5))
        
    # alpha055: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low,12)))), rank(volume), 6)) 
    def alpha055(self):
        divisor = (ts_max(self.high, 12) - ts_min(self.low, 12)).replace(0, 0.0001)
        inner = (self.close - ts_min(self.low, 12)) / (divisor)
        df = correlation(rank(inner), rank(self.volume), 6)
        return -1 * df.replace([-np.inf, np.inf], 0).fillna(value=0)
    
    # alpha060: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) -scale(rank(ts_argmax(close, 10)))))) 
    def alpha060(self):
        divisor = (self.high - self.low).replace(0, 0.0001)
        inner = ((self.close - self.low) - (self.high - self.close)) * self.volume / divisor
        return - ((2 * scale(rank(inner))) - scale(rank(ts_argmax(self.close, 10))))
        

# 在交易前计算所有股票alpha因子值，取最高的10组进行买入，这里也可以取最低的10组进行卖空操作
def before_trading(context):
    # 获取当前交易日日期
    date=str(context.now)[0:10]
    # 获取10个交易日前信息，根据选取因子所需计算的日期决定
    date=get_previous_trading_date(date,n=10)
    # 获取股票历史数据,获得10交易日，根据上边计算周期，岂不是只能得到一个数据。
    pn_data=get_price(context.stock, start_date=date, end_date=None, frequency='1d', fields=None, adjust_type='pre', skip_suspended=False)
    # 实例化Alpha对象
    alpha=Alphas(pn_data)  
    # 用户所选取的因子，返回所有股票的该因子值，这里选取001作为示范，用户可修改为其他自己感兴趣的因子
    alpha_use=alpha.alpha001()#
    # 取得交易日前一天的因子值
    result=alpha_use.tail(1)#最后一天
    # 将空值赋为0
    result[np.isnan(result)] = 0
    result=result.T
    logger.info('result: {}'.format(result))
    # 获取上一交易日日期
    today=str(context.now)[0:10]
    yesterday=get_previous_trading_date(today)###
    stock=result.sort_values(by=yesterday,ascending=False)[:10]###
    # 计算每只股票的权重，按照因子大小计算权重
    context.weight=stock.values/sum(stock.values)
    # 将选出的股票加入到待买股票池中
    context.stock_pool=stock.index
    
def handle_bar(context, bar_dict):
    # 获取权重的计数器
    i=0
    # 获取当前持有股票
    hand_stock=context.portfolio.positions
    # 当前的现金，用于做空时使用，只做多时不考虑
    cash=context.portfolio.cash
    # 当前持有的股票不在待买股票池中，亦即因子值跌出前10，就清仓。
    for stock in hand_stock:
         if stock not in context.stock_pool:
             order_target_percent(stock,0)
    # 买入待买股票池中的股票，买入权重为因子值大小
    for stock in context.stock_pool:
        weight=float(context.weight[i])
        # order_target_value(stock,-1*weight*cash) ，#做空时使用
        order_target_percent(stock,weight)
        createdic(context,bar_dict,stock)
        i+=1
        
        
        
        