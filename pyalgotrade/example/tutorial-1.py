#coding=utf-8
from pyalgotrade import strategy

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())
'''
getAdjClose', 'getAmount', 'getClose', 
'getDateTime', 'getExtraColumns', 'getFrequency', 
'getHigh', 'getLow', 'getOpen', 'getPrice',
 'getTypicalPrice', 'getUseAdjValue', 
 'getVolume', 'setUseAdjustedValue']
'''

from pyalgotrade import bar
from pyalgotrade import plotter
    
instrument = '600288'
market = 'SH'
fromDate = '20150201'
toDate ='20150221'
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
strat = MyStrategy(barfeed, pyalgotrade_id)
plt = plotter.StrategyPlotter(strat, True, True, True)
strat.run()
plt.plot()
