import pandas as pd
import glob
import os

# define variables
pathname = "data/*/*.csv"	
retained_cols=["Time", "Channel 1", "Channel 2", "Channel 7", "Channel 8", "Direction"]

# filepaths
all_csv_absolute_filenames = glob.glob(pathname)
mu_csv_absolute_filenames = [filepath for filepath in all_csv_absolute_filenames \
							if "ssvep" not in filepath]
ssvep_csv_absolute_filenames = [filepath for filepath in all_csv_absolute_filenames \
							if "ssvep" in filepath]

def return_mu_data(pandas_return=False):
	mu_df_list = (pd.read_csv(f, usecols=retained_cols) for f in mu_csv_absolute_filenames)
	concatenated_df = pd.concat(mu_df_list, ignore_index=True)
	if pandas_return:
		return concatenated_df[["Channel 1", "Channel 2", "Channel 7", "Channel 8"]]\
				, concatenated_df[["Direction"]]
	else:
		return concatenated_df[["Channel 1", "Channel 2", "Channel 7", "Channel 8"]].values\
				, concatenated_df[["Direction"]].values

def return_ssvep_data(pandas_return=False):
	mu_df_list = (pd.read_csv(f, usecols=retained_cols) for f in all_csv_absolute_filenames)
	concatenated_df = pd.concat(mu_df_list, ignore_index=True)
	if pandas_return:
		return concatenated_df[["Channel 1", "Channel 2", "Channel 7", "Channel 8"]]\
				, concatenated_df[["Direction"]]
	else:
		return concatenated_df[["Channel 1", "Channel 2", "Channel 7", "Channel 8"]].values\
				, concatenated_df[["Direction"]].values
