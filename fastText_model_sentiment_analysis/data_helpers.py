import numpy as np
import re
import itertools
from collections import Counter
import os
import tensorflow as tf


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(path1, path2):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = []    
    for file in os.listdir(path1):
        if file.endswith(".txt"):
            positive_examples.append(open(path1+'/'+file, "r").readlines()[0])
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = []
    for file in os.listdir(path2):
        if file.endswith(".txt"):
            negative_examples.append(open(path2+'/'+file, "r").readlines()[0])
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size)
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


def n_grams(x, cnt,n):
    voc = {}
    for lis in x:
        for i in xrange(len(lis)):
            voc[lis[i]] = voc.get(lis[i], 0)+1
            for j in xrange(1,n):
                if i+j<=len(lis):
                    n_gram = ' '.join(lis[i:(i+j)])
                    voc[n_gram] = voc.get(n_gram, 0)+1
    v_items = sorted(voc.items(), key=lambda t:t[1], reverse = True)[:cnt]
    voc = {}
    i = 1
    for item in v_items:
        voc[item[0]] = i
        i += 1
    voc['<oov>'] = 0
    return voc

def fit_transform(voc, x, length,n):
    """Transform documents to word-id matrix.
    Convert words to ids with vocabulary fitted with fit or the one
    provided in the constructor.
    Args:
      x: An iterable which yield either str or unicode.
    Yields:
      res: iterable, [n_samples, max_document_length]. Word-id matrix.
    """
    ind = voc['<oov>']
    res = []
    for lis in x:
        word_ids = np.zeros(length, np.int64)
        le = 0
        for j in xrange(n):
            for i in xrange(len(lis)):
                if i+j>len(lis) or le>=length:
                    break
                if not j:
                    n_gram = lis[i]
                else:
                    n_gram = ' '.join(lis[i:(i+j)])
                word_ids[le] = voc.get(n_gram, ind)
                le += 1
        res.append(word_ids)
    return res

def length(sequence, embedding_size):
    used = tf.sign(sequence)
    length = tf.reduce_sum(used, reduction_indices=1)
    y = tf.Variable(tf.constant(0.1, shape=[embedding_size]))
    return tf.meshgrid(length, y)[0]






