import time
import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot
import statsmodels.api as sm
from scipy.stats import ttest_ind

def init(context):
    df = all_instruments(type='CS')
    SZ = df[(df['exchange'] == 'XSHG')&(df['sector_code'] == 'InformationTechnology')]
    all_order_id = SZ.iloc[:,8]
    k=all_order_id
    k=k.tolist()
    start_date='2009-01-01'
    end_date='2009-12-31'
    u = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    f = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    days=get_trading_dates( start_date='2016-01-01', end_date='2016-12-31')
    for j in range(0,4):
        #s一个
        price=history_bars(k, daysfrequency='1d', fields='close',skip_suspended =False)
        normalprice=np.log(price/price[0])
        normalprice=normalprice.dropna(axis=1,how='any')
        days=range(10,231)
        for n in days:
            recorditem=[]
            recordname=[]
            for i in normalprice.columns.tolist():
                y = normalprice[i].head(n).values
                x = np.array(range(len(normalprice.head(n).index)))
                X = sm.add_constant(x)
                model = sm.OLS(y,X)
                results = model.fit()
                criteria=results.params[1]
                recorditem.append(criteria)
                name=i
                recordname.append(name)
            if n == days[0]:
                nam=['slope'+str(n)]
                df2=pd.DataFrame(recorditem,index=recordname,columns=nam)
            if n != days[0]:
                nam=['slope'+str(n)]
                df3=pd.DataFrame(recorditem,index=recordname,columns=nam)
                df2=df2.join(df3)
          if j==0:
             df5=df2
          if j!=0:
            frames=[df5,df2]
            df5=pd.concat(frames)
        
    resname=df5.index
    context.df5=df5
    df = all_instruments(type='CS')
    SZ = df[(df['exchange'] == 'XSHG')&(df['sector_code'] == 'InformationTechnology')]
    all_order_id = SZ.iloc[:,8]
    k=all_order_id
    k=k.tolist()
    price=get_price(k, start_date='2010-01-01', end_date='2010-06-01', frequency='1d', fields='close', adjust_type='none', skip_suspended =False)
    normalprice=np.log(price/price.ix[0])
    normalprice=normalprice.dropna(axis=1,how='any')
    days=range(10,len(normalprice.index))
    for n in days:
      recorditem=[]
      recordname=[]
      for i in normalprice.columns.tolist():
        y = normalprice[i].head(n).values
        x = np.array(range(len(normalprice.head(n).index)))
        X = sm.add_constant(x)
        model = sm.OLS(y,X)
        results = model.fit()
        criteria=results.params[1]
        recorditem.append(criteria)
        name=i
        recordname.append(name)
      if n == days[0]:
        nam=['slope'+str(n)]
        df2=pd.DataFrame(recorditem,index=recordname,columns=nam)
      if n != days[0]:
        nam=['slope'+str(n)]
        df3=pd.DataFrame(recorditem,index=recordname,columns=nam)
        df2=df2.join(df3)
    df4=df2
    context.df4=df4
    basket=[]
    reference2=[]
    for m in range(len(df4.index)): 
      A=df4.ix[m]
      record=[]
      match=[]
      idx=[]
      df5.index=range(len(df5.index))
      for i in range(len(df5.index)):
        B=df5.ix[i].head(len(df4.columns))
        p=ttest_ind(A,B)[1]
        record.append(p)
        idx.append(resname[i])
        match.append(df5.index[i])
      nam=['P-value']
      nam1=['stocks']
      pv=pd.DataFrame(record,index=match,columns=nam)
      pn=pd.DataFrame(idx,index=match,columns=nam1)
      pv=pv.join(pn)
      ref=np.mean(df5.ix[pv[pv['P-value']==np.max(pv['P-value'])].index.tolist()[0]])
      ref1=np.mean(A)
      ref2=df5.ix[pv[pv['P-value']==np.max(pv['P-value'])].index.tolist()[0]][-1]
      ref3=A[-1]
      if ref3<ref2:
        basket.append(df4.index[m])
        reference2.append(ref2)
    context.s1=basket
    context.ref2=reference2
    logger.info("RunInfo: {}".format(context.run_info))
    logger.info(context.s1)
    logger.info(context.ref2)
    scheduler.run_daily(handle_bar, time_rule=market_open(minute=10))

# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    planB=[]
    u = context.now
    if  (u.month)==(6) or (u.month)==(7) or (u.month)==(8) or (u.month)==(9) or (u.month)==(10) or (u.month)==(11):
        price=get_price(context.s1, start_date=datetime.datetime(year=u.year, month = 1, day = 1).strftime('%Y-%m-%d'), end_date=None, frequency='1d', fields='close', adjust_type='pre', skip_suspended=False)
        normalprice=np.log(price/price.ix[0])
        for i in range(len(normalprice.columns)):
            y = normalprice.iloc[:,i].values
            x = np.array(range(len(normalprice.index)))
            X = sm.add_constant(x)
            model = sm.OLS(y,X)
            results = model.fit()
            criteria=results.params[1]
            if criteria > context.ref2[i]:
                planB.append(normalprice.columns.tolist()[i])
        context.B=planB
        logger.info(context.B)
# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    u = context.now
    stock1 = context.s1
    num = len(stock1)
    stock2= context.B
    if  (u.month)==(6) or (u.month)==(7) or (u.month)==(8) or (u.month)==(9) or (u.month)==(10):
        for i in stock1:
            curPosition = context.portfolio.positions[i].quantity
            if curPosition == 0 and i not in stock2:
                order_target_percent(i, 1/num)
            if i in stock2:
                order_target_percent(i, 0)
    if  (u.day, u.month)==(15,11) or (u.day, u.month)==(16,11) or (u.day, u.month)==(17,11) or (u.month)==(12):
        for i in stock1:
            curPosition = context.portfolio.positions[i].quantity
            if curPosition > 0:
                order_target_percent(i, 0)
    
# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    u = context.now
    if  (u.day, u.month)==(31,5):
        df = all_instruments(type='CS')
        SZ = df[(df['exchange'] == 'XSHG')&(df['sector_code'] == 'InformationTechnology')]
        all_order_id = SZ.iloc[:,8]
        k=all_order_id
        k=k.tolist()
        start_date=datetime.datetime(year=u.year-1, month = 1, day = 1).strftime('%Y-%m-%d')
        end_date=datetime.datetime(year=u.year-1, month = 12, day = 31).strftime('%Y-%m-%d')
        u = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        f = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        for j in range(0,4):
          price=get_price(k, start_date=datetime.datetime(year=u.year - j, month = u.month, day = u.day).strftime('%Y-%m-%d'), end_date=datetime.datetime(year=f.year - j, month = f.month, day = f.day).strftime('%Y-%m-%d'), frequency='1d', fields='close', adjust_type='none', skip_suspended =False)
          normalprice=np.log(price/price.ix[0])
          normalprice=normalprice.dropna(axis=1,how='any')
          days=range(10,231)
          for n in days:
            recorditem=[]
            recordname=[]
            for i in normalprice.columns.tolist():
              y = normalprice[i].head(n).values
              x = np.array(range(len(normalprice.head(n).index)))
              X = sm.add_constant(x)
              model = sm.OLS(y,X)
              results = model.fit()
              criteria=results.params[1]
              recorditem.append(criteria)
              name=i
              recordname.append(name)
            if n == days[0]:
              nam=['slope'+str(n)]
              df2=pd.DataFrame(recorditem,index=recordname,columns=nam)
            if n != days[0]:
              nam=['slope'+str(n)]
              df3=pd.DataFrame(recorditem,index=recordname,columns=nam)
              df2=df2.join(df3)
          if j==0:
             df5=df2
          if j!=0:
            frames=[df5,df2]
            df5=pd.concat(frames)
        resname=df5.index
        context.df5=df5
        df = all_instruments(type='CS')
        SZ = df[(df['exchange'] == 'XSHG')&(df['sector_code'] == 'InformationTechnology')]
        all_order_id = SZ.iloc[:,8]
        k=all_order_id
        k=k.tolist()
        price=get_price(k, start_date=datetime.datetime(year=u.year, month = 1, day = 1).strftime('%Y-%m-%d'), end_date=datetime.datetime(year=u.year, month = 5, day = 31).strftime('%Y-%m-%d'), frequency='1d', fields='close', adjust_type='none', skip_suspended =False)
        normalprice=np.log(price/price.ix[0])
        normalprice=normalprice.dropna(axis=1,how='any')
        days=range(10,len(normalprice.index))
        for n in days:
          recorditem=[]
          recordname=[]
          for i in normalprice.columns.tolist():
            y = normalprice[i].head(n).values
            x = np.array(range(len(normalprice.head(n).index)))
            X = sm.add_constant(x)
            model = sm.OLS(y,X)
            results = model.fit()
            criteria=results.params[1]
            recorditem.append(criteria)
            name=i
            recordname.append(name)
          if n == days[0]:
            nam=['slope'+str(n)]
            df2=pd.DataFrame(recorditem,index=recordname,columns=nam)
          if n != days[0]:
            nam=['slope'+str(n)]
            df3=pd.DataFrame(recorditem,index=recordname,columns=nam)
            df2=df2.join(df3)
        df4=df2
        context.df4=df4
        basket=[]
        reference2=[]
        for m in range(len(df4.index)): 
          A=df4.ix[m]
          record=[]
          match=[]
          idx=[]
          df5.index=range(len(df5.index))
          for i in range(len(df5.index)):
            B=df5.ix[i].head(len(df4.columns))
            p=ttest_ind(A,B)[1]
            record.append(p)
            idx.append(resname[i])
            match.append(df5.index[i])
          nam=['P-value']
          nam1=['stocks']
          pv=pd.DataFrame(record,index=match,columns=nam)
          pn=pd.DataFrame(idx,index=match,columns=nam1)
          pv=pv.join(pn)
          ref=np.mean(df5.ix[pv[pv['P-value']==np.max(pv['P-value'])].index.tolist()[0]])
          ref1=np.mean(A)
          ref2=df5.ix[pv[pv['P-value']==np.max(pv['P-value'])].index.tolist()[0]][-1]
          ref3=A[-1]
          if ref3<ref2:
            basket.append(df4.index[m])
            reference2.append(ref2)
        context.s1=basket
        context.ref2=reference2
        logger.info(context.s1)
        logger.info(context.ref2)
        
        
    