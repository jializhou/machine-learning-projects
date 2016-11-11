import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import FactorAnalysis as FA
N = 1000
xTrue = np.linspace(0, 1000, N)
yTrue = 3 * xTrue
zTrue = np.linspace(0,0,N)
xData = xTrue + np.random.normal(0, 100, N)
yData = yTrue + np.random.normal(0, 100, N)
zData = zTrue + np.random.normal(0, 100, N)
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
[[-0.70711894  0.00541726  0.70707387]
 [-0.70708038 -0.011764   -0.70703532]
 [ 0.00448782 -0.99991613  0.01214899]]
 FA:
[[  8.36879668e-01   8.36860611e-01  -3.54151401e-03]
 [  1.60757109e-04  -2.05951290e-04  -2.00205282e-02]
 [  0.00000000e+00  -0.00000000e+00   0.00000000e+00]]
'''
