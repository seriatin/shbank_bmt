from __future__ import print_function

import os
import pickle
import tensorflow as tf
from args import bmt_args
from utils import concat_timestamp, create_export_dir

if __name__ == '__main__':
    parser = bmt_args()
    args = parser.parse_args()

mnist_data = 'mnist.pkl'

if os.path.exists(mnist_data):
    with open(mnist_data, 'rb') as f:
        mnist = pickle.load(f)
else:
    # Import MNIST data
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)
    with open(mnist_data, 'wb') as f:
        pickle.dump(mnist, f)

def xaver_init(n_inputs, n_outputs, uniform = True):
    if uniform:
        init_range = tf.sqrt(6.0/ (n_inputs + n_outputs))
        return tf.random_uniform_initializer(-init_range, init_range)

    else:
        stddev = tf.sqrt(3.0 / (n_inputs + n_outputs))
        return tf.truncated_normal_initializer(stddev=stddev)

learning_rate = 0.001
training_epochs = args.epochs
batch_size = 100
display_step = 1

# tensorflow graph input
X = tf.placeholder('float', [None, 784]) # mnist data image of shape 28 * 28 = 784
Y = tf.placeholder('float', [None, 10]) # 0-9 digits recognition = > 10 classes

# set dropout rate
dropout_rate = tf.placeholder("float")

# set model weights
W1 = tf.get_variable("W1", shape=[784, 256], initializer=xaver_init(784, 256))
W2 = tf.get_variable("W2", shape=[256, 256], initializer=xaver_init(256, 256))
W3 = tf.get_variable("W3", shape=[256, 256], initializer=xaver_init(256, 256))
W4 = tf.get_variable("W4", shape=[256, 256], initializer=xaver_init(256, 256))
W5 = tf.get_variable("W5", shape=[256, 10], initializer=xaver_init(256, 10))

B1 = tf.Variable(tf.random_normal([256]))
B2 = tf.Variable(tf.random_normal([256]))
B3 = tf.Variable(tf.random_normal([256]))
B4 = tf.Variable(tf.random_normal([256]))
B5 = tf.Variable(tf.random_normal([10]))

# Construct model
_L1 = tf.nn.relu(tf.add(tf.matmul(X,W1),B1))
L1 = tf.nn.dropout(_L1, dropout_rate)
_L2 = tf.nn.relu(tf.add(tf.matmul(L1, W2),B2)) # Hidden layer with ReLU activation
L2 = tf.nn.dropout(_L2, dropout_rate)
_L3 = tf.nn.relu(tf.add(tf.matmul(L2, W3),B3)) # Hidden layer with ReLU activation
L3 = tf.nn.dropout(_L3, dropout_rate)
_L4 = tf.nn.relu(tf.add(tf.matmul(L3, W4),B4)) # Hidden layer with ReLU activation
L4 = tf.nn.dropout(_L4, dropout_rate)

hypothesis = tf.add(tf.matmul(L4, W5), B5) # No need to use softmax here

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y)) # Softmax loss
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost) # Adam Optimizer

# Initializing the variables
init = tf.initialize_all_variables()

# Launch the graph,
with tf.Session() as sess:
    sess.run(init)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)

        # Fit the line.
        for step in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)

            # Fit training using batch data
            # set up 0.7 for training time
            sess.run(optimizer, feed_dict={X: batch_xs, Y: batch_ys, dropout_rate: 0.7})

            # Compute average loss
            avg_cost += sess.run(cost, feed_dict={X: batch_xs, Y: batch_ys, dropout_rate: 0.7})/total_batch
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' %(epoch+1), "cost=", "{:.9f}".format(avg_cost))

    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({X: mnist.test.images, Y: mnist.test.labels, dropout_rate: 1}))

    print("Export Serving Model!")
    export_dir = create_export_dir(args.export_dir, args.model_name)
    tf.saved_model.simple_save(sess, concat_timestamp(export_dir), inputs={"image": X}, outputs={'classes': Y})    

