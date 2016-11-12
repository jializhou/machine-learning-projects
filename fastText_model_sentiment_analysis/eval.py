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
from train import *

T = Train()

# Parameters
# ==================================================

# Eval Parameters
tf.flags.DEFINE_string("checkpoint_dir", T.checkpoint_dir, "Checkpoint directory from training run")
FLAGS = tf.flags.FLAGS


x_raw, y_test = data_helpers.load_data_and_labels("./test/pos","./test/neg")
y_test = np.argmax(y_test, axis=1)


# Map data into vocabulary
vocab_processor = pickle.load( open(os.path.join(T.out_dir,"vocab"), "rb" ) )
x_list = [x.split(" ") for x in x_raw]
x_test = np.array(list(data_helpers.fit_transform(vocab_processor, x_list, max_document_length, n_gram)))

print("\nEvaluating...\n")
checkpoint_file = tf.train.latest_checkpoint(T.checkpoint_dir)

# Evaluation
# ==================================================
graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=FLAGS.allow_soft_placement,
      log_device_placement=FLAGS.log_device_placement)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the saved meta graph and restore variables
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        saver.restore(sess, checkpoint_file)

        # Get the placeholders from the graph by name
        input_x = graph.get_operation_by_name("input_x").outputs[0]
        # input_y = graph.get_operation_by_name("input_y").outputs[0]
        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        # Tensors we want to evaluate
        predictions = graph.get_operation_by_name("output/predictions").outputs[0]

        # Generate batches for one epoch
        batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

        # Collect the predictions here
        all_predictions = []

        for x_test_batch in batches:
            batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
            all_predictions = np.concatenate([all_predictions, batch_predictions])

# Print accuracy if y_test is defined
    correct_predictions = float(sum([1 if all_predictions[i]==y_test[i] else 0 for i in xrange(len(all_predictions))]))
    print("Total number of test examples: {}".format(len(y_test)))
    print("Accuracy: {:g}".format(correct_predictions/float(len(y_test))))
