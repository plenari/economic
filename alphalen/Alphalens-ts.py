# coding: utf-8

# ## 因子分析part1
'''
performance :性能分析
plotting: 画图
tears: 汇总
utils :工具包
第一步，用处理好的数据，把数据标准化
alphalens.utils.get_clean_factor_and_forward_returns()
返回值是pd.pd.DataFrame - MultiIndex，包含每个调仓周期的收益率，因子值，所属group（这里是行业），以及分层的次序
第二步：
alphalens.tears.create_returns_tear_sheet(factor_data)
第三步：
information anslysis适用于分析评价在不考虑交易成本下，一个factor的预测能力的一种方法。主要的方法就是通过因子的IC来分析。
alphalens.tears.create_information_tear_sheet(factor_data)
第四步：
衡量一个因子的好坏还有一个指标，就是稳定性。因子的稳定性直接决定了你的调仓频率。
alphalens.tears.create_turnover_tear_sheet(factor_data)

'''
import pandas as pd
import numpy as np
from scipy.stats import mstats
from scipy import stats
from datetime import datetime
from alphalens import utils
from alphalens import plotting
from alphalens import tears
from alphalens import performance
import matplotlib as mpl
import matplotlib.pyplot as plt
import tushare as ts

# 选择日期
# 获得某段时间内hs300的pe因子数据,将其拼接成有multiindex的dataframe，再转成Series
#按照概念分类的股票。
#code   name c_name
#0     600050   中国联通   5G概念
stocks_sets = ts.get_concept_classified()
random_choice=np.random.choice(stocks_sets.index,size=50)
stocks_sets=stocks_sets.loc[random_choice,:]
stocks_sets.drop_duplicates('code')
stocks_sets.reset_index(drop=True)
df_facs_datas=ts.get_stock_basics()
df_facs_datas=df_facs_datas[(df_facs_datas.pe<60)&(df_facs_datas.pe>20)]
df_facs_datas=df_facs_datas.loc[stocks_sets.code,'pe']
df_facs_datas=df_facs_datas.dropna()
# 除去异常值和标准化
def winsorize_series(series):   
    q =series.quantile([0.02,0.98])
    if isinstance(q,pd.Series) and len(q) == 2:
        series[series<q.iloc[0]] = q.iloc[0]
        series[series>q.iloc[1]] = q.iloc[1]
    return series
def standardize_series(series):
    std = series.std()
    mean = series.mean()
    #新的数据的平均值为0，
    return (series-mean)/std

df_facs_datas=winsorize_series(df_facs_datas)
df_facs_datas=standardize_series(df_facs_datas)

##进行不下去了。
df_facs_datas.columns=df_facs_datas.columns.astype('datetime64[ns]')
df_facs_unstack=df_facs_datas.unstack()
df_facs_unstack.index.names= ['data','code']
df_facs_unstack.name='pe'
series_facs_datas=df_facs_unstack

price = get_price(stocks_sets, start_date='2017-05-01',end_date = '2017-08-01').close

# 获取收盘价数据：
price.index.name = 'date'
price.columns.name = 'code'
# 看一下价格数据的前几行
price.head()

# 获取市值数据,按照上面的方式进行拼接..
df_facs_datas_mc = pd.DataFrame()
q = query(fundamentals.eod_derivative_indicator.market_cap).filter(fundamentals.eod_derivative_indicator.stockcode.in_(stocks_sets))
for i in range(len(trading_dates)):
    daily_fac_mc_data = get_fundamentals(q,trading_dates[i])[0,0,:]

    df_daily_fac_mc_data = pd.DataFrame(daily_fac_mc_data)
    df_daily_fac_mc_data.columns = ['market_value']

    df_daily_fac_mc_data['date'] = trading_dates[i]
    df_facs_datas_mc = pd.concat([df_facs_datas_mc,df_daily_fac_mc_data])

df_facs_datas_mc = df_facs_datas_mc.set_index(['date',df_facs_datas_mc.index])
df_facs_datas_mc.index.names= ['date','code']
series_facs_datas_mc = df_facs_datas_mc['market_value']
series_facs_datas_mc.tail()

port = [1,2,3,4,5]
# 分位数处理，进行分组
def division(series):
    q = series.quantile([0.2,0.4,0.6,0.8])
    if isinstance(q,pd.Series) and len(q) == 4:
        series[series<q.iloc[0]] = port[0]
        series[(series>=q.iloc[0]) & (series<q.iloc[1])] = port[1]
        series[(series>=q.iloc[1]) & (series<q.iloc[2])] = port[2]
        series[(series>=q.iloc[2]) & (series<q.iloc[3])] = port[3]
        series[(series>=q.iloc[3])] = port[4]
    return series

# 将市值因子的数据每天都进行分组
mc_group = series_facs_datas_mc.groupby(level='date').apply(division)
# 标签
mc_label = {1:'very_small_MC',2:'small_MC',3:'mid_MC',4:'big_MC',5:'very_big_MC'}
mc_group.tail()

# #### 下面就进行分析了,一共有
# ##### Quantiles Statistics，Returns Analysis，Information Analysis，Turnover Analysis

# #### 整理数据成规定的格式：

get_ipython().magic('pinfo utils.get_clean_factor_and_forward_returns')

# 大致意思就是将上面得到的数据有:'因子数据','价格','市值数据','市值分组的标签'等数据（要符合规格）代入get_clean_factor_and_forward_returns这个函数就可以得到 一个多重索引的dataframe，包含了alpha（在factor那列），每个时期的预期收益(1,5,10)，因子分组的组号（factor_quantile），可能还会有按另一个因子（此处是市值）的分组（group）
facs_data_analysis  = utils.get_clean_factor_and_forward_returns(series_facs_datas,price,groupby=mc_group,groupby_labels=mc_label)

# 由于factor那列是object类型，转换成float方便下面继续分析
facs_data_analysis['factor'] = np.float128(facs_data_analysis['factor'])

# 1、 查看一下summary
get_ipython().magic('pinfo tears.create_summary_tear_sheet')

# 返回的是一个简易的summary包含（Quantiles Statistics，Returns Analysis，Information Analysis，Turnover Analysis）

tears.create_summary_tear_sheet(facs_data_analysis)

# 2、 Returns Analysis
get_ipython().magic('pinfo tears.create_returns_tear_sheet')

# 收益率分析：
# 分析每个预期收益在每组的情况、以及每个forward Period每组的累积收益；
# 
# factor_data:里面放上面通过utils.get_clean_factor_and_forward_returns的dataframe
# 
# by_group:如果是True，会每个组都展示图标
# 
# 可以对于pe看出第一组应该是好于第五组的
# 在每个Forward Period的高组减去低组的平均收益
# 每种市值的收益率分析

tears.create_returns_tear_sheet(facs_data_analysis,by_group=True)


# ### 3、 Turnover Analysis

get_ipython().magic('pinfo tears.create_turnover_tear_sheet')



#换手率分析
#每个forward period的每组的平均换手率以及等级相关系数（秩相关）;

factor_data:里面放上面通过utils.get_clean_factor_and_forward_returns的dataframe

tears.create_turnover_tear_sheet(facs_data_analysis)


# ### 4、 Information Analysis

get_ipython().magic('pinfo performance.factor_information_coefficient')

# #### 1、计算因子值和预期收益之间的基于Spearman Rank Correlation（斯皮尔曼等级相关系数）的IC：
# Computes the Spearman Rank Correlation based Information Coefficient (IC)
# between factor values and N period forward returns for each period in
# the factor index;
# 
# factor_data:里面放上面通过utils.get_clean_factor_and_forward_returns的dataframe
# 
# by_group:如果是True，会每个组都会计算IC;
# 
# group_adjust:在计算IC之前是否对预期收益进行处理
# 
# 返回：Spearman Rank correlation between factor and provided forward returns.

IC = performance.factor_information_coefficient(facs_data_analysis,group_adjust=False,by_group=True)
IC.head()


# #### 2、Get the mean information coefficient of specified groups.
# #### 获得某段时期或某种分组的平均IC
get_ipython().magic('pinfo performance.mean_information_coefficient')

# factor_data:里面放上面通过utils.get_clean_factor_and_forward_returns的dataframe
# 
# by_group:如果是True，计算每组的平均IC
# 
# group_adjust:在计算IC之前是否对预期收益进行处理
# 
# by_time:(按哪种时间规则计算，1q=1季度，1w=1周)

performance.mean_information_coefficient(facs_data_analysis,
                                 group_adjust=False,
                                 by_group=True,
                                 by_time='1q')


# ### 5、 其他

get_ipython().magic('pinfo performance.factor_alpha_beta')

# #### 计算alpha和beta
# 根据因子和预期收益计算alpha，beta等；
# factor_data:里面放上面通过utils.get_clean_factor_and_forward_returns的dataframe；
# 
#     Compute the alpha (excess returns), alpha t-stat (alpha significance),
#     and beta (market exposure) of a factor. A regression is run with
#     the period wise factor universe mean return as the independent variable
#     and mean period wise return from a portfolio weighted by factor values
#     as the dependent variable.

performance.factor_alpha_beta(facs_data_analysis)


get_ipython().magic('pinfo tears.create_event_returns_tear_sheet')

tears.create_event_returns_tear_sheet(facs_data_analysis,prices=price,avgretplot=(5, 15),
                                    long_short=True,
                                    by_group=True)

