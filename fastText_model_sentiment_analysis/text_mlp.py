import tensorflow as tf
import numpy as np


class MLP(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """
    def __init__(
      self, sequence_length, num_classes, vocab_size,
      embedding_size, filter_sizes, num_filters, l2_reg_lambda):

        # Placeholders for input, output and dropout (which you need to implement!!!!)
        self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
        

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)

        # Embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            used = tf.sign(self.input_x)
            length = tf.reduce_sum(used, reduction_indices=1)
            length = tf.cast(length, tf.float32)
            mul_length = tf.tile(length,[embedding_size])
            y = tf.reshape(mul_length, [embedding_size,-1])
            self.mask_length = tf.transpose(y)
            # mat = tf.placeholder(1.0, [embedding_size,])
            # self.mask_length = tf.transpose(tf.mul(mat, length))
            embedd_W = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W")
            self.embedded_chars = tf.nn.embedding_lookup(embedd_W, self.input_x)

            self.embedded_sum = tf.reduce_sum(self.embedded_chars,1)
            self.embedded_reduced = tf.div(self.embedded_sum, self.mask_length)


        # Create a MLP + maxpool layer for each filter size
        pooled_outputs = []
        num_filters = 2
        with tf.name_scope("mlp"):
            # MLP Layer
            W = tf.Variable(tf.random_normal([embedding_size, num_filters]), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
            self.mlp = tf.matmul(self.embedded_reduced, W)
            # Apply nonlinearity
            self.outputs = tf.sigmoid(tf.nn.bias_add(self.mlp, b), name="sigmoid")
        # Add dropout
        ###############add your code here################
        #hint: you need to add dropout on self.outputs with tf.nn.dropout()
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(self.outputs, self.dropout_keep_prob)

        # Final (unnormalized) scores and predictions
        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        # CalculateMean cross-entropy loss
        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(self.scores, self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # Accuracy
        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
