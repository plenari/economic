#coding=utf-8

'''
定长时间序列
训练RNN模型定长序列，假设在Ti交易日可以通过前m交易日技术分析走势预判后第n交易日股价涨跌幅度，
并且RNN模型可以自动从T{i-m}到T_i时间序列学习到这种预测关系。
输入数据格式[批次，步长，多因子] 其中步长表示从T_{i-m}到T_i时间序列
class.fit(trainX, trainY)训练模型
clf.pred_prob(trainX) 预测返回概率矩阵
clf.pred_signal(trainX) 预测返回标签
trainX 输入格式 [row, time_step, num_input]
trainY 输入格式 [row]
batch_size=128 喂入批次大小
display_step=5 显示步长
layer_units_num=2000 隐藏层单元数目
training_epoch=100 训练次数

假设我有1000只股票，这就是samples=1000
每次？
每只股票有20因子，这是num_input=20，也是隐藏层的个数
每次运行十天的数据，time_step=10
trainX 输入格式 [row, time_step, num_input]
那么每次输入的数据就是100x10x20
'''
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import datetime
import matplotlib.pylab as plt

class lstm(object):
    def __init__(self,
                batch_size = 10,#多少个样本
                learning_rate = 0.01,#
                training_epoch =1 ,#迭代次数
                display_step = 10,#
                layer_units_num = 20,#
                time_step=15,#日子，第二个维度
                num_input=20,#因子，第三个维度
                classes = 6):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.training_epoch = training_epoch
        self.display_step = display_step
        self.layer_units_num = layer_units_num
        self.classes=classes
        self.time_step=time_step
        self.num_input=num_input
    def dense_to_one_hot(self,return_y):
        """标签 转换one hot 编码
        输入return_y 为y日收益率,然后根据收益率分成self.classes分
        标签从0到self.classes-1。
        那个维度表示比较大呢？
        所以最后一个
        """
        return_y=self.quantile(return_y)
        raws_labels = return_y.shape[0]#多少列数据
        index_offset = np.arange(raws_labels) * self.classes
        labels_one_hot = np.zeros((raws_labels, self.classes))
        labels_one_hot.flat[index_offset + return_y.ravel()] = 1        
        return labels_one_hot 
    
    def one_hot_to_labels(self,labels_one_hot):
        #把one_hot        
        return np.where(labels_one_hot)[1]
        
    def Preprocessing(self, trainX, trainY, seed=False):
        '''
        预处理[batch_size, max_time, n_inputs]
        '''        
        if seed:
            tf.set_random_seed(201801318)
        # 对 weights biases 初始值的定义
        weights = {
        'in': tf.Variable(tf.random_normal([self.num_input, self.layer_units_num])),
        # shape (128, 10)
        'out': tf.Variable(tf.random_normal([self.layer_units_num, self.classes]))}
        biases = {# shape (128, )
        'in': tf.Variable(tf.constant(0.1, shape=[self.layer_units_num, ])),
        # shape (10, )
        'out': tf.Variable(tf.constant(0.1, shape=[self.classes, ]))}
        
        self.weights = weights
        self.biases = biases
        
        self.X = tf.placeholder(dtype=tf.float32, shape=[None, self.time_step, self.num_input], name='trainX') # 批次，时间序列，多因子
        self.Y = tf.placeholder(dtype= tf.float32, shape=[None, self.classes], name='trainY') 
        self.keep_prob = tf.placeholder(dtype= tf.float32)
        
        
    def Model(self):
        '''
        
        '''
        keep_prob = self.keep_prob
        self.X_for_in = tf.reshape(self.X, [-1,self.num_input])
        self.X_in = tf.matmul(self.X_for_in, self.weights['in']) + self.biases['in']
        self.X_in = tf.reshape(self.X_in, [-1,self.time_step,self.layer_units_num])
        
        layer_1 = tf.nn.rnn_cell.BasicLSTMCell(num_units= self.layer_units_num,forget_bias=1.,\
            state_is_tuple=True, activation=tf.tanh)
        layer_1 = tf.nn.rnn_cell.DropoutWrapper(cell=layer_1, output_keep_prob= keep_prob)

        Layers = tf.nn.rnn_cell.MultiRNNCell(cells=[layer_1]*2,state_is_tuple = True)
        
        init_state = Layers.zero_state(self.batch_size, dtype=tf.float32)
        
        outputs,states = tf.nn.dynamic_rnn(cell=Layers, inputs=self.X_in, initial_state=init_state,dtype=tf.float32,time_major=False)
        print('hidden_size: ',states[-1][1].shape,)#最后一个batch_size的hidden_size
        hidden_size=states[-1][1]
        return tf.nn.bias_add(value= tf.matmul(hidden_size, self.weights['out']), bias= self.biases['out'])  
        
    def train(self, trainX, trainY, seed=False):
        #创建模型，
        self.sess = tf.InteractiveSession()
        self.Preprocessing(trainX, trainY, seed)
        tmp = self.Model()#return bias
        self.predict = tf.nn.softmax(tmp)
        
        self.cost = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits=tmp, labels=self.Y))        
        self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.cost) # 0 设置训练器        
        self.correct_pred = tf.equal(tf.argmax(tmp,1), tf.argmax(self.Y,1))#
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))        #
        self.init = tf.global_variables_initializer()           
        
    def fit(self,trainX, trainY, dropout = 0.3, seed=True):
        #
        self.train(trainX, trainY, seed=True)
        sess = self.sess
        sess.run(self.init)
        batch_size = self.batch_size
        trainY = self.dense_to_one_hot(trainY)
        #训练
        for i in range(int(len(trainX)/batch_size)):#3
            batch_x = trainX[i*batch_size : (i+1)*batch_size]
            batch_y = trainY[i*batch_size : (i+1)*batch_size]
            sess.run(self.optimizer, feed_dict={self.X:batch_x, self.Y:batch_y, self.keep_prob:(1.-dropout)})
            if i%self.display_step==0:
                loss, acc = sess.run([self.cost,self.accuracy], feed_dict={self.X:batch_x, self.Y:batch_y, self.keep_prob:1.})
                print(str(i)+"th "+'Epoch Loss = {:.5f}'.format(loss)+" Training Accuracy={:.5f}".format(acc))
        #self.sess= sess
        print("Optimization Finished!") 

    def pred_prob(self, testX):
        #验证
        sess = self.sess
        predict_output = sess.run(self.predict,feed_dict={self.X:testX, self.keep_prob:1.})
        #predict_output = np.delete(predict_output, obj=0, axis=0)        
        return predict_output
    
    def pred(self, testX): 
        #验证
        pred_prob = self.pred_prob(testX)
        return np.argmax(pred_prob, axis=1)
    
    def next_batch(self,batch_size,sample,):
        
        '''
        '''
        pass
    def quantile(self,return_y):
        '''
        把reutrn_y限制到10,90分位数之内
        按照类别个数贴标签，越大越好。
        因为会是从0到6有七个分类，所以减了1。
        '''    
        classes=self.classes-1
        upper,lower = np.percentile(return_y, [90,10])
        
        return_y=np.clip(return_y,lower,upper)
        #贴标签划分范围
        label_step=[lower+i*(upper-lower)/classes for i in range(classes)]
        return_y_labels=np.searchsorted(label_step,return_y)
        return return_y_labels
    
    def save(self):
        #un
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(init_op)
            save_path = saver.save(sess, "/tmp/model.ckpt")
        print( "Model saved in file: ", save_path)

    def restore(self):
        #un
        saver = tf.train.Saver()
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph('model.ckpt-1000.meta')
            saver.restore(sess, os.path.join('','./'))

          
    
clf = lstm()
trainX=np.random.randn(1000,15,20)
trainY=np.round(np.random.randint(0,6,1000))
clf.fit(trainX, trainY)
re=clf.pred(np.random.randn(10,15,20))
print(np.array(re).mean())

