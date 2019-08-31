import os
import csv
import math
import numpy as np    
import pandas as pd
from statistics import mean
from scipy.stats import mode
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import load_model, Sequential
from sklearn.preprocessing import StandardScaler
from outputs import plot_clr, plot_auroc, plot_cm
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization

csvs = [
            ["data/original/March22_008/10_008-2019-3-22-15-8-55.csv", # Subject 1
            "data/original/March22_008/9_008-2019-3-22-14-59-0.csv",
            "data/original/March22_008/8_008-2019-3-22-14-45-53.csv",
            ],
            ["data/original/March22_001/1-001-rest20s_left10s_right10s_MI-2019-3-22-16-0-32.csv", # Subject 2
            "data/original/March22_001/2-001-rest20s_left10s_right10s_MI-2019-3-22-16-12-17.csv",
            "data/original/March22_001/3-001-rest20s_left15s_right15s_MI-2019-3-22-16-19-25.csv",
            "data/original/March22_001/4-001-rest25s_left15s_right15s_MI-2019-3-22-16-27-44.csv",
            "data/original/March22_001/5-001-rest25s_left10s_right10s_MI-2019-3-22-16-35-57.csv",
            "data/original/March22_001/7-001-rest25s_left20s_right20s_MI-2019-3-22-16-54-17.csv",
            ],
            ["data/original/March20/time-test-JingMingImagined_10s-2019-3-20-10-28-35.csv",  # Subject 3
            "data/original/March20/time-test-JingMingImagined_10s-2019-3-20-10-30-26.csv",
            "data/original/March20/time-test-JingMingImagined_10s-2019-3-20-10-35-31.csv",
            "data/original/March20/time-test-JingMingImagined_10s-2019-3-20-10-57-45.csv",
            "data/original/March20/time-test-JingMingImaginedREALLYGOOD-2019-3-20-10-21-44.csv",
            "data/original/March20/time-test-JingMingImagined10s-2019-3-20-10-12-1.csv",
            ],
            ["data/original/March24_011/1_011_Rest20LeftRight20_MI-2019-3-24-16-25-41.csv",  # Subject 4
            "data/original/March24_011/2_011_Rest20LeftRight20_MI-2019-3-24-16-38-10.csv",
            "data/original/March24_011/3_011_Rest20LeftRight10_MI-2019-3-24-16-49-23.csv",
            "data/original/March24_011/4_011_Rest20LeftRight10_MI-2019-3-24-16-57-8.csv",
            "data/original/March24_011/5_011_Rest20LeftRight20_MI-2019-3-24-17-3-17.csv",
            ],
            [
            "data/original/March29_014/1_014_rest_left_right_20s-2019-3-29-16-44-32.csv",  # Subject 5 
            "data/original/March29_014/2_014_rest_left_right_20s-2019-3-29-16-54-36.csv",
            "data/original/March29_014/3_014_AWESOME_rest_left_right_20s-2019-3-29-16-54-36.csv",
            "data/original/March29_014/4_014_final_run-2019-3-29-17-38-45.csv",
            ],
        ]
            
tfl = True 
mtype = "tfl" if tfl else "nor"   

for subject in range(len(csvs)):
    
    """
    
    df = []
    for j in csvs[subject]: df.append(pd.read_csv(j))
    df = pd.concat(df)
    
    X = np.array(df[['Channel 1', 'Channel 2', 'Channel 7', 'Channel 8']])
    
    y = df[['Direction']]
    y['Direction'] = y['Direction'].fillna(0)
    y['Direction'] = y['Direction'].replace(['Rest'], 0)
    y['Direction'] = y['Direction'].replace(['Right'], 1)
    y['Direction'] = y['Direction'].replace(['Left'], 2)
    y = to_categorical(np.array(y))
    
    channel_1, channel_2, channel_7, channel_8 = [], [], [], []
    X_new, y_new = [], []
    for i in range(len(X)):
        if i % 50 == 0:
            temp_X = X[i-50:i]
            temp_y = y[i-50:i]
            if temp_X.shape != (0, 4):
                for j in temp_X:
                    channel_1.append(j[0]); channel_2.append(j[1])
                    channel_7.append(j[2]); channel_8.append(j[3])
                mean1 = mean(channel_1); mean2 = mean(channel_2); mean7 = mean(channel_7); mean8 = mean(channel_8);
                if (math.isnan(mean1) != True and math.isnan(mean2) != True and math.isnan(mean7) != True and math.isnan(mean8) != True):
                    X_new.append([mean1, mean2, mean7, mean8])
                    y_new.append([mode(temp_y)[0][0][0], mode(temp_y)[0][0][1], mode(temp_y)[0][0][2]])
            print(str(i) + "/" + str(len(X)))
            
    data = pd.DataFrame(X_new)
    labels = pd.DataFrame(y_new)
    
    data.to_csv("data/preprocessed/X_sub"+str(subject)+".csv", index=False, header=None)
    labels.to_csv("data/preprocessed/y_sub"+str(subject)+".csv", index=False, header=None)
    
    """
    
    data = pd.read_csv("data/preprocessed/X_sub"+str(subject)+".csv").as_matrix()
    labels = pd.read_csv("data/preprocessed/y_sub"+str(subject)+".csv").as_matrix()
    
    classes = ["Rest", "Left", "Right"]
    
    randomize = np.arange(len(data))
    np.random.shuffle(randomize)
    
    X_train, X_test, y_train, y_test = train_test_split(data[randomize], labels[randomize], test_size = 0.2, random_state = 0)
    
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train); X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = sc.transform(X_test); X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    
    if tfl: classifier = load_model("models/centralized_model.hdf5")
    
    else:
    
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
        classifier.add(Dense(activation="softmax", units=len(classes), kernel_initializer="uniform"))

    classifier.compile(optimizer = "adam", loss = 'categorical_crossentropy', metrics = ['accuracy'])
    
    checkpoint = ModelCheckpoint("models/sub"+str(subject)+"_model_"+mtype+".hdf5", monitor='val_acc', verbose=1, save_weights_only=False, save_best_only=True)
    csv_logger = CSVLogger("models/sub"+str(subject)+"_history_"+mtype+".csv", separator=',', append=False)
    reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=4, verbose=1, mode='max', min_lr=0.0001)
    
    history = classifier.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size = 10, 
                             callbacks=[checkpoint, csv_logger, reduce_lr], epochs = 100)
    
    model = load_model("models/sub"+str(subject)+"_model_"+mtype+".hdf5")
        
    y_pred = model.predict(X_test)
    predictions, actuals = [], []
    for i in range(len(y_pred)): 
        predictions.append(np.where(y_pred[i] == np.max(y_pred[i]))[0][0])
        actuals.append(np.where(y_test[i] == np.max(y_test[i]))[0][0])
        
    plot_cm(predictions, actuals, classes, normalize=True, cmap=plt.cm.BuPu, figsz=(7,7), title="Confusion Matrix")
    plt.savefig("outputs/sub"+str(subject)+"_cm_"+mtype+".png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.5); plt.close();
    
    plot_auroc(y_pred, y_test, classes, title = 'Area Under the Reciever Operating Characteristics')
    plt.savefig("outputs/sub"+str(subject)+"_auroc_"+mtype+".png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.5); plt.close();
    
    plot_clr(predictions, actuals, classes, cmap='RdBu', figsz=(30,15), title = 'Classification Report')
    plt.savefig("outputs/sub"+str(subject)+"_clr_"+mtype+".png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.25); plt.close();
    
    fig = plt.figure(figsize=(9, 10))
    
    import sklearn.metrics as sm
    acc = str(round(sm.accuracy_score(predictions, actuals)*100, 3)); kappa = str(round(sm.cohen_kappa_score(predictions, actuals), 3))
    fig.suptitle("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + "*** ACCURACY = "+acc+"% | COHEN'S KAPPA = "+kappa+" ***", fontsize=17.5, fontweight="bold")
    #import math, scipy.stats as ss
    #rmse = str(round(math.sqrt(sm.mean_squared_error(predictions, actuals)), 3)); prc = str(round(ss.pearsonr(predictions, actuals), 3))
    #fig.suptitle("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + "*** RMSE = "+rmse+" | PEARSON'S CORRELATION = "+prc+" ***", fontsize=17.5, fontweight="bold")
    
    fig.add_subplot(221); plt.imshow(plt.imread("outputs/sub"+str(subject)+"_cm_"+mtype+".png")); plt.axis('off'); os.remove("outputs/sub"+str(subject)+"_cm_"+mtype+".png")
    fig.add_subplot(222); plt.imshow(plt.imread("outputs/sub"+str(subject)+"_auroc_"+mtype+".png")); plt.axis('off'); os.remove("outputs/sub"+str(subject)+"_auroc_"+mtype+".png")
    fig.add_subplot(212); plt.imshow(plt.imread("outputs/sub"+str(subject)+"_clr_"+mtype+".png")); plt.axis('off'); os.remove("outputs/sub"+str(subject)+"_clr_"+mtype+".png")
    
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    
    plt.savefig("outputs/sub"+str(subject)+"_output_derivations_"+mtype+".png", dpi=700, format='png'); plt.close();