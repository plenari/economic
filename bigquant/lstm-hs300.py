# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 09:33:09 2018

@author: omf
"""


def load_data(instrument,start_date,end_date,field,seq_len,prediction_len,train_proportion,normalise=True):
    '''
    # 加载数据，数据变化，提取数据模块
    
    '''    
    fields=[field,'amount']
    data=D.history_data(instrument,start_date,end_date,fields)
    data=data[data.amount>0]
    datetime=list(data['date'])
    data=list(data[field])
    seq_len=seq_len+1  
    result=[]
    for index in range(len(data)-seq_len):
        result.append(data[index:index+seq_len])
        
    if normalise:
        norm_result=normalise_windows(result)
    else:
        norm_result=result
        
    result=np.array(result)
    norm_result=np.array(norm_result)
    
    row=round(train_proportion*norm_result.shape[0])
    
    data_test=result[int(row):,:]
    datetime=datetime[int(row):]

    test_datetime=[]
    for index in range(len(datetime)):
        if index % prediction_len==0 and index+seq_len<len(datetime)-prediction_len:
            test_datetime.append(datetime[index+seq_len])
    
    train=norm_result[:int(row),:]
    np.random.shuffle(train)   #随机打乱训练样本
    x_train = train[:, :-1]
    y_train = train[:, -1]
    x_test = norm_result[int(row):, :-1]
    y_test = norm_result[int(row):, -1]
    
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))  

    return [x_train, y_train, x_test, y_test, data_test, test_datetime]