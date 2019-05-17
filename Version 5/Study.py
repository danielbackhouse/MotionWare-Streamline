# Class: Study
# Author: Daniel Backhouse and Alan Yan
#TODO: create seperate class for sleep analysis study
# Import extension libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import FindInBedTimes
import os
import TrimRawData as trim

class Study:
    """ The Study class defines a sleep study object
    
    fields:
        THOSE SPECIFIED BY USER
        - raw_data_directory: 
            The directory containing the raw data CSV files formatted as:
                Col0: Date
                Col1: Time
                Col2: Activity
                Col3: Lux
            With data begining by at least the 20th row
        - skiprows_rawdata:
            The number of rows that the relevant data starts on. This can be 
            within the actual data so long as is is not before. 
        - study_name:
            The abbreviated name of the study "BT" or "FACT". Would be the starting
            entry in the participant ID. For example in "RVCI-001" it would be 
            "RVCI"
        - assesment:
            The assesment type (baseline, midpoint, 6 month, final... etc...)
            
        THOSE SPECFIED WITHIN CLASS
        - All the information required to read the sleep analysis files.
        - This should ONLY be used to compute errors and compute subsequent 
        weight optimization.         
    """
    def __init__(self, raw_data_directory, skiprows_rawdata, study_name, assesment):
        
        self.sleep_analysis_directory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Analysis 2019-03-19.xlsx'
        self.lights_out_index_analysis = 2
        self.got_up_index_analysis = 5
        self.skiprows_analysis = 16
        
        self.raw_data_directory = raw_data_directory
        self.skiprows_rawdata = skiprows_rawdata
        self.study_name = study_name
        self.assesment = assesment
        print('Getting raw activity and lux data for participants...')
        self.raw_data = os.listdir(raw_data_directory)
        print('\n Found raw activity and lux data...\n')

    def get_in_bed_times(self):
        """Gets the in bed times for when not using sleep diaries
        
        FOR MORE INFO SEE FindInBedTime.py module
        
        :param: None
        :return: returns got up and lights out times of participants in study
        :rtype: (list<datetime) (list<datetime>)
        """
        print('\n Finding got up and lights out time using no sleep diary...')
        window_size = 8
        index = 0
        LOdatetimeList = list()
        GUdatetimeList = list()

        print('\n getting trimmed data...')
        dates, times, activity, lux, participants = self.get_trimmed_data()
        self.participant_list = participants
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

    def convert_date_time(self, dates, times):
        """ Converts date and time arrays (stored as strings) and combines them 
        both to form one datetime array
        
        :param (arr) dates: array of dates
        :param (arr) times: array of times
        """
        datetime_arr = []
        for i  in range(0, len(dates)):
            datetimeString = dates[i] + ' ' + times[i]
            datetime_arr.append(datetime.datetime.strptime(datetimeString, '%Y-%m-%d %I:%M:%S %p'))
            
        return datetime_arr
       
    def get_trimmed_data(self ):
        """Gets the trimmed raw data using the TrimRaw data module
        
        :param: none
        :return: Returns the set of trimmed pieces of data
        :rtype: list<datetime>, list<datetime.time>, list<int>, list<int>
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


    #TODO: makes this function return two dictionaries where the indices 
    # are given by the partici[ant list]. See how this changes the time of execution
    def get_study_analysis_sleep_times(self):
        """Gets the lights and and got up times for the protocol method of 
        determining sleep points for the entire study
        
        Returns the lights out and got up times for the human protocol 
        in two lists of lists, one containing all the lights out time for each
        participant and the other the got up times for each participant.
        
        :return: Returns the lights out and got up tims of all the participants
            within the study
        :rtype: (list<list>) (list<list>)
        """
        print('\n Getting study analysis sleep times...')
        lights_out_analysis_study_times = list()
        got_up_analysis_study_times = list()
        
        for participant_id in self.participant_list:    # Gets analysis for participants that were done by program
            lightsOutTimes, gotUpTimes = self.get_participant_sleep_analysis_times(
                    self.sleep_analysis_directory, participant_id)
            
            lights_out_analysis_study_times.append(lightsOutTimes)
            got_up_analysis_study_times.append(gotUpTimes) 

        return lights_out_analysis_study_times, got_up_analysis_study_times

    
    def get_participant_sleep_analysis_times(self, sleepAnalysisDirectory, participant_id):
        """Gets the lights out and got up times of the participant as determined in
        in the sleep analysis
        
        :param (string) participant_id: The participant ID to identify correct 
                        sheet
        :return: Returns the lights out and got up tims of the participant as 
            specified within the sleep analysis spreadsheet
        :rtype: (list) (list)
        """
        sheetName = self.study_name + '-' + participant_id + ' ' + self.assesment
        print(sheetName)
        sleepAnalysis = pd.read_excel(sleepAnalysisDirectory, 
                                      sheet_name = sheetName,
                                      skiprows = self.skiprows_analysis )
        dates = self.get_dates(sleepAnalysis)     #get the dates the study was done over
        lightsOutAnalysisTimes = list()
        gotUpAnalysisTimes = list()
        for day in dates:
            lightsOutTime = sleepAnalysis.get_value(
                    self.lights_out_index_analysis, day)
            
            getUpTime = sleepAnalysis.get_value(self.got_up_index_analysis, day)
            if(isinstance(day, str)):
                try:
                    strDate = datetime.datetime.strptime(day[0:10], '%Y-%m-%d')
                except:
                    break
                getUpDateTime = datetime.datetime.combine(
                        strDate + datetime.timedelta(days = 1), getUpTime)
                lightsOutDateTime = datetime.datetime.combine(
                        strDate, lightsOutTime)
            else:
                #TODO fix this because rn just adding one day instead of actually
                #adding date. (check above as well)
                getUpDateTime = datetime.datetime.combine(
                        day + datetime.timedelta(days = 1), getUpTime)
                lightsOutDateTime = datetime.datetime.combine(
                        day, lightsOutTime)
                
            lightsOutAnalysisTimes.append(lightsOutDateTime)          
            gotUpAnalysisTimes.append(getUpDateTime)
            
        return lightsOutAnalysisTimes, gotUpAnalysisTimes
        
    def get_dates(self,sleepAnalysis):
        """Gets the dates the study was done over give the analysis dataframe
        
        :param (pandas dataframe) sleepAnalysis: sleep analysis excel scan
        :return: Returns the dates the study was done over as a list
        :rtype: (list<datetime.datetime>)
        """
        dates = list(sleepAnalysis)
        dates.pop()
        dates.pop()
        dates.reverse()
        dates.pop()
        dates.reverse()
        
        return dates
    