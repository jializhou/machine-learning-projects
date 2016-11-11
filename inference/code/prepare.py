from gensim import models, similarities
import logging, gensim, bz2
corpus = []
f = open('docword.nipstimes.txt','r')
lines = f.readlines()[3:]
for line in lines:
    s = line.strip().split(' ')
    doc, word, cnt = int(s[0])-1, int(s[1]), int(s[2])
    if doc ==len(corpus):
        corpus.append([])
    corpus[-1].append((word,cnt))
dic = open('vocab.nipstimes.txt','r')
lines = dic.readlines()
id2word = {}
for i in xrange(len(lines)):
    w = lines[i].strip()
    id2word[i] = w   
