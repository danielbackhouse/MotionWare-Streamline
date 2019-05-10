# -*- coding: utf-8 -*-
"""
Created on Thu May  9 13:04:08 2019
Testing the no sleep diary  program
@author: danie
"""


import pandas as pd
import noSleepDiarySleepWindow

study_period = 14
start_threshold = 20    # starts if less than twenty zeros
activity_sleep_window_threshold = 60 # if there are 60 zeros in a 3 hour period then its a sleep window
light_sleep_window_threshold = 0 # not set yet

rawDataDirectory = r'RAW_DATA_NEW.xlsx'
rawData = pd.read_excel(rawDataDirectory, skiprows = 15)

dates = rawData.iloc[:,0].values
time = rawData.iloc[:,1].values
activity = rawData.iloc[:,2].values
lux = rawData.iloc[:,3].values


#sleep_indices = noSleepDiarySleepWindow.find_in_bed_time(
#        dates, time, activity, lux, study_period, start_threshold, 
#        activity_sleep_window_threshold, light_sleep_window_threshold)

#sortedWeights, sortedIndexIndexRange = noSleepDiarySleepWindow.find_in_bed_time

#days_of_recorded_activity = int(len(activity)/1440)
#start_index = noSleepDiarySleepWindow.find_start_index(time)
#days_indices = noSleepDiarySleepWindow.get_day_indices(start_index, days_of_recorded_activity)

#sleep_indices = noSleepDiarySleepWindow.get_sleep_window_indices(activity, lux, time, 8)
#for index in sleep_indices:
#    print(time[index])

lightsOutTimes, lightsOutIndices = noSleepDiarySleepWindow.find_in_bed_time(dates, time, activity, lux, 8)

#for index in lightsOutIndices:
#    print(dates[index])
#    print(time[index])