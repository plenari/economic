from pyalgotrade import strategy
from pyalgotrade.technical import ma


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy,self).__init__(feed)
        # We want a 15 period SMA over the closing prices.
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 5)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        if self.__sma[-1]:
            self.info("%s %s,%s" % (bar.getClose(), self.__sma[-1],(bar.getClose()>self.__sma[-1])))

		
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
    path = os.path.join('histdata', 'minute')
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