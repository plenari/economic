# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 14:04:31 2018
@author: omf
---------------
lstm模型 训练，预测
从其他地方引入数据data
"""
from conf import conf
import pandas as pd
import numpy as np
from keras.layers import Input, Dense, LSTM, concatenate
from keras.models import Model
from keras.models import Sequential
from keras import optimizers
from sklearn import metrics
import tensorflow as tf


def activation_atan(x):    
    return tf.atan(x)
def softmax(x):
    '''    '''
    return tf.nn.softmax(x)

def lstm_train_regression(df, batch_size,epoch,time_step,input_dim):

    '''
    
    >>> lstm_train(df,conf)
    
    model
    '''
    # 构建神经网络层 2层LSTM层+2层Dense层
    lstm_input = Input(shape=(time_step, input_dim), name='lstm_input')
    lstm_output = LSTM(128, activation='relu', dropout_W=0.2, dropout_U=0.1,return_sequences=True)(lstm_input)
    lstm_output = LSTM(64, activation='relu', dropout_W=0.2, dropout_U=0.1,return_sequences=False)(lstm_output)
    dense_output_1 = Dense(16, activation='relu')(lstm_output)
    predictions = Dense(1,activation='linear')(dense_output_1)

    model = Model(input=lstm_input, output=predictions)
    #rms=optimizers.RMSprop(lr=0.005, rho=0.9, epsilon=1e-06)
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='mse', metrics=['mse'])
    
    model.fit(
        np.array(df['X'].values.tolist()),np.array(df['y'].values.tolist()),
        batch_size=batch_size, epochs=epoch,  verbose=2,validation_split=0.1
    )   
    return model


def lstm_train_class(trainx,trainy, batch_size,epoch,time_step,input_dim,classification,validation_data=None):

    '''
    分类问题    
    >>> lstm_train_class(df,conf)
    
    model
    '''
    # 构建神经网络层 2层LSTM层+2层Dense层
    lstm_input = Input(shape=(time_step, input_dim), name='lstm_input')
    lstm_output = LSTM(128, activation='relu', dropout_W=0.2, dropout_U=0.1,return_sequences=True)(lstm_input)
    lstm_output = LSTM(64, activation='relu', dropout_W=0.2, dropout_U=0.1,return_sequences=False)(lstm_output)
    dense_output_1 = Dense(16, activation='relu')(lstm_output)
    predictions = Dense(classification,activation=softmax)(dense_output_1)
    
    model = Model(input=lstm_input, output=predictions)    
    
    #model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy',metrics.roc_auc_score])
    
    
    model.fit(
        trainx,trainy,batch_size=batch_size, epochs=epoch,  verbose=2, validation_data=validation_data
        
    )   
    return model


def lstm_predict(model,df,flag='train'):
    '''
    训练
    '''
    X=np.array(df.X.values.tolist())
    y_pred=model.predict(X)    
    y_true=np.array(df.y.values.tolist())
    
    print("{}'s{} is {}.".format(flag,'f1-score',metrics.f1_score(y_true>0,y_pred>0)))
    print("{}'s{} is {}.".format(flag,'accuracy_score',metrics.accuracy_score(y_true>0,y_pred>0)))
    
    return y_true,y_pred.flatten()

