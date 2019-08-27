from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D


import matplotlib.pyplot as plt  

import pandas as pd 

fig = plt.figure(1, figsize=(4, 3))


ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)


X = pd.read_csv("X_data001.csv").values
y = pd.read_csv("y_data001.csv").values 

new_y = []
for row in y:
	new_y.append(list(row).index(1))


pca = PCA(n_components=2)
pca.fit(X)
X_tr = pca.fit_transform(X)

ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap=plt.cm.nipy_spectral)

plt.savefig("pca_results.png")