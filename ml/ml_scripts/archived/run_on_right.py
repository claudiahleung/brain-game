import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.utils.class_weight import compute_class_weight

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer

from sklearn.externals import joblib

import numpy as np

from sklearn.metrics import roc_auc_score

from scipy.stats import mode
from collections import Counter

from datetime import datetime

import json


np.random.seed(0)

accuracies_dict = {}
auc_dict = {}

csvs = [
			["data/March22_008/10_008-2019-3-22-15-8-55.csv", #008
			"data/March22_008/9_008-2019-3-22-14-59-0.csv",
			"data/March22_008/8_008-2019-3-22-14-45-53.csv"
			],
			# ["data/March17/4_RestLeftRight_MI_5s.csv", #005
			# "data/March17/5_RestLeftRight_MI_10s.csv",
			# ],
			["data/March22_001/1-001-rest20s_left10s_right10s_MI-2019-3-22-16-0-32.csv", #001
			"data/March22_001/2-001-rest20s_left10s_right10s_MI-2019-3-22-16-12-17.csv",
			"data/March22_001/3-001-rest20s_left15s_right15s_MI-2019-3-22-16-19-25.csv",
			"data/March22_001/4-001-rest25s_left15s_right15s_MI-2019-3-22-16-27-44.csv",
			"data/March22_001/5-001-rest25s_left10s_right10s_MI-2019-3-22-16-35-57.csv",
			"data/March22_001/7-001-rest25s_left20s_right20s_MI-2019-3-22-16-54-17.csv",
			],
			["data/March20/time-test-JingMingImagined_10s-2019-3-20-10-28-35.csv",  #009
			"data/March20/time-test-JingMingImagined_10s-2019-3-20-10-30-26.csv",
			"data/March20/time-test-JingMingImagined_10s-2019-3-20-10-35-31.csv",
			"data/March20/time-test-JingMingImagined_10s-2019-3-20-10-57-45.csv",
			"data/March20/time-test-JingMingImaginedREALLYGOOD-2019-3-20-10-21-44.csv",
			"data/March20/time-test-JingMingImagined10s-2019-3-20-10-12-1.csv",
			],
			["data/March24_011/1_011_Rest20LeftRight20_MI-2019-3-24-16-25-41.csv",  #011
			"data/March24_011/2_011_Rest20LeftRight20_MI-2019-3-24-16-38-10.csv",
			"data/March24_011/3_011_Rest20LeftRight10_MI-2019-3-24-16-49-23.csv",
			"data/March24_011/4_011_Rest20LeftRight10_MI-2019-3-24-16-57-8.csv",
			"data/March24_011/5_011_Rest20LeftRight20_MI-2019-3-24-17-3-17.csv",
			],
			[
			"data/March29_014/1_014_rest_left_right_20s-2019-3-29-16-44-32.csv",
			"data/March29_014/2_014_rest_left_right_20s-2019-3-29-16-54-36.csv",
			"data/March29_014/3_014_AWESOME_rest_left_right_20s-2019-3-29-16-54-36.csv",
			"data/March29_014/4_014_final_run-2019-3-29-17-38-45.csv",
			],
			["C:/Users/laure/Desktop/Work/brain-game/data/16-07-19/005_3(LEFT20s_REST20s_RIGHT20s)Trial1-2019-07-16-18-45-36.csv",
			"C:/Users/laure/Desktop/Work/brain-game/data/16-07-19/005_3(LEFT20s_REST20s_RIGHT20s)Trial2-2019-7-16-19-4-9.csv"
			],
			["C:/Users/laure/Desktop/Work/brain-game/data/16-07-19/006_3(LEFT20s_REST20s_RIGHT20s)Trial1-2019-7-16-19-38-15.csv",
			"C:/Users/laure/Desktop/Work/brain-game/data/16-07-19/006_3(LEFT20s_REST20s_RIGHT20s)Trial2-2019-7-16-19-44-13.csv"],
			
			# MISSING DATA
			# ["C:/Users/laure/Desktop/Work/brain-game/data/11-07-19/001_3LeftRightRest20sTrial2-2019-7-11-19-10-19.csv",
			# "C:/Users/laure/Desktop/Work/brain-game/data/11-07-19/001_3LeftRightRestTrial1_20s-2019-7-11-18-57-27.csv"],
			# ["C:/Users/laure/Desktop/Work/brain-game/data/15-07-19/003_2(REST30s_LEFT30s_RIGHT30s)Trial1-2019-7-15-18-40-58.csv",
			# "C:/Users/laure/Desktop/Work/brain-game/data/15-07-19/003_2(REST30s_LEFT30s_RIGHT30s)Trial2-2019-7-15-18-47-56.csv",
			# "C:/Users/laure/Desktop/Work/brain-game/data/15-07-19/003_2(REST30s_LEFT30s_RIGHT30s)Trial3-2019-7-15-18-56-54.csv",
			# "C:/Users/laure/Desktop/Work/brain-game/data/15-07-19/003_2(REST30s_LEFT60s_RIGHT60s)Trial4-2019-7-15-19-12-8.csv"],
			
			# MISSING DATA
			# ["C:/Users/laure/Desktop/Work/brain-game/data/15-07-19/004_2(REST30s_LEFT60s_RIGHT60s)Trial1-2019-7-15-19-53-9.csv",
			# "C:/Users/laure/Desktop/Work/brain-game/data/15-07-19/004_2(REST30s_LEFT60s_RIGHT60s)Trial2-2019-7-15-20-0-55.csv"],
			
			["C:/Users/laure/Desktop/Work/brain-game/data/16-07-19/007_3(LEFT20s_REST20s_RIGHT20s)Trial2-2019-7-16-20-31-2.csv"],
			["C:/Users/laure/Desktop/Work/brain-game/data/18-07-19/008_trial1-2019-7-18-18-14-20.csv",
			"C:/Users/laure/Desktop/Work/brain-game/data/18-07-19/008_trial2-2019-7-18-18-21-22.csv"],
			["C:/Users/laure/Desktop/Work/brain-game/data/18-07-19/009_trial1-2019-7-18-18-54-0.csv",
			"C:/Users/laure/Desktop/Work/brain-game/data/18-07-19/009_trial2-2019-7-18-19-0-12.csv",
			"C:/Users/laure/Desktop/Work/brain-game/data/18-07-19/009_trial3-2019-7-18-19-5-44.csv"],
			["C:/Users/laure/Desktop/Work/brain-game/data/18-07-19/010_trial1-2019-7-18-19-40-9.csv"],
			["C:/Users/laure/Desktop/Work/brain-game/data/18-07-19/011_trial1-2019-7-18-20-23-16.csv"],
			["C:/Users/laure/Desktop/Work/brain-game/data/19-07-19/001-trial1-2019-7-19-19-16-45.csv",
			"C:/Users/laure/Desktop/Work/brain-game/data/19-07-19/001-trial2-2019-7-19-19-23-24.csv"],
			["C:/Users/laure/Desktop/Work/brain-game/data/19-07-19/012-trial1-2019-7-19-18-29-43.csv",
			"C:/Users/laure/Desktop/Work/brain-game/data/19-07-19/012-trial2-2019-7-19-18-37-28.csv"]
		]

list_of_dfs = []
X_ready = []

# for patient, patient_identifier in zip(csvs,["008", "005", "001", "009", "011", "014"]):

# 	for label in patient:
# 		list_of_dfs.append(pd.read_csv(label, usecols=["Time", "Channel 1", "Channel 2", "Channel 7", "Channel 8", "Direction"]))

# 	master_df = pd.DataFrame()
# 	for df in list_of_dfs:
# 		master_df = master_df.append(df)

# 	X_raw_data = df.drop(columns=["Direction", "Time"]).dropna().values

# 	start = 0
# 	end = start + 255/5



# 	# n_intervals = int((max_time - min_time)/255*5)
# 	# start = min_time
# 	# end = start + 255/5
# 	start = 0
# 	end = start + 255/5

# 	print("EXTREMA")
# 	print(df.max())
# 	print(df.min())
# 	print("ABOVE")

# 	counter = 0
# 	print("MAX MIN")
# 	# print(max_time)
# 	# print(min_time)
# 	print(master_df.head())
# 	print(master_df.shape)
# 	while(end <= master_df.shape[0]):
# 		# selected_rows = df[(df['Time'] >= start) & (df['Time'] <= end)]
# 		selected_rows = master_df.iloc[int(start):int(end)]


# 		c1_mode = np.mean(selected_rows["Channel 1"].values)
# 		c2_mode = np.mean(selected_rows["Channel 2"].values)
# 		c7_mode = np.mean(selected_rows["Channel 7"].values)
# 		c8_mode = np.mean(selected_rows["Channel 8"].values)

# 		X_ready.append(np.array([c1_mode, c2_mode, c7_mode, c8_mode]).reshape(4,))

# 		if counter%1000==0:
# 			print(np.array([c1_mode, c2_mode, c7_mode, c8_mode]).reshape(4,))
# 			print(counter)

# 		counter += 1
# 		start += 255/5
# 		end += 255/5

# norm_scaler = Normalizer()
# norm_scaler.fit_transform(X_ready)
# joblib.dump(norm_scaler, "overall_normalizer.pkl")



print(len(csvs))
print(len(["old-008", "old-001", "old-009", "old-011", "old-014", "005", "006", "007", "008", "009", "010", "011", "001b", 
	"012"]))

for patient, patient_identifier in zip(csvs,["old-008", "old-001", "old-009", "old-011", "old-014", "005", "006", "007", "008", "009", "010", "011", "001b", 
	"012"]):
	list_of_dfs = []


	for label in patient:
		list_of_dfs.append(pd.read_csv(label, usecols=["Time", "Channel 1", "Channel 2", "Channel 7", "Channel 8", "Direction"]))

	for df in list_of_dfs:
		print(df.head())

	X_ready = []
	y_ready = []

	master_df = pd.DataFrame()
	for df in list_of_dfs:
		master_df = master_df.append(df)

	# print(master_df.head())
	y_raw_label = master_df["Direction"].values
	identifiers = ["Left", "Right", "Rest"]

	class_weight = compute_class_weight('balanced', np.unique(y_raw_label), y_raw_label)



	max_time = max(master_df["Time"].values)
	min_time = min(master_df["Time"].values)

	X_raw_data = master_df.drop(columns=["Direction", "Time"]).values

	n_intervals = int((max_time - min_time)/255*5)
	# start = min_time
	# end = start + 255/5
	start = 0
	end = start + 255/5

	# print("EXTREMA")
	# print(df.max())
	# print(df.min())
	# print("ABOVE")

	counter = 0
	# print("MAX MIN")
	# print(max_time)
	# print(min_time)
	while(end <= df.shape[0]):
		# selected_rows = df[(df['Time'] >= start) & (df['Time'] <= end)]
		selected_rows = master_df.iloc[int(start):int(end)]

		most_frequent_label = max(set(selected_rows["Direction"].values), key = list(selected_rows["Direction"].values).count)
		c1_mode = np.mean(selected_rows["Channel 1"].values)
		c2_mode = np.mean(selected_rows["Channel 2"].values)
		c7_mode = np.mean(selected_rows["Channel 7"].values)
		c8_mode = np.mean(selected_rows["Channel 8"].values)

		# c1_mode = np.mean(selected_rows["Channel 1"].values)
		# c2_mode = np.mean(selected_rows["Channel 2"].values)
		# c7_mode = np.mean(selected_rows["Channel 7"].values)
		# c8_mode = np.mean(selected_rows["Channel 8"].values)

		X_ready.append(np.array([c1_mode, c2_mode, c7_mode, c8_mode]).reshape(4,))
		y_ready.append(most_frequent_label)
		start += 255/5
		end += 255/5
		# if counter==0:
			# print(most_frequent_label)
			# print(start, end)
			# print(selected_rows.head())
			# print(counter)
			# print(np.array([c1_mode, c2_mode, c7_mode, c8_mode]).reshape(4,))
		# counter += 1

	# print(counter)

	y_processed_labels = []
	for row in y_ready:
		# print(row)
		temp_row = [0]*len(identifiers)
		temp_row[identifiers.index(row)] = 1
		# print(temp_row)
		y_processed_labels.append(temp_row)


	# see_class_distribution(y_processed_labels)

	print("HEAD")
	print(master_df.head())

	normalizer = joblib.load("overall_normalizer.pkl")
	# norm_scaler = Normalizer()
	X_ready = normalizer.fit_transform(X_ready)
	# joblib.dump(norm_scaler, )

	# scaler = MinMaxScaler(feature_range=(0,1))
	# X_ready = scaler.fit_transform(X_ready)

	# np.savetxt("X_data_"+patient_identifier+".csv", X_ready, delimiter=",", fmt="%s")
	# np.savetxt("y_data_"+patient_identifier+".csv", y_processed_labels, delimiter=",", fmt="%s")

	y_processed_labels = np.array(y_processed_labels)[:,1]


	X_train, X_test, y_train, y_test = train_test_split(X_ready, y_processed_labels, test_size=0.2, random_state=42)

	# print(y_train[:10])

	# print(class_weight)

	clf = RandomForestRegressor()
	clf.fit(X_train, y_train)
	predictions = clf.predict(X_test) 

	acc = 0
	counter = 0
	for pred, y in zip(predictions, y_test):
		if round(pred+0.5) == y:
			counter += 1
		acc += 1

	# acc = clf.score(X_test, y_test)
	# print(acc)

	# print(acc)
	# print(len(y_test))

	print("ACC: "+str(counter/acc*100)+" %")
	# print("AUC: "+str(roc_auc_score(predictions, y_test)))

	# for i in range(20):
		# print(predictions[i], end='\t')
		# print(y_test[i])

	accuracies_dict[patient_identifier] = counter/acc*100
	# auc_dict[patient_identifier] = roc_auc_score(predictions, y_test)

	joblib.dump(clf, "saved_model_rf_right_"+patient_identifier+".pkl")

with open(f"results_acc_rf_right.json", 'w') as f:
	json.dump(accuracies_dict, f)

# with open(f"results_auc_knn_left.json".replace(' ','-'), 'w') as f:
# 	json.dump(auc_dict, f)