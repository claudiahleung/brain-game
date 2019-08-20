from sklearn.externals import joblib
import os
import pandas as pd


clf = joblib.load("../../ml/saved_knn/saved_model_knn_001.pkl")
print(clf)

data_dir = "../../data/11-07-19/demo"

final_df = pd.DataFrame()

for subject_file in os.listdir(data_dir):
    file_dir = os.path.join(data_dir, subject_file)
    data_df = pd.read_csv(file_dir)

    final_df = final_df.append(data_df)

print(final_df)
#prediction = clf.predict() # preprocessed data from headset