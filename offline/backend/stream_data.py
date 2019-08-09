from pyOpenBCI import OpenBCICyton
import requests
import numpy as np
import pandas as pd 

mean_df = pd.Dataframe(columns=['Channel 1', 'Channel 2', 'Channel 7', 'Channel 8'])

dashboard_url = "localhost:5000/data_stream"

def print_raw(sample):
    raw_data = sample.channels_data
    X_ready = np.array([raw_data[0], raw_data[1], raw_data[6], raw_data[7]])
    mean_df = mean_df.append(X_ready)

    if len(mean_df) == 50:
        json_data = mean_df.to_json(orient='split')
        requests.post(dashboard_url, data=json_data)


board = OpenBCICyton(port=None, daisy=False)

instance = board.start_stream(print_raw)