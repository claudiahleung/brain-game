from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def train_knn(X_train, y_train, parameters=None):
	clf = KNeighborsClassifier()
	clf.fit(X_train, y_train)
	return clf

def train_random_forest(X_train, y_train, parameters=None):
	clf = RandomForestClassifier(n_estimators=8)
	clf.fit(X_train, y_train)
	return clf

def train_svm(X_train, y_train, parameters=None):
	clf = SVC()
	clf.fit(X_train, y_train)
	return clf
