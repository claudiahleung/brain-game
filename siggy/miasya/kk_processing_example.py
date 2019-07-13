import os
from kk_processing_class import Kiral_Korek_Preprocessing

path = r'C:\Users\{YOUR_PATH_HERE}\brain-game\data\11-07-19'

folder_items = os.listdir(path)
files = []
for filename in folder_items:
    if filename.endswith(".txt"):
        files.append(filename)
print(files)


"""
Plot all .txt files in folder of data
"""
for i, data in enumerate(files):
    test = Kiral_Korek_Preprocessing('{0}\{1}'.format(path, files[i]))
    test.load_data_BCI()
    test.initial_preprocessing(bp_lowcut=5, bp_highcut=20, bp_order=2)
    test.plots2() 