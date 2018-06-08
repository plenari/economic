from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        #self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None
        self.info('%s %s'%(self.__sma[-1],self.__instrument))

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        print type(self.__position)
        # If a position was not opened, check if we should enter a long position.
        bar=bars[self.__instrument]
        if self.__position is None:
            if cross.cross_above(self.__prices,self.__sma)>0:
                shares=int(self.getBroker().getCash()*0.9/bar.getPrice())
                self.__position=self.enterLong(self.__instrument,shares,True)
                self.info('buy')
        elif not self.__position.exitActive() and cross.cross_below(self.__prices,self.__sma)>0:
            self.__position.exitMarket()
            self.info('sell')
            print self.__position.exitActive()