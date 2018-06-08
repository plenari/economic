# coding: utf-8
import tensorflow as tf
import numpy as np
'''
我用rnn做一个回归

'''

class lstm:
    def __init__(self):
        '''
        sess 关闭之后数据就会丢失。
        '''
        # hyperparameters
        self.lr = 0.001                  # learning rate
        #self.training_iters = 100     # train step 上限
        self.batch_size = 40            
        self.n_inputs = 80               # MNIST data input (img shape: 28*28)
        self.n_steps =20                # time steps
        self.n_hidden_units = 100        # neurons in hidden layer

        self.Preprocessing()
        self.sess=tf.Session()
        
    def Preprocessing(self):
        '''
        初始化数据变量和入口
        '''
        # 1. 由于batch_size=40,所以x的形状是40x20x80.进去之后改变形状为：800x80
        # 2. 所以$x*$weights['in']$*$weights['out']的过程是：800x80***80x128 *** 128x10 ====3584x10
        # 3. 就是y的形状
        # x y placeholder
        #x.shape: -1x28x28
        self.x = tf.placeholder(tf.float32, [None, self.n_steps, self.n_inputs])
        #y.shape :-1x10
        self.y = tf.placeholder(tf.float32, [None, self.n_inputs])
        # 对 weights biases 初始值的定义
        self.weights = {
            # shape (80, 100)
            'in': tf.Variable(tf.random_normal([self.n_inputs, self.n_hidden_units])),
            # shape (100,80 )
            'out': tf.Variable(tf.random_normal([self.n_hidden_units, self.n_inputs]))
        }
        self.biases = {
            # shape (100, )
            'in': tf.Variable(tf.constant(0.1, shape=[self.n_hidden_units, ])),
            # shape (80, )
            'out': tf.Variable(tf.constant(0.1, shape=[self.n_inputs, ]))
        }

    def Model(self):
        '''
        创建模型
        不知道这些变量是否应该用同一个变量。
        '''
        # 原始的 X 是 3 维数据, 我们需要把它变成 2 维数据才能使用 weights 的矩阵乘法
        # X ==> (40 batches * 20 steps, 80 inputs)
        X = tf.reshape(self.x, [-1, self.n_inputs])    
        # X_in = W*X + b===800*80
        X_in = tf.matmul(X, self.weights['in']) + self.biases['in']
        # X_in ==> (40 batches, 20 steps, 100 hidden) 换回3维
        X_in = tf.reshape(X_in, [-1, self.n_steps, self.n_hidden_units])
    
        # 使用 basic LSTM Cell.
        lstm_cell = tf.contrib.rnn.BasicLSTMCell(self.n_hidden_units, forget_bias=1, state_is_tuple=True)
        init_state = lstm_cell.zero_state(self.batch_size, dtype=tf.float32) # 初始化全零 state
        outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=init_state, time_major=False)
        #print(outputs)#128,28,100
        #[batch_size, cell.state_size]
        results = tf.matmul(final_state[-1], self.weights['out']) + self.biases['out']
        return results
    
    def train(self,trainy):
        '''
        构建出可以fit的模型.
        '''
        self.pred =self.Model()
        cost = tf.reduce_mean(tf.square(self.pred-trainy))
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(cost)
        #准确率
        correct_pred = tf.reduce_mean(tf.square(self.pred-trainy))
        self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        
    def fit(self,trainx,trainy):
        '''
        
        '''
        self.init=tf.global_variables_initializer()
        self.sess.run(self.init)
        step = 0
        select=np.arange(0,180)
        for i in range(1000):
            index=np.random.choice(select)
            batch_xs=trainx[index:index+self.batch_size]
            batch_ys=trainy[index:index+self.batch_size]
            
            self.sess.run([self.train_op], feed_dict={
                self.x: batch_xs,
                self.y: batch_ys,
            })
            if step % 20 == 0:
                print(step,self.sess.run(self.accuracy, feed_dict={
                self.x: batch_xs,
                self.y: batch_ys,
            }))
            step += 1
    def predict(self,testx):
        '''
        预测数值。
        '''
        pred=self.sess.run(self.pred,feed_dict={self.x:testx})
        return pred
    
    def save(self,file):
        '''
        保存模型
        '''
        saver = tf.train.Saver()
        #self.sess.run(init_op)
        save_path = saver.save(self.sess, file)
        print( "Model saved in file: ", save_path)

    def close(self):
        '''
        '''
        self.sess.close()
        
    def restore(self,file):
        '''
        
        '''
        saver = tf.train.Saver()
        #saver = tf.train.import_meta_graph('model.ckpt-1000.meta')
        saver.restore(self.sess, file)        
        