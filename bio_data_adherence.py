import numpy as np
import os
import pandas as pd
import warnings 
warnings.filterwarnings('ignore')
import csv

lists_directories = [['data/pre-pilot/fitbit','data/pre-pilot/selfObservation'],['data/pilot/fitbit/control','data/pilot/selfObservation/control'],['data/pilot/fitbit/intervention','data/pilot/selfObservation/intervention']]

for cnt,lst in enumerate(lists_directories):
    print(cnt)
    fitbit_data_dir,self_obs_data_dir = lst

    ext = ('.csv')
    # Read fitbit_data
    fitbit_data_lst = []
    for files in os.listdir(fitbit_data_dir):
        if files.endswith(ext):
            #print(fitbit_data_dir + "/" + files)
            fitbit_data = pd.read_csv(fitbit_data_dir + "/" + files,delimiter=',', dtype=object)
            fitbit_data['pid'] = files[0:-4]
            fitbit_data['pid'] = files[0:-4]
            fitbit_data.rename(columns={'date': 'timestamp'}, inplace=True)
            fitbit_data_lst.append(fitbit_data)

    fitbit_data = pd.concat(fitbit_data_lst, axis=0, ignore_index=True)

    fitbit_data['timestamp'] = pd.to_datetime(fitbit_data['timestamp']).dt.date #Convert columns to their correct type
    fitbit_data = fitbit_data.iloc[: , 1:] # Drop index column

    fitbit_data.head()

    ext = ('.xlsx')
    # Read self_obs_data
    self_obs_data_lst = []
    for files in os.listdir(self_obs_data_dir):
        if files.endswith(ext):
            #print(files)
            self_obs_data = pd.read_excel(self_obs_data_dir + "/" + files)
            self_obs_data['pid'] = files[0:-5]
            self_obs_data = self_obs_data.iloc[:, 1:]
            #print(self_obs_data)
            self_obs_data_lst.append(self_obs_data)

    #print(self_obs_data_lst)
    #print(len(self_obs_data_lst))
    self_obs_data = pd.concat(self_obs_data_lst, axis=0, ignore_index=True)

    for i in ['target',"weight","home","junk"]:
      self_obs_data[i] = self_obs_data[i].astype(str).str.replace(',','.')
      self_obs_data[i] = self_obs_data[i].astype(str).str.replace('<','')
      self_obs_data[i] = self_obs_data[i].astype(str).str.replace('Ο','0')
      self_obs_data[i] = self_obs_data[i].astype(str).str.replace(' ','')
      self_obs_data[i] = self_obs_data[i].replace('nan',np.nan)
      self_obs_data[i] = self_obs_data[i].replace('-',np.nan)

    remap = {'Ναι': 1, 'Όχι': 0, ' ':np.nan}
    self_obs_data['target'] = self_obs_data['target'].map(remap)
    self_obs_data['home'] = self_obs_data["home"].map(remap)
    self_obs_data['junk'] = self_obs_data["junk"].map(remap)
    self_obs_data['timestamp'] = pd.to_datetime(self_obs_data['timestamp']).dt.date

    self_obs_data.head()

    """### Fitbit adherence"""

    all_columns = ["patientID","start_date","end_date"] + list(fitbit_data.columns)
    pids = list(fitbit_data["pid"].unique())

    # open the file in the write mode
    if (cnt == 0):
        fileName = 'fitbit_adherence_prepilot.csv'
    elif (cnt == 1):
        fileName = 'fitbit_adherence_pilot_control.csv'
    elif (cnt == 2):
        fileName = 'fitbit_adherence_pilot_intervention.csv'

    # create the csv writer
    with open(fileName, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(all_columns)

        for pid in pids:
          temp = fitbit_data.loc[fitbit_data['pid'] == pid]
          length = len(temp)

          writer.writerow(row_list)

    """### Self-observation adherence"""

    all_columns = ["patientID","start_date","end_date"] + list(self_obs_data.columns)
    pids = list(self_obs_data["pid"].unique())

    # open the file in the write mode
    if (cnt == 0):
        fileName = 'selfObs_adherence_prepilot.csv'
    elif (cnt == 1):
        fileName = 'selfObs_adherence_pilot_control.csv'
    elif (cnt == 2):
        fileName = 'selfObs_adherence_pilot_intervention.csv'

    # create the csv writer
    with open(fileName, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(all_columns)

        for pid in pids:
          temp = self_obs_data.loc[self_obs_data['pid'] == pid]
          row_list = [pid,temp.timestamp.min(),temp.timestamp.max()]
          length = len(temp)
          for column in temp.columns:
            row_list.append(str(length - temp[column].isna().sum()))

          writer.writerow(row_list)

        # close the file