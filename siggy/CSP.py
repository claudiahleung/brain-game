import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from scipy.signal import butter, lfilter
from glob import glob
from os import mkdir
from os.path import join
from warnings import filterwarnings
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def CSP(X, X_labels):
    '''
    Aplpies a multi-class variation of the CSP algorithm to an eeg dataset

    X - Bandpass filtered dataset
    X_labels - label (left, right, or rest) which corresponds to each data point
    '''

    #Toggling the part about centering can speed up code at slight cost of accuracy, O(cN^2) -> close to being the same as straight matrix mult
    #Could practically speed up by saving compressed, stupidly large (300,000 by 300,000) id and matrix of ones and indexing necessary size?
    ############################################################################### 
    num_sample_points = X.shape[1]
    #Center the mean to zero and scale bandpass-filtered signal
    #X = 1 / sqrt(T) * X * (Id - matrix_of_ones)
  
    centered_scaled_eeg_data = np.zeros(X.shape)
    for channel in range(X.shape[0]):
        for i in range(num_sample_points):
            temp = np.zeros(num_sample_points) - np.ones(num_sample_points)
            temp[i] += 1
            centered_scaled_eeg_data[channel, i] = np.dot(X[channel, :], temp.T)
    
    centered_scaled_eeg_data = centered_scaled_eeg_data / np.sqrt(num_sample_points)
    centered_scaled_eeg_data = X

    ###############################################################################
    
    #Seperate data based on labels               
    seperate_labels = {'Rest': [], 'Left': [], 'Right': []}
    latest_start = 0
    i = 0
    while i < len(X_labels) - 1:
        if X_labels[i] != X_labels[i-1]:
            seperate_labels[X_labels[i-1]].extend([j for j in range(latest_start, i)])
            latest_start = i
        i += 1        
    
    seperate_labels[X_labels[i]].extend([j for j in range(latest_start, len(X_labels))])

    rest_samples = np.matrix(centered_scaled_eeg_data[:, seperate_labels['Rest']])
    left_samples = np.matrix(centered_scaled_eeg_data[:, seperate_labels['Left']])
    right_samples = np.matrix(centered_scaled_eeg_data[:, seperate_labels['Right']])

    #Calculate left/right covariance matrices
    rest_covariance = (rest_samples * rest_samples.T) / rest_samples.shape[1]
    left_covariance = (left_samples * left_samples.T) / left_samples.shape[1]
    right_covariance = (right_samples * right_samples.T) / right_samples.shape[1]
    
    #Solve generalized eigenvalue problem with left/right covariance matricese
    return [eigh(left_covariance, left_covariance + rest_covariance, lower=False, check_finite=False), 
            eigh(right_covariance, right_covariance + rest_covariance, lower=False, check_finite=False), 
            eigh(left_covariance, left_covariance + right_covariance, lower=False, check_finite=False)]

def process(files, graph=False, save=False, img_root='./images/'):
    '''
    Processes eeg data files by applying multi-class CSP algorithm and either outputting or saving results

    files - Path to data file to be processed. If files is a list of file paths, process every file. Otherwise process a single file.
    graph - Option to graph the results of the CSP algorithm applied to bandpass filtered data from files. If "save" is False, then the graphs are displayed to screen, if "save" is True, then the graphs are saved to directories named after their acquisition date in root image directory.
    save - Option to save the eigenvalues to a file called "results.txt" in current directory.
    img_root - Destination to save graphs if "graph" and "save" are True
    '''

    def process_file(f, graph, save, img_root):
        '''
        Helper function that processes a single eeg data file
        '''
        #Get constants
        global fs, low, high, order
    
        #Load data and labels
        raw_eeg_data = np.genfromtxt(f, delimiter=',', skip_header=1, usecols=[1,2,7,8]).T
        labels = np.genfromtxt(f, delimiter=',', skip_header=1, usecols=[9], dtype="|U5")

        #Bandpass filter
        nyq = 0.5 * fs
        b, a = butter(order, [low / nyq, high / nyq], btype='band')
        bandpass_eeg_data = lfilter(b, a, raw_eeg_data)

        #Get eigenvalues and eigenvectors for left-rest, right-rest, and left-right
        lrest, rrest, lr = CSP(bandpass_eeg_data, labels)

        if save:
            #Save resulting eigenvalues
            with open('./results.txt', 'a+') as out:
                out.write(f + '\n')
                out.write('Left-Rest:' + str(lrest[0]) + '\n')
                out.write('Right-Rest:' + str(rrest[0]) + '\n')
                out.write('Left-Right:' + str(lr[0]) + '\n')

#                #Uncomment these to save actual eigenvectors - they don't give any information though
#                out.write('*****CSP Eigenvectors*****\n')
#                out.write('*****Left-Rest*****\n')
#                out.write(lrest[1] + '\n')
#                out.write('*****Right-Rest*****\n')
#                out.write(rrest[1] + '\n')
#                out.write('*****Left-Right*****\n')
#                out.write(lr[1] + '\n')

            if graph:
                filepath = f.split('/')

                #Save plots by date of data acquisition
                d = filepath[-2]
                fname = filepath[-1][:-4]
    
                #Make the directory if it doesn't exist
                try:
                    mkdir(join(img_root, d))
                except FileExistsError:
                    pass

                #Apply CSP filters and save the plot of CSP-filtered eeg data, bandpass-filtered eeg data
                #left-rest
                scatter_plot(1, bandpass_eeg_data, np.array(lrest[1].T * np.matrix(bandpass_eeg_data)))
                plt.savefig(join(img_root, d, 'plot-1-' + fname), bbox_inches='tight')
    
                #right-rest
                scatter_plot(2, bandpass_eeg_data, np.array(rrest[1].T * np.matrix(bandpass_eeg_data)))
                plt.savefig(join(img_root, d, 'plot-2-' + fname), bbox_inches='tight')
    
                #left-right
                scatter_plot(3, bandpass_eeg_data, np.array(lr[1].T * np.matrix(bandpass_eeg_data)))
                plt.savefig(join(img_root, d, 'plot-3-' + fname), bbox_inches='tight')
        else:
            #If not saving the results, print them
            print(f)
            print('*****CSP Eigenvalues*****')
            print('Left-Rest:', lrest[0])
            print('Right-Rest:', rrest[0])
            print('Left-Right:', lr[0])

            def classifier(W, X):
                a = 0.5
                b = 0

                return np.sign( a * np.log( np.var( W * X ) ) + b)

            correct_votes = 0
            incorrect_votes = 0
            for i in range(bandpass_eeg_data.shape[1] // 250):
                classify_data = np.matrix(bandpass_eeg_data[:, 250 * i : 250 * (i + 1)])
                correct_label = labels[250 * i + 125]
    
                votes = [0, 0, 0]
                l = ['Rest', 'Left', 'Right']

                if classifier(np.matrix(lrest[1]), classify_data) > 0:
                    votes[0] += 1
                else:
                    votes[1] += 1

                if classifier(np.matrix(rrest[1]), classify_data) > 0:
                    votes[0] += 1
                else:
                    votes[1] += 1

                if classifier(np.matrix(lr[1]), classify_data) > 0:
                    votes[2] += 1
                else:
                    votes[1] += 1

                if l[np.argmax(votes)] == correct_label:
                    correct_votes += 1
                else:
                    incorrect_votes += 1

            print(correct_votes, incorrect_votes)
            print(correct_votes / (correct_votes + incorrect_votes), incorrect_votes / (correct_votes + incorrect_votes))


#            #Uncomment these to print actual eigenvectors - they don't give any information though
#            print('*****CSP Eigenvectors*****')
#            print('*****Left-Rest*****')
#            print(lrest[1])
#            print('*****Right-Rest*****')
#            print(rrest[1])
#            print('*****Left-Right*****')
#            print(lr[1])

            #Apply CSP filters and graph the plot of CSP-filtered eeg data, bandpass-filtered eeg data
            if graph:
                scatter_plot(1, bandpass_eeg_data, np.array(lrest[1].T * np.matrix(bandpass_eeg_data)))
                scatter_plot(2, bandpass_eeg_data, np.array(rrest[1].T * np.matrix(bandpass_eeg_data)))
                scatter_plot(3, bandpass_eeg_data, np.array(lr[1].T * np.matrix(bandpass_eeg_data)))
                plt.show()

    #Check whether arugment is a list of files or a single file
    if type(files) == type(list()):
        #Process every file
        for f in files:
            process_file(f, graph, save, img_root)
    else:
        #Only have to process a one file
        process_file(files, graph, save, img_root)

def scatter_plot(plt_num, first, second):
    '''
    Creates a scatter point plot figure with 4 subplots

    plt_num - number of figure to be created 
    first - first dataset to plot, is plotted in the first two subplots
    second - second dataset to plot, is plotted in the second two subplots
    '''
    plt.figure(plt_num)

    plt.subplot(411)
    plt.title('Bandpass Filtered EEG Data Channels 1 and 8')
    plt.xlabel('Channel 1')
    plt.ylabel('Channel 8')
    plt.plot(first[0], first[3], 'ro')
 
    plt.subplot(412)
    plt.title('Bandpass Filtered EEG Data Channels 2 and 7')
    plt.xlabel('Channel 2')
    plt.ylabel('Channel 7')
    plt.plot(first[1], first[2], 'ro')
 
    plt.subplot(413)
    plt.title('CSP Filtered Data Channels 1 and 8')
    plt.xlabel('Channel 1')
    plt.ylabel('Channel 8')
    plt.plot(second[0], second[3], 'ro')
 
    plt.subplot(414)
    plt.title('CSP Filtered Data Channels 2 and 7')
    plt.xlabel('Channel 2')
    plt.ylabel('Channel 7')
    plt.plot(second[1], second[2], 'ro')
 
    plt.tight_layout()

if __name__ == "__main__":  
    filterwarnings("ignore")

    #Constants
    fs = 250                                            #BCI sampling rate
    low = 7                                             #Bandpass filter lowcut frequency
    high = 30                                           #Bandpass filter highcut frequency
    order = 5                                           #Bandpass filter order
    
#    directories = sorted(glob('../data/*'))
    files = sorted(glob('../data/2019-08-19/*mu*.csv'))
    process(files[0], graph=False, save=False)
