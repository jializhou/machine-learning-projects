import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# Load data
X_train = pd.read_csv('data/banana_train.csv',header=None)
y_train = X_train[0]
y_train.replace([-1],[0],inplace=True)
X_train.drop(X_train.columns[0], axis=1, inplace=True)


X_test = pd.read_csv('data/banana_test.csv',header=None)
y_test = X_test[0]
y_test.replace([-1],[0],inplace=True)
X_test.drop(X_test.columns[0], axis=1, inplace=True)


mean = X_train.mean()
std = X_train.std()
X_train = (X_train - mean) / std

mean = X_test.mean()
std = X_test.std()
X_test = (X_test - mean) / std


# Train
test_error = []
for j in xrange(2,12):
	clf = DecisionTreeClassifier(max_depth=6,min_samples_leaf=4,min_samples_split=j).fit(X_train, y_train)
	# Plot the decision boundary
	Z = clf.predict(X_test)
	error = 0
	for t in xrange(len(Z)):
		if Z[t]!=y_test[t]:
			error += 1
	print error
	test_error.append(error/float(len(y_test)))
plt.plot(xrange(1,11), test_error,'y')
plt.title("test error of a decision tree")
plt.legend(['test_error'], loc='upper left')
plt.xlabel('min_samples_split of a tree')
plt.ylim([0.11,0.13])
plt.show()