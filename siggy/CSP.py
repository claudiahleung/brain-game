import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from scipy.signal import butter, lfilter
from glob import glob
from random import sample

if __name__ == "__main__":
    #Set constants
    files = sorted(glob('../data/11-07-19/*.txt'))  #Search directory for txt data files
    fname = files[0]                                #Choose a file
    fs = 250                                        #BCI sampling rate
    low = 1                                         #Bandpass filter lowcut frequency
    high = 70                                       #Bandpass filter highcut frequency
    order = 5                                       #Bandpass filter order
    task_s = 20                                     #Length (in seconds) of each task (left, right, rest) of trial
    rest, l, r = 2, 0, 1                            #Zero-indexed order that tasks are performed in

    #Load raw EEG data
    raw_eeg_data = np.loadtxt(fname, delimiter=', ', skiprows=7, usecols=[1,2,7,8], dtype='float64').T
    num_sample_points = raw_eeg_data.shape[1]
    samples_per_task = task_s * fs
    samples_per_task_set = 3 * samples_per_task
    num_full_trials = num_sample_points // samples_per_task_set
    
    #Bandpass filter
    nyq = 0.5 * fs
    b, a = butter(order, [low / nyq, high / nyq], btype='band')
    filtered_eeg_data = lfilter(b, a, raw_eeg_data)

#Toggling the part about centering can speed up code at slight cost of accuracy
############################################################################### 
    
    #Center the mean to zero and scale bandpass-filtered signal
    #X = 1 / sqrt(T) * X * (Id - matrix_of_ones)
    
    centered_scaled_eeg_data = np.zeros(filtered_eeg_data.shape)
    for channel in range(filtered_eeg_data.shape[0]):
        for i in range(num_sample_points):
            temp = np.zeros(num_sample_points) - np.ones(num_sample_points)
            temp[i] += 1
            centered_scaled_eeg_data[channel, i] = np.dot(filtered_eeg_data[channel, :], temp.T)
    
    centered_scaled_eeg_data = centered_scaled_eeg_data / np.sqrt(num_sample_points)
    
    #Seperate left/right sample points
    select_data_index = 3 * fs * task_s * num_full_trials
#    selected_data = filtered_eeg_data[:,:select_data_index]
    selected_data = centered_scaled_eeg_data[:, :select_data_index]

###############################################################################

    rest_indices = []
    left_indices = []
    right_indices = []

    for i in range(select_data_index):
        if rest == 0:
            if i % samples_per_task_set < samples_per_task:
                rest_indices.append(i)
        elif rest == 1:
            if i % samples_per_task_set >= samples_per_task and i % samples_per_task_set < 2 * samples_per_task:
                rest_indices.append(i)
        else:
            if i % samples_per_task_set >= 2 * samples_per_task:
                rest_indices.append(i)

    for i in range(select_data_index):
        if l == 0:
            if i % samples_per_task_set < samples_per_task:
                left_indices.append(i)
        elif l == 1:
            if i % samples_per_task_set >= samples_per_task and i % samples_per_task_set < 2 * samples_per_task:
                left_indices.append(i)
        else:
            if i % samples_per_task_set >= 2 * samples_per_task:
                left_indices.append(i)
                
    for i in range(select_data_index):
        if r == 0:
            if i % samples_per_task_set < samples_per_task:
                right_indices.append(i)
        elif r == 1:
            if i % samples_per_task_set >= samples_per_task and i % samples_per_task_set < 2 * samples_per_task:
                right_indices.append(i)
        else:
            if i % samples_per_task_set >= 2 * samples_per_task:
                right_indices.append(i)

    left_samples = np.matrix(selected_data[:, left_indices])
    right_samples = np.matrix(selected_data[:, right_indices])

    #Calculate left/right covariance matrices
    left_covariance = (left_samples * left_samples.T) / left_samples.shape[1]
    right_covariance = (right_samples * right_samples.T) / right_samples.shape[1]

    #Solve generalized eigenvalue problem with left/right covariance matricese
    CSP_values, CSP_filters = eigh(left_covariance, left_covariance + right_covariance, lower=False, check_finite=False)
    print('*****CSP Eigenvalues*****')
    print(CSP_values)
    print('*****CSP Eigenvectors*****')
    print(CSP_filters)
    
#The rest is data visualization, technically you can tell how well they're seperated from CSP_values
#Ideally CSP_values[0] is really close to 0, CSP_values[1] is kind of close, CSP_values[2] is kind of close to 1, CSP_values[3] is really close
    
#Scatter point graphs of bandpass-filtered and CSP-filtered eeg data with sibling channels paired together
###############################################################################
    #Apply CSP 
#    CSP_filtered_data = CSP_filters.T * np.matrix(filtered_eeg_data)
#    plot_indices = sample([i for i in range(num_sample_points)], 100) #Plotting random samples for less clutter
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
