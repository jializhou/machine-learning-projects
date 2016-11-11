import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import FactorAnalysis as FA
N = 1000
xTrue = np.random.normal(0, 100, N)
yTrue = np.random.normal(0, 100, N)
zTrue = 3 * np.random.normal(0, 100, N)
xData = xTrue 
yData = yTrue 
zData = zTrue 
xData = np.reshape(xData, (N, 1))
yData = np.reshape(yData, (N, 1))
zData = np.reshape(zData, (N, 1))
data = np.hstack((xData, yData,zData))

mu = data.mean(axis=0)
# data = data - mu
data = (data - mu)/data.std(axis=0)  # Uncommenting this reproduces mlab.PCA results
eigenvectors, eigenvalues, V = np.linalg.svd(data.T, full_matrices=False)
projected_data = np.dot(data, eigenvectors)
sigma = projected_data.std(axis=0).mean()
print(eigenvectors)

factor = FA(n_components = 3).fit(data)
print factor.components_

'''
The result is showed as below:
PCA:
[[ 0.72487226  0.07757523  0.68450149]
 [ 0.63248486 -0.46870237 -0.61666927]
 [ 0.27298921  0.87994328 -0.3888145 ]]
 FA:
[[-0.27055423 -0.23179254 -0.07952469]
 [ 0.03080109 -0.08799517  0.15436858]
 [ 0.         -0.         -0.        ]]
'''
