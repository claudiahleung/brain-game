from pyOpenBCI import OpenBCICyton
import requests
import numpy as np
import pandas as pd 

data_list = []

dashboard_url = "localhost:3000/data_stream"

def print_raw(sample):
    global mean_df
    raw_data = sample.channels_data
    X_ready = [raw_data[0], raw_data[1], raw_data[6], raw_data[7]]
    data_list.append(X_ready)
    
    if len(data_list) == 50:
        mean_df = pd.DataFrame(data=data_list, columns=['Channel 1', 'Channel 2', 'Channel 7', 'Channel 8'])
        json_data = mean_df.to_json(orient='split')
        requests.post(dashboard_url, data=json_data)


board = OpenBCICyton(port=None, daisy=False)

instance = board.start_stream(print_raw)
