#author Jiali Zhou
import pandas as pd
from sklearn import cross_validation
from sklearn import feature_selection
import numpy as np
#import data
def import_data(train_data, test_data):
	train_x = pd.read_table(train_data)
	test_x = pd.read_table(test_data)
	#split train data into features of training set and target variable
	train_target = train_x['target']
	train_x = train_x.drop('target',1)
	return train_x, test_x, train_target

def normalize_data(x):
	#deal with missing data
	g = x.columns.to_series().groupby(x.dtypes).groups
	for key, value in g.items():
		if key == 'float64':
			for name in value:
				x[name] = x[name].fillna(x[name].mean())
		else:
			for name in value:
				counts = x[name].value_counts()
				x[name] = x[name].fillna(counts.keys()[0])
	#split categorical data into multipal columns
	x = pd.get_dummies(x)
	#normalize training set and testing set, name it train_norm and test_norm
	x_norm = (x - x.mean()) / (x.max() - x.min())
	return x_norm

def soft_thresholding(a, sigma):
  result = 1
  if a < 0:
    result = -1
  result *= abs(abs(a) - sigma)
  return result

def compute_square_loss(X, y, theta):
    return ((np.linalg.norm(np.dot(X,theta) - y))**2) / X.shape[0]

def square_loss(X, y_predict, y):
	return ((np.linalg.norm(y_predict - y))**2) / X.shape[0]

def AkaShooting(X, y, Lambda):
	n, D = X.shape
	w = np.linalg.inv(X.T.dot(X) + Lambda*np.identity(D)).dot(X.T).dot(y)
	dist = 1
	while (dist > 1e-6):
		prev_w = w.copy()
		for j in range(D):
			a_j = 2 * np.linalg.norm(X.iloc[:,j])**2
			z = y - np.dot(X,w.T) + w[j] * X.iloc[:,j]
			c_j = 2 * np.dot(X.iloc[:,j],z)
			w[j] = soft_thresholding(c_j / float(a_j), Lambda / float(a_j))
		dist = np.linalg.norm(prev_w - w)
	return w

def stochastic_grad_descent(X, y, lambda_reg = 1, num_iter = 100):
	num_instances, num_features = X.shape
	theta = np.ones(num_features)
	theta_hist = np.zeros((num_instances, num_features))
	#Initialize theta_hist
	loss_hist = np.zeros(num_instances)
	pointList = range(num_instances)
	step_size_p = 2
	#set stepsize
	for i in range(num_iter):
		#shuffle the points
		#change alpha
		np.random.shuffle(pointList)
		for j in pointList:
			theta_hist[j] = theta
			loss_hist[j] = compute_square_loss(X, y, theta)
			#simultaneously update theta
			grad = (np.dot(X.iloc[j], theta) - y.iloc[j]) * X.iloc[j] + 2 * lambda_reg * theta
			theta -= 1. / np.sqrt(step_size_p) * grad
			step_size_p += 1
	min_loss = min(loss_hist)
	index_min = loss_hist.tolist().index(min_loss)
	return theta_hist[index_min], min_loss













