from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 4)
        self.__sma = ma.SMA(self.__rsi, 5)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__rsi[-1], self.__sma[-1]))

#feed
from pyalgotrade import bar
from pyalgotrade import plotter
    
instrument = '600288'
market = 'SH'
fromDate = '20150201'
toDate ='20150215'
frequency = bar.Frequency.DAY

import os
if frequency == bar.Frequency.MINUTE:
    path = os.path.join(r'C:\Users\linner\Desktop\learn\pyalgo\histdata', 'minute')
elif frequency == bar.Frequency.DAY:
    path = os.path.join( r'C:\Users\linner\Desktop\learn\pyalgo\histdata', 'day')
filepath = os.path.join(path, instrument + market + ".csv")
    
    
#############################################don't change ############################33  
from pyalgotrade.cn.csvfeed import Feed
 
barfeed = Feed(frequency)
barfeed.setDateTimeFormat('%Y-%m-%d')
barfeed.loadBars(instrument, market, fromDate, toDate, filepath)
  
pyalgotrade_id = instrument + '.' + market
strat=MyStrategy(barfeed,pyalgotrade_id)
plt=plotter.StrategyPlotter(strat, True, True, True)
strat.run()
plt.plot()
