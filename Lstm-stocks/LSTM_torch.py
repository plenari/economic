# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 15:03:45 2018
@author: Plenari
pytorch
"""

import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as  np
from sklearn import metrics
import torch
from imblearn.under_sampling import RandomUnderSampler
#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#device = torch.device('cpu')   
    
class LSTM(nn.Module):
    '''
    双层，双向LSTM，加两个全连接层。    
    每次开始传播之前需要重置隐藏层，需要传入batch_size参数。
    '''
    def __init__(self,  input_dim, hidden_dim, num_layers, num_classes,batch_size,seq_len):
        super(LSTM, self).__init__()
        
        self.seq_len=seq_len
        self.input_dim=input_dim
        self.hidden_dim=hidden_dim
        self.num_layers=num_layers
        self.num_classes=num_classes
        self.num_directions=2
        self.batch_size=batch_size
        
        self.lstm=nn.LSTM(
                    input_size= input_dim,
                    hidden_size= hidden_dim,
                    num_layers=num_layers,
                    bias=True,
                    dropout= 0.2,
                    batch_first=False,
                    bidirectional=True
                    )

        # 线性层将隐状态空间映射到标注空间
        self.linear1 = nn.Linear(self.seq_len*self.hidden_dim*self.num_directions, 128)
        self.linear2 = nn.Linear(128, self.num_classes)
                
    def init_hidden(self,batch_size):
        # 各个维度的含义是 (num_layers, minibatch_size, hidden_dim)
        return (autograd.Variable(torch.zeros(self.num_layers * self.num_directions, \
                                               batch_size,  self.hidden_dim)),
            
            autograd.Variable(torch.zeros(self.num_layers * self.num_directions, \
                                               batch_size,  self.hidden_dim)))
    def forward(self, X):
        '''    
        
        '''
        #seq_len ,batch_size,input_size,        
        X, self.hidden = self.lstm(X.view(self.seq_len,-1,self.input_dim), self.hidden)      
 
        X=self.linear1(X.view(-1,self.seq_len*self.hidden_dim*self.num_directions))
        X=F.relu(X)        
        X=self.linear2(X)        
        X = F.log_softmax(X, dim=1)
        return X    

def train_epoch(model,loss_function,optimizer,trainx,trainy,testx,testy,batch_size,\
                seq_len,input_dim,num_layers,epochs=15,cuda=0,device=0,sample=1):
    '''
    trainx.shape, batch,seq_len,input_dim    
    sample，下采样
    '''
    for epoch in range(epochs):
        
        if sample:  
            '''下采样 '''
            rus = RandomUnderSampler()
            trainx_,trainy_ = rus.fit_sample(trainx,trainy)            
        
        for i in range(0,trainx_.shape[0]-batch_size+1,batch_size):
            model.train()
            x=trainx_[i:i+batch_size].reshape(seq_len,batch_size,input_dim)
            y=trainy_[i:i+batch_size]
            
            inputs = autograd.Variable(torch.from_numpy(x).float())
            labels = autograd.Variable(torch.LongTensor(y))
            
            if cuda:
                inputs, labels = inputs.cuda(device), labels.cuda(device)
                
            model.zero_grad()
            model.hidden=model.init_hidden(inputs.shape[1])
            
            output = model(inputs)
            loss = loss_function(output, labels.squeeze(0))
            
            loss.backward(retain_graph=False)           # back propagation !important
            optimizer.step()   
            
            if i%200==0:
                print('epoch:{}, step:{},loss:{}'.format(epoch,i,loss.item()))
                
            if i%2000==0:
                test(model,loss_function,testx,testy,epoch,batch_size,seq_len,input_dim,num_layers,cuda,device)                
                
    return model


def test(model,loss_function,testx,testy,epoch,batch_size,seq_len,input_dim,num_layers,cuda=0,device=0):
    '''
    '''
    model.eval()
    
    with torch.no_grad():        
        
        x=testx.reshape(seq_len,testx.shape[0],input_dim)
        y=testy            
        inputs = autograd.Variable(torch.from_numpy(x).float())
        labels = autograd.Variable(torch.LongTensor(y))        
        
        if cuda:
            inputs, labels = inputs.cuda(device), labels.cuda(device)

        model.hidden=model.init_hidden(inputs.shape[1])
        output = model(inputs)
        test_loss=loss_function(output, labels.squeeze(0)).data

    pred = output.max(1)[1].numpy() # get the index of the max log-probability    
    f1_score=metrics.f1_score(y,pred)
    accuracy=metrics.accuracy_score(y,pred)
    auc=metrics.roc_auc_score(y,output.numpy()[:,1])
    
    print('\nepoch:{} Test set: Average loss: {:.4f}, f1:{}, accuracy:{}, auc:{}\n'.format(epoch,\
        test_loss,f1_score,accuracy,auc))

    return test_loss

