#! /usr/bin/env python

import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
from text_mlp import MLP
from tensorflow.contrib import learn
import pickle
tf.flags.DEFINE_integer("embedding_dim", 64, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "3,4,5", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 5, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.8, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.4, "L2 regularizaion lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 16, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 30, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")


print("Loading data...")
max_document_length = 750
max_word_cnt = 10000
n_gram = 5
print max_document_length, max_word_cnt
# Parameters
# ==================================================

# Model Hyperparameters
class Train(object):
    def __init__(self):

        x_text, y = data_helpers.load_data_and_labels("./train/pos","./train/neg")

        # Build vocabulary
        x_list = [x.split(" ") for x in x_text]
        vocab_processor = data_helpers.n_grams(x_list, max_word_cnt, n_gram)
        print 'feed finished'
        x = np.array(data_helpers.fit_transform(vocab_processor, x_list, max_document_length, n_gram))
        # print x[0]
        print 'fit transform finished'


        # Randomly shuffle data
        np.random.seed(10)
        shuffle_indices = np.random.permutation(np.arange(len(y)))
        x_shuffled = x[shuffle_indices]
        y_shuffled = y[shuffle_indices]

        # Split train/test set
        # TODO: This is very crude, should use cross-validation
        x_train, x_dev = x_shuffled[:-1000], x_shuffled[-1000:]
        y_train, y_dev = y_shuffled[:-1000], y_shuffled[-1000:]
        print("Vocabulary Size: {:d}".format(len(vocab_processor)))
        print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))


        # Training
        # ==================================================

        with tf.Graph().as_default():
            session_conf = tf.ConfigProto(
              allow_soft_placement=FLAGS.allow_soft_placement,
              log_device_placement=FLAGS.log_device_placement)
            sess = tf.Session(config=session_conf)
            with sess.as_default():
                cnn = MLP(
                    sequence_length=x_train.shape[1],
                    num_classes=2,
                    vocab_size=len(vocab_processor),
                    embedding_size=FLAGS.embedding_dim,
                    filter_sizes=list(map(int, FLAGS.filter_sizes.split(","))),
                    num_filters = FLAGS.num_filters,
                    l2_reg_lambda=FLAGS.l2_reg_lambda)

                # Define Training procedure
                global_step = tf.Variable(0, name="global_step", trainable=False)
                starter_learning_rate = 1e-3
                learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step,
                                                           3000, 0.96, staircase=True)
                optimizer = tf.train.AdamOptimizer(starter_learning_rate)
                grads_and_vars = optimizer.compute_gradients(cnn.loss)
                train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

                # Keep track of gradient values and sparsity (optional)
                grad_summaries = []
                for g, v in grads_and_vars:
                    if g is not None:
                        grad_hist_summary = tf.histogram_summary("{}/grad/hist".format(v.name), g)
                        sparsity_summary = tf.scalar_summary("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
                        grad_summaries.append(grad_hist_summary)
                        grad_summaries.append(sparsity_summary)
                grad_summaries_merged = tf.merge_summary(grad_summaries)

                # Output directory for models and summaries
                timestamp = str(int(time.time()))
                self.out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
                print("Writing to {}\n".format(self.out_dir))

                # Summaries for loss and accuracy
                loss_summary = tf.scalar_summary("loss", cnn.loss)
                acc_summary = tf.scalar_summary("accuracy", cnn.accuracy)

                # Train Summaries
                train_summary_op = tf.merge_summary([loss_summary, acc_summary, grad_summaries_merged])
                train_summary_dir = os.path.join(self.out_dir, "summaries", "train")
                train_summary_writer = tf.train.SummaryWriter(train_summary_dir, sess.graph)

                # Dev summaries
                dev_summary_op = tf.merge_summary([loss_summary, acc_summary])
                dev_summary_dir = os.path.join(self.out_dir, "summaries", "dev")
                dev_summary_writer = tf.train.SummaryWriter(dev_summary_dir, sess.graph)

                # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
                self.checkpoint_dir = os.path.abspath(os.path.join(self.out_dir, "checkpoints"))
                checkpoint_prefix = os.path.join(self.checkpoint_dir, "model")
                if not os.path.exists(self.checkpoint_dir):
                    os.makedirs(self.checkpoint_dir)
                saver = tf.train.Saver(tf.all_variables())
                # Write vocabulary
                pickle.dump(vocab_processor, open(os.path.join(self.out_dir,"vocab"), "wb" ) )
                # Initialize all variables
                sess.run(tf.initialize_all_variables())

                def train_step(x_batch, y_batch):
                    """
                    A single training step
                    """
                    feed_dict = {
                      cnn.input_x: x_batch,
                      cnn.input_y: y_batch,
                      cnn.dropout_keep_prob: FLAGS.dropout_keep_prob
                    }
                    _, step, summaries, loss, accuracy = sess.run(
                        [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
                        feed_dict)
                    time_str = datetime.datetime.now().isoformat()
                    print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
                    train_summary_writer.add_summary(summaries, step)

                def dev_step(x_batch, y_batch, writer=None):
                    """
                    Evaluates model on a dev set
                    """
                    feed_dict = {
                      cnn.input_x: x_batch,
                      cnn.input_y: y_batch,
                      cnn.dropout_keep_prob:1
                    }
                    step, summaries, loss, accuracy = sess.run(
                        [global_step, dev_summary_op, cnn.loss, cnn.accuracy],
                        feed_dict)
                    time_str = datetime.datetime.now().isoformat()
                    print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
                    if writer:
                        writer.add_summary(summaries, step)

                # Generate batches
                t = list(zip(x_train, y_train))
                batches = data_helpers.batch_iter(
                    t, FLAGS.batch_size, FLAGS.num_epochs)
                # Training loop. For each batch...
                for batch in batches:
                    x_batch, y_batch = zip(*batch)
                    train_step(x_batch, y_batch)
                    current_step = tf.train.global_step(sess, global_step)
                    if current_step % FLAGS.evaluate_every == 0:
                        print("\nEvaluation:")
                        dev_step(x_dev, y_dev, writer=dev_summary_writer)
                        print("")
                    if current_step % FLAGS.checkpoint_every == 0:
                        path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                        print("Saved model checkpoint to {}\n".format(path))


