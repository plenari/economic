#coding:utf-8
from QA_trade_stock import QA_Trade_stock_util,QA_Trade_stock_api
import pymongo
import csv,time,datetime

st = QA_Trade_stock_api.QA_Stock()
st.get_config()
print(st.sTradeAccountNo)
client = st.QA_trade_stock_login()

print('可用资金查询')
print(st.QA_trade_stock_get_cash(client))
print('当前持仓股票查询')
print(st.QA_trade_stock_get_stock(client))
print('委托查询')
print(st.QA_trade_stock_get_orders(client))
holder=st.QA_trade_stock_get_holder(client)
account=QA_Trade_stock_util.QA_get_account_assest(st,client)
print(holder)
hold_list=[l['code'] for l in account['stock']]
# 打开股票列表
stock_lists=['000001']



# 买入
for item in stock_lists:

   if str(item)[0]=='6':
        print(holder[0])
        print(item)
        st.QA_trade_stock_post_order(client,[0, 4, holder[0],item, 0, 100])
   else:
        print(holder[1])
        print(item)
        st.QA_trade_stock_post_order(client,[0, 4, holder[1],item, 0, 100])
# 获取当前持仓股票

account=QA_Trade_stock_util.QA_get_account_assest(st,client)
hold_list=[l['code'] for l in account['stock'] if float(l['sell_available'])>0]
#print(hold_list)

#卖出
for item in hold_list:
    
    if str(item)[0]=='6':
        st.QA_trade_stock_post_order(client,[1, 4, st.sTradeAccountNo,item, 0, 100])
    else:
        st.QA_trade_stock_post_order(client,[1, 4, st.sTradeAccountNo,item, 0, 100])


#import QA_query    