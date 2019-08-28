import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
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

from scipy.stats import pearsonr
from scipy.spatial.distance import euclidean

np.random.seed(0)

csvs = [
			# ["data/March22_008/10_008-2019-3-22-15-8-55.csv", #008
			# "data/March22_008/9_008-2019-3-22-14-59-0.csv",
			# "data/March22_008/8_008-2019-3-22-14-45-53.csv"
			# ],
			# # ["data/March17/4_RestLeftRight_MI_5s.csv", #005
			# # "data/March17/5_RestLeftRight_MI_10s.csv",
			# # ],
			# ["data/March22_001/1-001-rest20s_left10s_right10s_MI-2019-3-22-16-0-32.csv", #001
			# "data/March22_001/2-001-rest20s_left10s_right10s_MI-2019-3-22-16-12-17.csv",
			# "data/March22_001/3-001-rest20s_left15s_right15s_MI-2019-3-22-16-19-25.csv",
			# "data/March22_001/4-001-rest25s_left15s_right15s_MI-2019-3-22-16-27-44.csv",
			# "data/March22_001/5-001-rest25s_left10s_right10s_MI-2019-3-22-16-35-57.csv",
			# "data/March22_001/7-001-rest25s_left20s_right20s_MI-2019-3-22-16-54-17.csv",
			# ],
			# ["data/March20/time-test-JingMingImagined_10s-2019-3-20-10-28-35.csv",  #009
			# "data/March20/time-test-JingMingImagined_10s-2019-3-20-10-30-26.csv",
			# "data/March20/time-test-JingMingImagined_10s-2019-3-20-10-35-31.csv",
			# "data/March20/time-test-JingMingImagined_10s-2019-3-20-10-57-45.csv",
			# "data/March20/time-test-JingMingImaginedREALLYGOOD-2019-3-20-10-21-44.csv",
			# "data/March20/time-test-JingMingImagined10s-2019-3-20-10-12-1.csv",
			# ],
			# ["data/March24_011/1_011_Rest20LeftRight20_MI-2019-3-24-16-25-41.csv",  #011
			# "data/March24_011/2_011_Rest20LeftRight20_MI-2019-3-24-16-38-10.csv",
			# "data/March24_011/3_011_Rest20LeftRight10_MI-2019-3-24-16-49-23.csv",
			# "data/March24_011/4_011_Rest20LeftRight10_MI-2019-3-24-16-57-8.csv",
			# "data/March24_011/5_011_Rest20LeftRight20_MI-2019-3-24-17-3-17.csv",
			# ],
			# [
			# "data/March29_014/1_014_rest_left_right_20s-2019-3-29-16-44-32.csv",
			# "data/March29_014/2_014_rest_left_right_20s-2019-3-29-16-54-36.csv",
			# "data/March29_014/3_014_AWESOME_rest_left_right_20s-2019-3-29-16-54-36.csv",
			# "data/March29_014/4_014_final_run-2019-3-29-17-38-45.csv",
			# ],

			# SUMMER DATA FROM THIS POINT FORWARD
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


pearsonr_table = []
eucl_dist_table = []

for patient_1, patient_identifier_1 in zip(csvs,["old-008", "old-001", "old-009", "old-011", "old-014", "005", "006", "007", "008", "009", "010", "011", "001b", "012"]):

	row_pearsonr_table = []
	row_eucl_dist_table = []

	for patient_2, patient_identifier_2 in zip(csvs,["old-008", "old-001", "old-009", "old-011", "old-014", "005", "006", "007", "008", "009", "010", "011", "001b", "012"]):

		list_of_dfs_1 = []
		for label in patient_1:
			list_of_dfs_1.append(pd.read_csv(label, usecols=["Time", "Channel 1", "Channel 2", "Channel 7", "Channel 8", "Direction"]))

		master_df_1 = pd.DataFrame()
		for df in list_of_dfs_1:
			master_df_1 = master_df_1.append(df)


		list_of_dfs_2 = []
		for label in patient_2:
			list_of_dfs_2.append(pd.read_csv(label, usecols=["Time", "Channel 1", "Channel 2", "Channel 7", "Channel 8", "Direction"]))

		master_df_2 = pd.DataFrame()
		for df in list_of_dfs_2:
			master_df_2 = master_df_2.append(df)

		classes = ["Left", "Right", "Rest"]


		# master_df_1 = master_df_1.drop(columns=["Time", "Direction"])
		# master_df_2 = master_df_2.drop(columns=["Time", "Direction"])

		patient_1_avgs = []
		patient_2_avgs = []

		for class_ in classes:
			df_patient_1 = master_df_1.loc[master_df_1["Direction"] == class_].drop(columns=["Time", "Direction"]).values
			df_patient_2 = master_df_2.loc[master_df_2["Direction"] == class_].drop(columns=["Time", "Direction"]).values

			patient_1_avgs.append(np.mean(df_patient_1))
			patient_2_avgs.append(np.mean(df_patient_2))

		avg_1 = np.mean(master_df_1.drop(columns=["Time", "Direction"]).values)
		avg_2 = np.mean(master_df_2.drop(columns=["Time", "Direction"]).values)

		pearson_r_value = pearsonr(patient_1_avgs, patient_2_avgs)[0]
		eucl_dist = euclidean(avg_1, avg_2)

		print(pearson_r_value)
		print(eucl_dist)

		row_pearsonr_table.append(pearson_r_value)
		row_eucl_dist_table.append(eucl_dist)

	pearsonr_table.append(row_pearsonr_table)
	eucl_dist_table.append(row_eucl_dist_table)

np.savetxt("pearsonr.csv", np.array(pearsonr_table), delimiter=',', fmt='%s')
np.savetxt("euclidean_dist.csv", np.array(eucl_dist_table), delimiter=',', fmt='%s')