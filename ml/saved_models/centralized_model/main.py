csvs = [
            ["data/March22_008/10_008-2019-3-22-15-8-55.csv", #008
            "data/March22_008/9_008-2019-3-22-14-59-0.csv",
            "data/March22_008/8_008-2019-3-22-14-45-53.csv",
            ],
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
        ]

import numpy as np    
import pandas as pd
from scipy import interp
from itertools import cycle
from statistics import mean
import matplotlib.pyplot as plt
from sklearn import metrics as sm
from keras.utils import to_categorical
from keras.models import load_model, Sequential
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from cm_clr import plot_classification_report, plot_confusion_matrix
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization

df = []
for i in csvs:
    for csv in i:
        df.append(pd.read_csv(csv))
df = pd.concat(df)

X = np.array(df[['Channel 1', 'Channel 2', 'Channel 7', 'Channel 8']])

channel_1, channel_2, channel_7, channel_8 = [], [], [], []
X_new = []
for i in range(len(X)):
    if i % 50 == 0:
        temp_X = X[i-50:i]
        if temp_X.shape != (0, 4):
            for j in temp_X:
                channel_1.append(j[0]); channel_2.append(j[1])
                channel_7.append(j[2]); channel_8.append(j[3])
            mean1 = mean(channel_1); mean2 = mean(channel_2); mean7 = mean(channel_7); mean8 = mean(channel_8);
            X_new.append([mean1, mean2, mean7, mean8])
pd.DataFrame(X_new).to_csv('data/X_new.csv', index=False, header=False)

y = df[['Direction']]
y['Direction'] = y['Direction'].replace(['Rest'], 0)
y['Direction'] = y['Direction'].replace(['Right'], 1)
y['Direction'] = y['Direction'].replace(['Left'], 2)
y = to_categorical(np.array(y))

X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.2, random_state = 0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train); X_test = sc.transform(X_test)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

classifier = Sequential()

classifier.add(Conv1D(128, X_train.shape[1], activation='relu', input_shape=(X_train.shape[1], 1)))
classifier.add(MaxPooling1D(pool_size = (1), strides=(10)))
classifier.add(Conv1D(64, 1, strides=1, padding='valid', activation="relu", kernel_initializer='glorot_uniform'))
classifier.add(MaxPooling1D(pool_size = (1), strides=(10)))
classifier.add(Conv1D(32, 1, strides=1, padding='valid', activation="relu", kernel_initializer='glorot_uniform'))
classifier.add(MaxPooling1D(pool_size = (1), strides=(10)))

classifier.add(Dropout(0.166))
classifier.add(Flatten())
classifier.add(Dropout(0.166))

classifier.add(Dense(activation="relu", units=256, kernel_initializer="uniform"))
classifier.add(BatchNormalization())
classifier.add(Dense(activation="relu", units=128, kernel_initializer="uniform"))
classifier.add(BatchNormalization())
classifier.add(Dense(activation="relu", units=64, kernel_initializer="uniform"))
classifier.add(BatchNormalization())
classifier.add(Dense(activation="relu", units=32, kernel_initializer="uniform"))
classifier.add(BatchNormalization())
classifier.add(Dense(activation="relu", units=16, kernel_initializer="uniform"))
classifier.add(BatchNormalization())
classifier.add(Dense(activation="relu", units=3, kernel_initializer="uniform"))

classifier.compile(optimizer = "adam", loss = 'categorical_crossentropy', metrics = ['accuracy'])

checkpoint = ModelCheckpoint("model.hdf5", monitor='val_acc', verbose=1, save_weights_only=False, save_best_only=True)
csv_logger = CSVLogger("history.csv", separator=',', append=False)
reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=4, verbose=1, mode='max', min_lr=0.0001)

history = classifier.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size = 10, 
                         callbacks=[checkpoint, csv_logger, reduce_lr], epochs = 25)

model = load_model("model.hdf5")