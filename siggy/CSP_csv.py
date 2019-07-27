import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from scipy.signal import butter, lfilter
from glob import glob
from random import sample

def CSP(X, X_labels):
#Toggling the part about centering can speed up code at slight cost of accuracy, O(cN^2) -> close to being the same as straight matrix mult
#Could practically speed up by saving compressed, stupidly large (300,000 by 300,000) id and matrix of ones and indexing necessary size?
############################################################################### 
#    num_sample_points = X.shape[1]
#    #Center the mean to zero and scale bandpass-filtered signal
#    #X = 1 / sqrt(T) * X * (Id - matrix_of_ones)
#  
#    centered_scaled_eeg_data = np.zeros(X.shape)
#    for channel in range(X.shape[0]):
#        for i in range(num_sample_points):
#            temp = np.zeros(num_sample_points) - np.ones(num_sample_points)
#            temp[i] += 1
#            centered_scaled_eeg_data[channel, i] = np.dot(X[channel, :], temp.T)
#    
#    centered_scaled_eeg_data = centered_scaled_eeg_data / np.sqrt(num_sample_points)
    centered_scaled_eeg_data = X

###############################################################################
    
    #Seperate data based on labels               
    seperate_labels = {'Rest': [], 'Left': [], 'Right': []}
    latest_start = 0
    for i in range(len(X_labels)):
        if X_labels[i] != X_labels[i-1]:
            seperate_labels[X_labels[i-1]].extend([j for j in range(latest_start, i)])
            latest_start = i
    
    seperate_labels[X_labels[i]].extend([j for j in range(latest_start, len(X_labels))])

    left_samples = np.matrix(centered_scaled_eeg_data[:, seperate_labels['Left']])
    right_samples = np.matrix(centered_scaled_eeg_data[:, seperate_labels['Right']])

    #Calculate left/right covariance matrices
    left_covariance = (left_samples * left_samples.T) / left_samples.shape[1]
    right_covariance = (right_samples * right_samples.T) / right_samples.shape[1]
    
    #Solve generalized eigenvalue problem with left/right covariance matricese
    return eigh(left_covariance, left_covariance + right_covariance, lower=False, check_finite=False)
    
if __name__ == "__main__":  
    #Constants
    fs = 250            #BCI sampling rate
    low = 7             #Bandpass filter lowcut frequency
    high = 30           #Bandpass filter highcut frequency
    order = 5           #Bandpass filter order
    files = sorted(glob('../data/18-07-19/*.csv'))      #Search directory for csv data files
    fname = files[0]                                    #Choose a file
    
    #Load data and labels
    raw_eeg_data = np.genfromtxt(fname, delimiter=',', skip_header=1, usecols=[1,2,7,8]).T
    labels = np.genfromtxt(fname, delimiter=',', skip_header=1, usecols=[9], dtype="|U5")
    
    #Bandpass filter
    nyq = 0.5 * fs
    b, a = butter(order, [low / nyq, high / nyq], btype='band')
    filtered_eeg_data = lfilter(b, a, raw_eeg_data)
    
    CSP_values, CSP_filters = CSP(filtered_eeg_data, labels)

    print('*****CSP Eigenvalues*****')
    print(CSP_values)
    print('*****CSP Eigenvectors*****')
    print(CSP_filters)
    
#The rest is data visualization, technically you can tell how well they're seperated from CSP_values
#Ideally CSP_values[0] is really close to 0, CSP_values[1] is kind of close, CSP_values[2] is kind of close to 1, CSP_values[3] is really close
    
#Scatter point graphs of bandpass-filtered and CSP-filtered eeg data with sibling channels paired together
###############################################################################
#    #Apply CSP    
#    CSP_filtered_data = CSP_filters.T * np.matrix(filtered_eeg_data)
##    plot_indices = sample([i for i in range(filtered_eeg_data.shape[1])], 100) #Plotting random samples for less clutter
#    plt.figure()
#    
#    plt.subplot(411)
#    plt.title('Bandpass Filtered EEG Data Channels 1 and 4')
#    plt.xlabel('Channel 1')
#    plt.ylabel('Channel 4')
#    plt.plot(filtered_eeg_data[0], filtered_eeg_data[3], 'ro')
#    
#    plt.subplot(412)
#    plt.title('Bandpass Filtered EEG Data Channels 2 and 3')
#    plt.xlabel('Channel 2')
#    plt.ylabel('Channel 3')
#    plt.plot(filtered_eeg_data[1], filtered_eeg_data[2], 'ro')
#
#    plt.subplot(413)
#    plt.title('CSP Filtered Data Channels 1 and 4')
#    plt.xlabel('Channel 1')
#    plt.ylabel('Channel 4')
#    plt.plot(np.array(CSP_filtered_data[0]), np.array(CSP_filtered_data[3]), 'ro')
#    
#    plt.subplot(414)
#    plt.title('CSP Filtered Data Channels 2 and 3')
#    plt.xlabel('Channel 2')
#    plt.ylabel('Channel 3')
#    plt.plot(np.array(CSP_filtered_data[1]), np.array(CSP_filtered_data[2]), 'ro')
#    
#    plt.tight_layout()
#    plt.show()

#Line graphs of seperate bandpass-filtered eeg data and CSP-filtered eeg data
###############################################################################
#    CSP_filtered_data = CSP_filters.T * np.matrix(filtered_eeg_data)
#    plt.figure()
#    
#    plt.subplot(421)
#    plt.title('Filtered EEG Data Channel 1')
#    plt.plot(filtered_eeg_data[0])
#    
#    plt.subplot(422)
#    plt.title('CSP EEG Data Channel 1')
#    plt.plot(CSP_filtered_data[0])
#    
#    plt.subplot(423)
#    plt.title('Filtered EEG Data Channel 2')
#    plt.plot(filtered_eeg_data[1])
#   
#    plt.subplot(424)
#    plt.title('CSP EEG Data Channel 2')
#    plt.plot(CSP_filtered_data[1])
#   
#    plt.subplot(425)
#    plt.title('Filtered EEG Data Channel 3')
#    plt.plot(filtered_eeg_data[2])
#   
#    plt.subplot(426)
#    plt.title('CSP EEG Data Channel 3')
#    plt.plot(CSP_filtered_data[2])
#   
#    plt.subplot(427)
#    plt.title('Filtered EEG Data Channel 4')
#    plt.plot(filtered_eeg_data[3])
#   
#    plt.subplot(428)
#    plt.title('CSP EEG Data Channel 4')
#    plt.plot(CSP_filtered_data[3])
#   
#    plt.tight_layout()
#    plt.show()
