import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LassoCV
from sklearn.cluster import KMeans

def init(context):
    context.trader_dates=get_trading_dates('2011-01-01','2017-09-08')
    
def before_trading(context):
    current_date=pd.to_datetime(context.now) #当前时间
    previous_date=pd.to_datetime(get_previous_trading_date(context.now)) #上一个交易日时间
    if current_date.month==previous_date.month: #如果同一个月,则不进行选股操作
        return
    
    #********************以下获取一个月前的财务因子********************#
    EDI=fundamentals.eod_derivative_indicator  #股票估值指标
    d1=get_fundamentals(query(EDI.pe_ratio),context.now,'2m')
    train1=pd.Series(d1[0,1,:],name='pe_ratio')
    test1=pd.Series(d1[0,0,:],name='pe_ratio')
    d2=get_fundamentals(query(EDI.pcf_ratio),context.now,'2m')
    train2=pd.Series(d2[0,1,:],name='pcf_ratio')
    test2=pd.Series(d2[0,0,:],name='pcf_ratio')
    d3=get_fundamentals(query(EDI.pb_ratio),context.now,'2m')
    train3=pd.Series(d3[0,1,:],name='pb_ratio')
    test3=pd.Series(d3[0,0,:],name='pb_ratio')
    d4=get_fundamentals(query(EDI.market_cap),context.now,'2m')
    train4=pd.Series(d4[0,1,:],name='market_cap')
    test4=pd.Series(d4[0,0,:],name='market_cap')
    
    IS=fundamentals.income_statement #利润表指标
    d5=get_fundamentals(query(IS.revenue),context.now,'2m')
    train5=pd.Series(d5[0,1,:],name='revenue')
    test5=pd.Series(d5[0,0,:],name='revenue')
    d6=get_fundamentals(query(IS.basic_earnings_per_share),context.now,'2m')
    train6=pd.Series(d6[0,1,:],name='basic_earnings_per_share')
    test6=pd.Series(d6[0,0,:],name='basic_earnings_per_share')
    d7=get_fundamentals(query(IS.total_expense),context.now,'2m')
    train7=pd.Series(d7[0,1,:],name='total_expense')
    test7=pd.Series(d7[0,0,:],name='total_expense')

    FI=fundamentals.financial_indicator #财务指标
    d8=get_fundamentals(query(FI.earnings_per_share),context.now,'2m')
    train8=pd.Series(d8[0,1,:],name='earnings_per_share')
    test8=pd.Series(d8[0,0,:],name='earnings_per_share')
    d9=get_fundamentals(query(FI.free_cash_flow_company_per_share),context.now,'2m')
    train9=pd.Series(d9[0,1,:],name='free_cash_flow_company_per_share')
    test9=pd.Series(d9[0,0,:],name='free_cash_flow_company_per_share')
    #****************财务因子获取完毕****************************#
    
    #****************再构造两个量价因子******************************#
    #相应的交易日期
    last_month_end=previous_date #上个月底
    last_month_start=previous_date-datetime.timedelta(previous_date.days_in_month-1) #上个月初
    last_month2_end=previous_date-datetime.timedelta(previous_date.days_in_month) #上上个月底
    last_month2_start=last_month2_end-datetime.timedelta(last_month2_end.days_in_month-1) #上上个月初
    
    Stock=all_instruments(type='CS').order_book_id.values #获取当前的股票
    Index=get_price('000001.XSHG',start_date=last_month2_start,frequency='1d', fields='close', adjust_type='pre')
    
    Close=get_price(Stock,start_date=last_month2_start,frequency='1d', fields='close', adjust_type='pre') #当前股票两个月的收盘价
    Volume=get_price(Stock,start_date=last_month2_start,frequency='1d', fields='volume', adjust_type='pre') #当前股票两个月的成交量
    #求相关系数。
    train10=Close[:last_month2_end].rank().corrwith(Volume[:last_month2_end].rank())
    #这个地方的平方有什么问题？
    test10=Close[last_month_start:].rank().corrwith(Volume[last_month_start:].rank())
    train10.name=test10.name='VPcor'#重命名
    train11=Close[:last_month2_end].pct_change().corrwith(Index[:last_month2_end].pct_change())#
    test11=Close[last_month_start:].pct_change().corrwith(Index[last_month_start:].pct_change())
    train11.name=test11.name='rsquare'
    #****************量价因子计算完毕******************************#
    
    
    #合并数据集
    data=pd.concat([train1,train2,train3,train4,train5,train6,train7,train8,train9,train10,train11],axis=1) #合并数据集
    test=pd.concat([test1,test2,test3,test4,test5,test6,test7,test8,test9,test10,test11],axis=1)
    
    #计算训练集的y,即下一个月的收益率
    Price=get_price(Stock,start_date=last_month2_end,frequency='1d', fields='close', adjust_type='pre')
    Returns=pd.Series(np.log(Price.iloc[-1]/Price.iloc[0]),name='Returns')
    Returns=data.join(Returns)['Returns'].fillna(0) 
    #已经获得各个股票的
    
    #根据训练时间段的市值,波动率进行聚类
    Clusterdata1=pd.Series(Close[last_month2_start:last_month2_end].pct_change().std(),name='volatility')
    Clusterdata2=train4
    Clusterdata=pd.concat([Clusterdata1,Clusterdata2],axis=1)
    Clusterdata=((Clusterdata-Clusterdata.mean())/Clusterdata.std()).fillna(0) #中心标准化
    np.random.seed(0)
    clf=KMeans(n_clusters=5) #定义聚类的个数为5
    clf.fit(Clusterdata)
    label=pd.Series(clf.labels_,index=data.index,name='label') #聚类的标签
    
    preReturn=groupLasso(data,Returns,label,test)  #根据不同的类分类做lasso回归
    score=preReturn.rank()
    Q=score.quantile(0.9)
    context.condition=(score>Q).to_dict() 

#*******************************************************************************************#

def handle_bar(context, bar_dict):                                       
    Stock=all_instruments(type='CS').order_book_id.values #获取当前的股票
    #5天下跌10%，做清仓止损        
    for s in Stock:
        p=history_bars(s,5, '1d', 'close')
        if len(p)<5:
            continue
        if p[-1]/p[-5]-1<-0.1 and context.portfolio.positions[s].quantity>0:
            order_target_percent(s, 0)
    
    #每个月选一次股
    current_date=pd.to_datetime(context.now) #当前时间
    previous_date=pd.to_datetime(get_previous_trading_date(context.now)) #上一个交易日时间
    if current_date.month==previous_date.month: #如果同一个月,则不进行选股操作
        return
    
    chosed=[]  #取出满足条件的股票
    for s in context.condition.keys():
        if context.condition[s] and bar_dict[s].is_trading and instruments(s).status=='Active':
            chosed.append(s)
    N=len(chosed)
    for s in Stock: #在当前全市场股票中，满足条件的等权持仓
        if s in chosed:
            order_target_percent(s,1./N)
        elif context.portfolio.positions[s].quantity>0:
            order_target_percent(s,0)
        
        
def groupLasso(X,Y,labels,Test):
    '''
    该函数可根据聚类结果labels将股票分成不同的组,在不同的组中,分别做lasso模型，再分别对测试集进行预测
    '''
    preReturn=pd.Series(np.nan,index=Test.index,name='preReturn')
    for label in np.unique(labels):#一共5个标签。遍历每一个标签
        x,y,test=X.loc[labels.index[labels==label]],Y.loc[labels.index[labels==label]],Test.loc[labels.index[labels==label]] #根据label截取子集
        if len(y)<10:#如果小于10个就 进行下个循环
            continue
        combine=pd.concat([x,Test]) #训练数据和测试数据合并
        combine=combine.iloc[:,(combine.isnull().sum()/len(combine)<0.9).values]#剔除缺失数据高于90%的特征
        tmp=(combine.rank()-combine.rank().mean()).fillna(0)
        combine=tmp/tmp.std() #排序后中心标准化
        x,test=combine.iloc[:len(x),:],combine.iloc[-len(test):,:] #再拆回训练集与测试集
        clf=LassoCV(alphas=np.logspace(-3,2,100))
        clf.fit(x,y) #拟合lasso回归模型
        preReturn[test.index]=clf.predict(test) #对测试集做预测
    return preReturn

