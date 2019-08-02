from sklearn.preprocessing import Normalizer
from sklearn.externals import joblib
import numpy as np

rf_model_filename = "saved_model"

clf_load = joblib.load(rf_model_filename)

def get_random_forest(input_matrix):
	averaged_input = np.mean(input_matrix, axis=1)
	clf_load.predict(clf_load)
