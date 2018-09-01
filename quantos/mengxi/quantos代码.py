from __future__ import print_function
from __future__ import absolute_import
import time

import numpy as np
import pandas as pd

import jaqs.trade.analyze as ana
from jaqs.data import RemoteDataService
from jaqs.data import DataView
from jaqs.trade import model
from jaqs.trade import AlphaBacktestInstance
from jaqs.trade import AlphaTradeApi
from jaqs.trade import PortfolioManager
from jaqs.trade import AlphaStrategy
import jaqs.util as jutil  #不能删掉
from jaqs.data.dataapi import DataApi

data_config = {
  "remote.data.address": "tcp://data.quantos.org:8910",
  "remote.data.username": "15566028568",    #phone是注册时使用的手机号
  "remote.data.password": "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MzU1OTg2MTI0NzYiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU1NjYwMjg1NjgifQ.ToTAnVWpKtweGj4yoXhVW0pzHds7a9qQzXC8qLBui2g"     #token是api令牌
}
trade_config = {
  "remote.trade.address": "tcp://gw.quantos.org:8901",
  "remote.trade.username": "15566028568",
  "remote.trade.password": "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MzU1OTg2MTI0NzYiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU1NjYwMjg1NjgifQ.ToTAnVWpKtweGj4yoXhVW0pzHds7a9qQzXC8qLBui2g"
}

dataview_dir_path = '***' #dataview存储路径
backtest_result_dir_path = '***' #回测结果存储路径

api = DataApi(addr='tcp://data.quantos.org:8910')
api.login("phone", "token")


dv = DataView()
dv.load_dataview(folder_path=dataview_dir_path)
dv.add_field('turnover_ratio', ds)
dv.save_dataview(folder_path=dataview_dir_path)
dv.update_snapshot()

#在已经保存dataview之后，需要添加某项指标(dataview.py里面可以找这些指标，不是因子！)，如turnover_ratio，使用这段代码，添加完之后下一次运行就可以注释掉


def my_selector(context, user_options=None):
    #筛选僵尸股和ST股
    df = context.dataview.data_inst['name']
    result = pd.DataFrame(df, columns=['ST'], index=df.index, dtype='bool')
    selector_volume = context.snapshot['mean_turnover'] > 50000000 #这里要先add('ts_mean(turnover, 5)', 'mean_turnover')
    names = list(df)
    for i in range(len(df)):
        if 'ST' in names[i]:
            result['ST'][i] = False
        else: result['ST'][i] = True
    result = result.join(selector_volume)
    result = result.dropna(how='any')
    return result

def alpha(context, user_options=None):
    #选择因子值最大的10支股票
    a = context.snapshot['alpha3'] #在使用新因子时，alpha3应改为新因子的名称
    print(len(a))
    s = np.sort(a.dropna(how='any').values)
    if len(s) > 0:
        critical = s[-11] if len(s) > 11 else np.min(s)     #选择因子值最大的10个因子，如要选因子值最小的n个因子，作两个改动：critical = s[n+1], mask=a<critical
        mask = a > critical
        a[mask] = 1.0
        a[~mask] = 0.0
    return a

def test_save_dataview():
    ds = RemoteDataService()
    ds.init_from_config(data_config)
    dv = DataView()
    
    #dataview参数选择
    props = {'start_date': 20080527, 'end_date': 20180807, 'universe': '000002.SH,399107.SZ',"benchmark": "000905.SH,000905.SH",
             'fields': ('open,close,volume,vwap,high,low,turnover'),
             'freq': 1}

    dv.init_from_config(props, ds)
    dv.prepare_data()
    #因子
    factor_formula = 'rank(volume)*(ts_sum(close, 5)/5)*(vwap-close)/(high-low)'
    dv.add_formula('alpha', factor_formula, is_quarterly=False,formula_func_name_style='lower')
    dv.save_dataview(folder_path=dataview_dir_path)

def add(formula, name):
    dv = DataView()
    dv.load_dataview(folder_path=dataview_dir_path)
    dv.add_formula(name, formula, is_quarterly=False,formula_func_name_style='lower')
    dv.save_dataview(folder_path=dataview_dir_path)

def test_alpha_strategy_dataview():
    dv = DataView()
    dv.load_dataview(folder_path=dataview_dir_path)
    #回测参数选择
    props = {
        "benchmark": "000905.SH",
        "universe": ','.join(dv.symbol),

        "start_date": 20170605,
        "end_date": 20180807,

        "period": "day",
        "days_delay": 0,

        "init_balance": 1e9,
        "position_ratio": 1.0,
        "commission_rate": 0.0015,  #手续费
        "n_periods": 2
    }
    props.update(data_config)
    props.update(trade_config)

    trade_api = AlphaTradeApi()

    
    signal_model = model.FactorSignalModel()
    #添加信号
    signal_model.add_signal('alpha3', alpha)  #在使用新因子时，alpha3应改为新因子的名称
    stock_selector = model.StockSelector()
    stock_selector.add_filter(name='myselector', func=my_selector)

    strategy = AlphaStrategy(stock_selector=stock_selector, signal_model=signal_model, pc_method='factor_value_weight')
    pm = PortfolioManager()

    bt = AlphaBacktestInstance()
    
    context = model.Context(dataview=dv, instance=bt, strategy=strategy, trade_api=trade_api, pm=pm)
    
    for mdl in [signal_model, stock_selector]:
        mdl.register_context(context)

    bt.init_from_config(props)

    bt.run_alpha()

    bt.save_results(folder_path=backtest_result_dir_path)
    

def test_backtest_analyze():
    ta = ana.AlphaAnalyzer()
    dv = DataView()
    dv.load_dataview(folder_path=dataview_dir_path)

    ta.initialize(dataview=dv, file_folder=backtest_result_dir_path)

    ta.do_analyze(result_dir=backtest_result_dir_path, selected_sec=list(ta.universe))   #selected_sec=[]时，可以不打印每支股票的交易记录，加快回测分析的速度


if __name__ == "__main__":
    t_start = time.time()

    #test_save_dataview()   #如果没有保存dataview，不能省略这一句；如果已经保存dataview，可以省略这一句，在保存的dataview上进行操作
	
	
    #add('decay_linear(rank(volume)*(ts_sum(close,5)/5)*(vwap-close)/(high-low),5)', 'alpha3') #在原有的dataview上添加新的因子，不用重新下载数据，新因子的名字最好不要与已有因子名字重合
    add('ts_mean(turnover, 5)', 'mean_turnover') #加完一次就可以注释掉这句话
    test_alpha_strategy_dataview()
    test_backtest_analyze()

    t3 = time.time() - t_start
    print("\n\n\nTime lapsed in total: {:.1f}".format(t3))