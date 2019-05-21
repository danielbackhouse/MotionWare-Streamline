""" Title: Study
    Purpose: The study class 
    Author: Daniel Backhouse and Alan Yan
"""
# Import extension libraries
import datetime
import os
import sys
import pandas as pd
import motionwatch.compute.find_in_bed_times as find_in_bed_times
import motionwatch.compute.raw_data_editor as raw_data_editor

class Study:
    
    def __init__(self, raw_data_directory, skiprows_rawdata, study_name, 
                 assesment, trim_type, sd_directory):
        
        self.raw_data_directory = raw_data_directory
        self.skiprows_rawdata = skiprows_rawdata
        self.study_name = study_name
        self.assesment = assesment
        
        print(' Getting raw activity and lux data for participants...')
        self.raw_data = os.listdir(raw_data_directory)
        print('\n Found raw activity and lux data...')
        
        if (trim_type == 0):
            print('\n Getting untrimmed data...')
            dates, times, activity, lux, participants = self.__get_untrimmed_data()
        elif (trim_type == 1):
            print('\n Getting program trimmed data...' )
            dates, times, activity, lux, participant = self.__get_trimmed_data()
        elif (trim_type == 2):
            print('Getting study dates...')
            self.study_dates = self.__get_study_dates(sd_directory)
            print('\n Getting trimmed data based on study dates')
            dates, times, activity, lux, partcipant = self.__get_study_trimmed_data()
        else:
            print('\n Error you entered an invalid trim_type (enter number between 0-2)')
            print('Terminating program...')
            sys.exit()
            
        self.dates = dates
        self.times = times
        self.activity = activity
        self.lux = lux
        self.participant_list = participants

    def get_in_bed_times(self):
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
        SleepInfoList = list()
        
        for i in range(0, len(self.participant_list)):
            print(self.participant_list[i])
            datetime_arr = self.__convert_date_time(self.dates[i], self.times[i])
            LOdatetime, GUdatetime, SleepInfo = find_in_bed_times.find_in_bed_time(
                    datetime_arr, self.activity[i], self.lux[i], window_size)
            LOdatetimeList.append(LOdatetime)
            GUdatetimeList.append(GUdatetime)
            SleepInfoList.append(SleepInfo)
            #TODO fix day analysis here
            #DayDataAnalysis.findDayInfo(participants[i],LOindex, GUindex, activity[i], dates[i], times[i])
        
            index = index + 1
    
        return LOdatetimeList, GUdatetimeList, SleepInfoList, self.participant_list
    
    #TODO: Write out docstring
    def __convert_date_time(self, dates, times):
        """ Converts date and time arrays (stored as strings) and combines them 
        both to form one datetime array
        """
        datetime_arr = []
        for i  in range(0, len(dates)):
            datetimeString = dates[i] + ' ' + times[i]
            datetime_arr.append(datetime.datetime.strptime(datetimeString, '%Y-%m-%d %I:%M:%S %p'))
            
        return datetime_arr
    
    def __get_study_dates(self, sd_directory):
        """ Read the sleep diary file and gets the 
        dates the study was done over for each participant
        """
        file = pd.read_excel(sd_directory, sheet_name = None)
        raw_dates = []
        for sheets in file.values():
            raw_dates.append(list(sheets))
    
    #TODO: fix docstring
    def __get_untrimmed_data(self ):
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
                        #TODO: throw some error if the skiprows is too short
                        dates, times, lux, activity = raw_data_editor.untrimmed_data(
                                self.raw_data_directory+ '\\'+file, self.skiprows_rawdata)
                    
                        trim_activity.append(activity)
                        trim_dates.append(dates)
                        trim_lux.append(lux)
                        trim_times.append(times)
                        participant_id.append(participant_num)
    
        return trim_dates, trim_times, trim_activity, trim_lux , participant_id 
    
    #TODO: fix docstring
    def __get_trimmed_data(self):
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
                        #TODO: throw some error if the skiprows is too short
                        dates, times, lux, activity = raw_data_editor.trimmed_data(
                                self.raw_data_directory+ '\\'+file, self.skiprows_rawdata)
                    
                        trim_activity.append(activity)
                        trim_dates.append(dates)
                        trim_lux.append(lux)
                        trim_times.append(times)
                        participant_id.append(participant_num)
    
        return trim_dates, trim_times, trim_activity, trim_lux , participant_id 
    
    def __get_study_trimmed_data(self):
        """ This function gets the study trimmed data
        """