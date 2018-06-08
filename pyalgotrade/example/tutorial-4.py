from pyalgotrade import strategy
from pyalgotrade.technical import ma
import os 

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy,self).__init__(feed, 10000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        #self.setUseAdjustedValues(False)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f,%s" % (execInfo.getPrice(),execInfo.getQuantity()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("sell at $%.2f,%s" % (execInfo.getPrice(),execInfo.getQuantity()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        
        if self.__sma[-1] is None:
            return 
        bar=bars[self.__instrument]
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                self.__position=self.enterLong(self.__instrument,5)
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive() and self.getBroker().getShares>2:
        
            self.__position=self.enterShort(self.__instrument,2)
            #self.info('sell at %s,2'%bar.getPrice())

from pyalgotrade import bar
from pyalgotrade import plotter
    
instrument = '600519'
market = 'SH'
fromDate = '20160201'
toDate ='20160515'
frequency = bar.Frequency.DAY
filepath = os.path.join(r'E:\xsj\day', instrument + market + ".csv")
from pyalgotrade.cn.csvfeed import Feed
 
barfeed = Feed(frequency)
barfeed.setDateTimeFormat('%Y-%m-%d')
barfeed.loadBars(instrument, market, fromDate, toDate, filepath)
  
pyalgotrade_id = instrument + '.' + market
strat=MyStrategy(barfeed,pyalgotrade_id,14)
plt=plotter.StrategyPlotter(strat, True, True, True)
strat.run()
plt.plot()

print "Final portfolio value: $%.2f" % strat.getBroker().getEquity()

