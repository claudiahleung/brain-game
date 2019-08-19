from sklearn.externals.joblib import load
import numpy as np

overall_normalizer = load("models/overall_normalizer.pkl")
centralized_rf = load("models/saved_model_rf_centralized.pkl")
centralized_knn = load("models/saved_model_knn_centralized.pkl")

def rf_predict(input_data):
	"""Input data can either be [1,1,1,1] (4,) shape, 
	[[1,1,1,1]] (1,4) shape, 
	or (x,4)
	where x is an int > 0"""
	input_data = np.array(input_data)
	if input_data.shape == (4,):
		input_data = input_data.reshape(1,4)
	input_data = np.mean(input_data, axis=0)
	input_data = overall_normalizer.fit_transform([input_data])
	prediction = centralized_rf.predict(input_data)
	str_prediction = None
	if np.argmax(prediction) == 0:
		str_prediction = "left"
	elif np.argmax(prediction) == 1:
		str_prediction = "right"
	else:
		str_prediction = "rest"
	return str_prediction

def knn_predict(input_data):
	"""Input data can either be [1,1,1,1] (4,) shape, 
	[[1,1,1,1]] (1,4) shape, 
	or (x,4)
	where x is an int > 0"""
	input_data = np.array(input_data)
	if input_data.shape == (4,):
		input_data = input_data.reshape(1,4)
	input_data = np.mean(input_data, axis=0)
	input_data = overall_normalizer.fit_transform([input_data])
	prediction = centralized_knn.predict(input_data)
	str_prediction = None
	if np.argmax(prediction) == 0:
		str_prediction = "left"
	elif np.argmax(prediction) == 1:
		str_prediction = "right"
	else:
		str_prediction = "rest"
	return str_prediction