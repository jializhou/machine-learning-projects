import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import math
n_classes = 2
plot_colors = 'by'
plot_step = 0.02
# Load data
X_train = pd.read_csv('data/banana_train.csv',header=None)
y_train = X_train[0]
X_train.drop(X_train.columns[0], axis=1, inplace=True)


X_test = pd.read_csv('data/banana_test.csv',header=None)
y_test = X_test[0]
X_test.drop(X_test.columns[0], axis=1, inplace=True)


mean = X_train.mean()
std = X_train.std()
X_train = (X_train - mean) / std
w = [1.0/len(y_train)]*len(y_train)
mean = X_test.mean()
std = X_test.std()
X_test = (X_test - mean) / std

# Train
train_error = []
training = []
test_error = []
contours = []
testing = []
x_min, x_max = X_test[1].min() - 1, X_test[1].max() + 1
y_min, y_max = X_test[2].min() - 1, X_test[2].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                         np.arange(y_min, y_max, plot_step))
for j in xrange(1,11):
	clf = DecisionTreeClassifier(max_depth=3).fit(X_train, y_train,sample_weight=w)
	# Plot the decision boundary
	Z = clf.predict(X_train)
	error = 0
	for t in xrange(len(Z)):
		if Z[t]!=y_train[t]:
			error += w[t]
	error /= float(sum(w))
	alpha = 1/error - 1
	for t in xrange(len(Z)):
		if Z[t]!=y_train[t]:
			w[t] *= alpha
	alpha = math.log(alpha)
#question 2
	plt.subplot(2, 5, j)
	Z = alpha*clf.predict(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)
	if not len(contours):
		contours.append(Z)
	else:
		Z += contours[-1]
		contours[-1] = Z
	Z = np.sign(Z)
	cs = plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
	plt.axis("tight")
	for i, color in zip(range(n_classes), plot_colors):
		clas = 0
		if not i:
			clas = -1
		else:
			clas = 1
		idx = np.where(y_train == clas)
		print max(w)
		plt.scatter(X_train[1].iloc[idx], X_train[2].iloc[idx], c=color, label=i, s = w, marker='+')
	plt.axis("tight")
#question 3
	# V = alpha*clf.predict(X_train)
	# if not len(training):
	# 	training.append(V)
	# else:
	# 	V += training[-1]
	# 	training[-1] = V
	# V = np.sign(V)
	# error = 0
	# for t in xrange(len(V)):
	# 	if V[t]!=y_train[t]:
	# 		error += 1
	# error /= float(len(V))
	# train_error.append(error)

	# V = alpha*clf.predict(X_test)
	# if not len(testing):
	# 	testing.append(V)
	# else:
	# 	V += testing[-1]
	# 	testing[-1] = V
	# V = np.sign(V)
	# error = 0
	# for t in xrange(len(V)):
	# 	if V[t]!=y_test[t]:
	# 		error += 1
	# error /= float(len(V))
	# test_error.append(error)
# plt.plot(xrange(1,11), train_error,'b')
# plt.plot(xrange(1,11), test_error,'y')
# plt.title("training and testing of AdaBoost")
# plt.legend(['train_error','test_error'], loc='upper left')
plt.suptitle("AdaBoost training procedure for different numbers of rounds")
# plt.legend(['test_error'], loc='upper left')
# plt.xlabel('min_samples_split of a tree')
# plt.ylim([0.11,0.13])
plt.show()