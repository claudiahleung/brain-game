import matplotlib.pyplot as plt
import numpy as np

pearsonr_table = np.genfromtxt("pearsonr.csv", delimiter=",")
euclidean_table = np.genfromtxt("euclidean_dist.csv", delimiter=",")

fig, ax = plt.subplots()
im = ax.imshow(pearsonr_table)

plt.imshow(pearsonr_table)
plt.colorbar()

labels = ["005", "006", "007", "008", "009", "010", "011", "001b", "012"]

ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))

ax.set_xticklabels(labels)
ax.set_yticklabels(labels)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(labels)):
	for j in range(len(labels)):
		text = ax.text(j, i, str(pearsonr_table[i, j])[:4], ha="center", va="center", color="w")

ax.set_title("Pearson R Correlations of Raw BCI Data")

# print(pearsonr_table)

# plt.imshow(pearsonr_table)
plt.savefig("pearsonr_table.png", dpi=500)
plt.close()




fig, ax = plt.subplots()
im = ax.imshow(euclidean_table)

plt.imshow(euclidean_table)
plt.colorbar()

labels = ["005", "006", "007", "008", "009", "010", "011", "001b", "012"]

ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))

ax.set_xticklabels(labels)
ax.set_yticklabels(labels)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(labels)):
	for j in range(len(labels)):
		text = ax.text(j, i, str(euclidean_table[i, j])[:4], ha="center", va="center", color="w")

ax.set_title("Euclidean Distances of Raw BCI Data")

# print(pearsonr_table)

# plt.imshow(pearsonr_table)
plt.savefig("euclidean_table.png", dpi=500)
plt.close()