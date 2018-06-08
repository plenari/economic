from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
import sma_crossover

#feed
from pyalgotrade import bar
   
instrument = '600288'
market = 'SH'
fromDate = '20150201'
toDate ='20150515'
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

myStrategy = sma_crossover.SMACrossOver(barfeed,pyalgotrade_id, 10)

# Attach a returns analyzers to the strategy.
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy)
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
plt.getInstrumentSubplot("600288").addDataSeries("SMA", myStrategy.getSMA())
# Plot the simple returns on each bar.
plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())



# Run the strategy.
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

# Plot the strategy.
plt.plot()
