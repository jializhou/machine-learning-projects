import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import random

'''
K: number of topics
alpha: parameters vector of length K
theta :posterior topic distribution for each topic, length K
beta_wn : length K vector(for every word wn, the probability to topic k (k=1,...,K))
N : number of words
Z : topic assignment to each of the word w, length = N
cnt_k: word counts assigned to topic k
'''
def gibbs_sampler(collapsed):
	#initialize all parameters
	Dir = np.random.dirichlet
	Mult = np.random.multinomial
	r = open('./ps4_data/abstract_nips21_NIPS2008_0517.txt.ready','r')
	lines = r.readlines()
	K = int(lines[0])
	alpha = [float(i) for i in lines[1].split()]
	theta = Dir(alpha, size = 1)[0]
	beta_wn = []
	words = []
	for line in lines[2:]:
		s = line.rstrip().split()
		words.append(s[0])
		beta_wn.append([float(i) for i in s[1:]])
	N = len(beta_wn)
	Z = np.nonzero(Mult(1, theta, size = N))[1]
	iters = int(1e+3)
	cnt_k = [0]*K
	for k in Z:
		cnt_k[k] += 1
	Posterior_wn = {}
	l2_error = []
	burn_in = 50
	E_theta = [0]*K
	total = [0]*K
	def normalize(lst):
	    s = sum(lst)
	    return np.array(map(lambda x: float(x)/s, lst))
	def L2_error(x, y):
		t = [(a-b)**2 for a,b in zip(x,y)]
		return np.sqrt(sum(t))


	#gibbs sampling
	for iter in xrange(iters):
		for n, beta in zip(xrange(N),beta_wn):
			alpha_new = np.sum([cnt_k, alpha], axis=0)
			theta = Dir(alpha_new, size=1)[0]
			cnt_k[Z[n]] -= 1
			if collapsed:
				Posterior_wn[n] = normalize(beta * alpha_new)
			else:
				Posterior_wn[n] = normalize(beta * theta)
			new_topic = np.nonzero(Mult(1, Posterior_wn[n], size=1))[1][0]
			Z[n] = new_topic
			cnt_k[new_topic] += 1
		if iter<burn_in:
			continue
		total = np.sum([total, alpha_new], axis=0)
		E_theta = normalize(total)	
		l2_error.append(E_theta)

	l2_error = [L2_error(i, E_theta) for i in l2_error]
	return l2_error


fig = plt.figure()

color_all = ['ro','bs']

	plt.plot(x,result_c1,color)
plt.legend(['K = 1', 'K = 10', 'K = 19'], loc='upper left')
plt.xlabel('N = n')
plt.ylabel('p(N = n|K,C)')
plt.show()