
# coding: utf-8

# ### 一. 单个rnn +mnist

# ####  1.1 RNN 来进行分类的训练 (Classification).
#  1. 会继续使用到手写数字 MNIST 数据集. 
#  2.  RNN 从每张图片的第一行像素读到最后一行, 然后再进行分类判断.
#  3. 接下来我们导入 MNIST 数据并确定 RNN 的各种参数(hyper-parameters)

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
tf.set_random_seed(1)   # set random seed

# 导入数据
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# hyperparameters
lr = 0.001                  # learning rate
training_iters = 10000     # train step 上限
batch_size = 40            
n_inputs = 28*4               # MNIST data input (img shape: 28*28)
n_steps =7                # time steps
n_hidden_units = 100        # neurons in hidden layer
n_classes = 10              # MNIST classes (0-9 digits)



# 1. 由于batch_size=128,所以x的形状是128x28x28.进去之后改变形状为：3584x28
# 2. 所以$x*$weights['in']$*$weights['out']的过程是：3584x28***28x128 *** 128x10 ====3584x10
# 3. 就是y的形状

# x y placeholder
#x.shape: -1x28x28
x = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
#y.shape :-1x10
y = tf.placeholder(tf.float32, [None, n_classes])

# 对 weights biases 初始值的定义
weights = {
    # shape (28, 128)
    'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
    # shape (128, 10)
    'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
}
biases = {
    # shape (128, )
    'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
    # shape (10, )
    'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
}





def RNN(X, weights, biases):
    # 原始的 X 是 3 维数据, 我们需要把它变成 2 维数据才能使用 weights 的矩阵乘法
    # X ==> (128 batches * 28 steps, 28 inputs)
    print(X.shape)
    X = tf.reshape(X, [-1, n_inputs])

    # X_in = W*X + b===3584*128
    X_in = tf.matmul(X, weights['in']) + biases['in']
    # X_in ==> (128 batches, 28 steps, 128 hidden) 换回3维
    X_in = tf.reshape(X_in, [-1, n_steps, n_hidden_units])
    print(X_in.shape)
    # 使用 basic LSTM Cell.
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden_units, forget_bias=1.0, state_is_tuple=True)
    init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32) # 初始化全零 state
    outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=init_state, time_major=False)
    print(outputs)#128,28,100
    #[batch_size, cell.state_size]
    results = tf.matmul(final_state[-1], weights['out']) + biases['out']
    return results


pred = RNN(x, weights, biases)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
train_op = tf.train.AdamOptimizer(lr).minimize(cost)


correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()
sess=tf.Session()

sess.run(init)
step = 0
while step * batch_size < training_iters:
    batch_xs, batch_ys = mnist.train.next_batch(batch_size)
    batch_xs = batch_xs.reshape([batch_size, n_steps, n_inputs])
    sess.run([train_op], feed_dict={
        x: batch_xs,
        y: batch_ys,
    })
    if step % 100 == 0:
        print(step,sess.run(accuracy, feed_dict={
        x: batch_xs,
        y: batch_ys,
    }))
    step += 1
print('done')


# ### 5. 结果验证，时间序列？？必须相同维度


test_len = batch_size
test_data = mnist.test.images[:test_len].reshape((-1, n_steps, n_inputs))
test_label = mnist.test.labels[:test_len]
print ("Testing Accuracy:",        sess.run(accuracy, feed_dict={x: test_data, y: test_label}))

