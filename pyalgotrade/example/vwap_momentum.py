from pyalgotrade import strategy
from pyalgotrade.technical import vwap
from pyalgotrade.stratanalyzer import sharpe
import os

class VWAPMomentum(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, vwapWindowSize, threshold):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__vwap = vwap.VWAP(feed[instrument], vwapWindowSize)
        self.__threshold = threshold

    def getVWAP(self):
        return self.__vwap

    def onBars(self, bars):
        vwap = self.__vwap[-1]
        if vwap is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        price = bars[self.__instrument].getClose()
        notional = shares * price

        if price > vwap * (1 + self.__threshold) and notional < 1000000:
            self.marketOrder(self.__instrument, 100)
            #self.info('buy 100 at %.2f'%price)
            #print self.getBroker().getPositions()
        elif price < vwap * (1 - self.__threshold) and notional > 0:
            self.limitOrder(self.__instrument, price*1.05,-100,True,True)
            #self.info('sell 100 at %.2f'%price)
        
        if len(self.getBroker().getActiveOrders()):
            for i in self.getBroker().getActiveOrders():
                if i.getAge()>5:
                    self.getBroker().getActiveOrders()[-1].setState(4)
                    #print self.getBroker().getActiveOrders()[-1].getState()
                    print self.getBroker().getActiveOrders()[-1]
from pyalgotrade import bar
from pyalgotrade import plotter
from pyalgotrade.cn.csvfeed import Feed
instrument = '600519'
market = 'SH'
fromDate = '20150201'
toDate ='20160315'
frequency = bar.Frequency.DAY
filepath = os.path.join(r'E:\xsj\day', instrument + market + ".csv")
 
barfeed = Feed(frequency)
barfeed.setDateTimeFormat('%Y-%m-%d')
barfeed.loadBars(instrument, market, fromDate, toDate, filepath)
  
pyalgotrade_id = instrument + '.' + market
vwapWindowSize=10
threshold=0.05
strat = VWAPMomentum(barfeed, pyalgotrade_id, vwapWindowSize, threshold)
plt=plotter.StrategyPlotter(strat, True, True, True)
strat.run()
plt.plot()

print "Final portfolio value: $%.2f" % strat.getBroker().getEquity()