#coding=utf-8
import pandas as pd
import os
def run(name,start,end,benchmark,stock,plot):
    if plot:
        os.system('''rqalpha run -f {0} -d d:/bundle -s {1} -e {2} --account stock {3}  \
        --benchmark {4}  --plot -o {5}.pkl'''.format(name,start,end,stock,benchmark,name.split('.')[0]+start))
    if not plot:
        os.system('''rqalpha run -f {0} -d d:/bundle -s {1} -e {2} --account stock {3}  \
        --benchmark {4}  -o {5}.pkl'''.format(name,start,end,stock,benchmark,name.split('.')[0]+start))

if __name__=='__main__':
    name='buy_and_hold.py'
    start=['2015-1-10']#,'2012-10-10','2014-10-10','2016-10-10']
    end='2018-1-1'
    benchmark='000300.XSHG'
    stock=100000
    for i in start:
        run(name,i,end,benchmark,stock,1)
    '''
    result={}
    for i in start:
        result_dict = pd.read_pickle(name.split('.')[0]+i+'.pkl')
        ## [out]dict_keys(['total_portfolios', 'summary', 'benchmark_portfolios', 'benchmark_positions', 'stock_positions', 'trades', 'stock_portfolios'])
        result[i]=result_dict['summary']
    result=pd.DataFrame.from_dict(result,'index')
    result.to_excel(name.replace('.py','.xlsx'))'''