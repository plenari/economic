from pyalgotrade.cn.csvfeed import Feed
import itertools
from pyalgotrade.optimizer import local
import thrSMA
from pyalgotrade import bar
import os
from pyalgotrade import plotter
def parameters_generator():
    instrument=['600519.SH']
    short= range(4,15)
    mid = range(17,30)
    long = range(30,60)
    up = range(5,16)
    return itertools.product(instrument, short,mid,long,up)

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    instrument = '600519'
    market = 'SH'
    fromDate = '20100601'
    toDate ='20150101'
    pyalgotrade_id = instrument + '.' + market
    paras=parameters_generator()
    frequency = bar.Frequency.DAY
    filepath = os.path.join(r'E:\xsj\day', instrument + market + ".csv")      
    barfeed = Feed(frequency)
    barfeed.setDateTimeFormat('%Y-%m-%d')
    barfeed.loadBars(instrument, market, fromDate, toDate, filepath)  
    local.run(thrSMA.thrSMA, barfeed, parameters_generator())
