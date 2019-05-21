""" Title: Study
    Purpose: The study class 
    Author: Daniel Backhouse and Alan Yan
"""
# Import extension libraries
import datetime
import os
import sys
import pandas as pd
import compute.find_in_bed_times as find_in_bed_times
import compute.raw_data_editor as raw_data_editor

class Study:
    
    def __init__(self, raw_data_directory, skiprows_rawdata, study_name, 
                 assesment, trim_type, sd_directory):
        
        self.raw_data_directory = raw_data_directory
        self.skiprows_rawdata = skiprows_rawdata
        self.study_name = study_name
        self.assesment = assesment
        
        if(assesment == "Baseline"):
            self.sd_skiprows = 0
        elif(assesment == "Midpoint"):
            self.sd_skiprows = 16
        elif(assesment == "Final"):
            self.sd_skiprows = 0
        else:
            print('Entered an invalid assemsent type: specify either Baseline, Midpoint or Final')
            sys.exit()
        
        print(' Getting raw activity and lux data for participants...')
        self.raw_data = os.listdir(raw_data_directory)
        print('\n Found raw activity and lux data...')
        
        if (trim_type == 0):
            print('\n Getting untrimmed data...')
            dates, times, activity, lux, participants = self.__get_untrimmed_data()
        elif (trim_type == 1):
            print('\n Getting program trimmed data...' )
            dates, times, activity, lux, participants = self.__get_trimmed_data()
        elif (trim_type == 2):
            print('Getting study dates...')
            study_dates, participant_num = self.__get_study_dates(sd_directory)
            print('\n Getting trimmed data based on study dates')
            dates, times, activity, lux, participants = self.__get_study_trimmed_data(
                    study_dates, participant_num)
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
        file = pd.read_excel(sd_directory, sheet_name = None, 
                             skiprows = self.sd_skiprows)
        raw_dates = []
        for sheets in file.values():
            raw_dates.append(list(sheets))
        
        raw_dates.reverse() #Removing the template sheet
        raw_dates.pop()
        raw_dates.reverse()
        
        real_dates = self.__get_study_days(raw_dates)
        
        participant_nums = self.__format_diary_participants(list(file.keys()))
        
        return real_dates, participant_nums
    
    def __format_diary_participants(self, participants):
        """ Formats the diary participants ID's correctly
        
        :param (list) participants: a list of the participant ID's taken from
        the sleep diaries
        """
        participants.reverse()
        participants.pop()
        participants.reverse()
        ID_num = []
        for ID in participants:
            ID_num.append(ID[len(self.study_name)+1:6])
        
        return ID_num
    
    def __get_study_days(self, raw_dates):
        """ Looks at the raw study date files and finds the first and last entry
        these correspond to the start and end of the relevant study days given in
        the diary.
        """
        real_dates = []
        for participant in raw_dates:
            for dates in participant:
                if(isinstance(dates, datetime.datetime )):
                    start_date = dates
                    break
            
            participant.reverse()
            for dates in participant:
                if(isinstance(dates, datetime.datetime )):
                    end_dates = dates
                    break
                
            real_dates.append([start_date, end_dates])
            
        return real_dates
    
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
    
    def __get_study_trimmed_data(self, study_dates, participants_sd):
        """ This function gets the study trimmed data 
        """
        trim_activity = []
        trim_lux = []
        trim_dates = []
        trim_times = []
        participant_id = []
        dates_counter = 0
        for sd_participant in participants_sd:
            for file in self.raw_data:
                if(file.endswith('.csv') and sd_participant == file[3:6]):
                    participant_num = file[3:6]
                    print(participant_num)
                    part_dates = study_dates[dates_counter]
                    start = part_dates[0]
                    end = part_dates[1]
                    dates, times, lux, activity = raw_data_editor.study_trimmed_data(
                                self.raw_data_directory+ '\\'+file, 
                                self.skiprows_rawdata, start, end)
                    
                    trim_activity.append(activity)
                    trim_dates.append(dates)
                    trim_lux.append(lux)
                    trim_times.append(times)
                    participant_id.append(participant_num)
                    
            dates_counter = dates_counter + 1
            
        return trim_dates, trim_times, trim_activity, trim_lux, participant_id
    
    
    
    