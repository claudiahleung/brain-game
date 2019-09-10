# sklearn functions
from sklearn.model_selection import train_test_split

# for pickling
from sklearn.externals import joblib

# ml_scripts
import analyze_data
import train_models

# for datetime
from datetime import datetime


# load data
mu_data, mu_labels = analyze_data.return_mu_data()
mu_labels_one_hot = analyze_data.perform_one_hot(mu_labels)

print(mu_data[0])

# split data
mu_X_train, mu_X_test, mu_y_train, mu_y_test = train_test_split(mu_data, mu_labels_one_hot, test_size=0.99)
print("data split!")
print(mu_y_train[0])
print(mu_y_test[0])

# run random forest
clf = train_models.train_random_forest(mu_X_train, mu_y_train)
print("Done training!")
predictions = clf.predict(mu_X_test[:400])
acc_counter = 0
for i in range(len(predictions)):
	print(list(predictions[i]), list(mu_y_test[i]))
	if list(predictions[i]) == list(mu_y_test[i]):
		acc_counter += 1
print(f"acc: {acc_counter/len(predictions)*100} %")
joblib.dump(clf, "random_forest.pkl")