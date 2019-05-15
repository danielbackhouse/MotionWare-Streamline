""" Title: Study
    Purpose: The study class 
    Author: Daniel Backhouse and Alan Yan
"""
# Import extension libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import FindInBedTimes
import os
import TrimRawData as trim
############### Note participant list changes to just the diaries that are 
## properly filled once use_sleep_diaries has been called 
class Study:
    
    def __init__(self, raw_data_directory, skiprows_rawdata, study_name, assesment):
        
        self.raw_data_directory = raw_data_directory
        self.skiprows_rawdata = skiprows_rawdata
        self.study_name = study_name
        self.assesment = assesment
        print('Getting raw activity and lux data for participants...')
        self.raw_data = os.listdir(raw_data_directory)
        print('\n Found raw activity and lux data...\n')

    def get_in_bed_times_noDiary(self):
        """Gets the in bed times for when not using sleep diaries
        
        :param: None
        :return: returns 4 lists, the got up times, got up dates, lights out times
        and lights out dates
        :rtype: (list<numpy.datetime64>) (list<numpy.datetime64.time>)
        """
        print('\n Finding got up and lights out time using no sleep diary...')
        window_size = 8
        index = 0
        LOdatetimeList = list()
        GUdatetimeList = list()

        print('\n getting trimmed data...')
        dates, times, activity, lux, participants = self.get_trimmed_data()

        print('\n trimmed data... calculating sleep points...')
        for i in range(0, len(participants)):
            print(participants[i])
            datetime_arr = self.convert_date_time(dates[i], times[i])
            LOdatetime, GUdatetime = FindInBedTimes.find_in_bed_time(
                    datetime_arr, activity[i], lux[i], window_size)
            LOdatetimeList.append(LOdatetime)
            GUdatetimeList.append(GUdatetime)

        
            index = index + 1
    
        return LOdatetimeList, GUdatetimeList 
    #TODO: WRite out docstring
    def convert_date_time(self, dates, times):
        """ Converts date and time arrays (stored as strings) and combines them 
        both to form one datetime array
        """
        datetime_arr = []
        for i  in range(0, len(dates)):
            datetimeString = dates[i] + ' ' + times[i]
            datetime_arr.append(datetime.datetime.strptime(datetimeString, '%Y-%m-%d %I:%M:%S %p'))
            
        return datetime_arr

       
    #TODO: modify this function so that populateRawDataList takes a directory
    #TODO: add docstring
    def get_trimmed_data(self ):
        """This function uses the SheetManager module and gets the raw Data
        excel files pandas data frame an stores each as a seperate entry in     
        a list
        
        :param: none
        :return: Returns a list of raw data files stored in dataframes
        :rtype: (list<pandas dataFrame>)
        """
        trim_activity = []
        trim_lux = []
        trim_dates = []
        trim_times = []
        participant_id = []
        for file in self.raw_data:
                    if file.endswith('.csv'):
                        participant_num = file[3:6]
                        print(participant_num)
                        if int(participant_num) >= 58:
                            skiprows = 15
                            dates, times, lux, activity = trim.trimDataThree(
                                    self.raw_data_directory+ '\\'+file, skiprows)
                        else:
                            dates, times, lux, activity = trim.trimDataThree(
                                    self.raw_data_directory+ '\\'+file, self.skiprows_rawdata)
                    
                        print(dates[0], times[0])
                        print(dates[-1], times[-1])
                        print()
                        trim_activity.append(activity)
                        trim_dates.append(dates)
                        trim_lux.append(lux)
                        trim_times.append(times)
                        participant_id.append(participant_num)
    
        return trim_dates, trim_times, trim_activity, trim_lux , participant_id 
