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
        SleepInfoList = list()

        print('\n getting trimmed data...')
        dates, times, activity, lux, participants = self.get_trimmed_data()
        self.participant_list = participants
        print('\n trimmed data... calculating sleep points...')
        for i in range(0, len(participants)):
            print(participants[i])
            datetime_arr = self.convert_date_time(dates[i], times[i])
            LOdatetime, GUdatetime, SleepInfo = FindInBedTimes.find_in_bed_time(
                    datetime_arr, activity[i], lux[i], window_size)
            LOdatetimeList.append(LOdatetime)
            GUdatetimeList.append(GUdatetime)
            SleepInfoList.append(SleepInfo)
        
            index = index + 1
    
        return LOdatetimeList, GUdatetimeList, SleepInfoList, self.participant_list
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
        
        for participant_id in self.participant_list:
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
                
            lightsOutAnalysisTimes.append(lightsOutDateTime)         # Note here that we are assuming that the lightsOutTime dates and 
            gotUpAnalysisTimes.append(getUpDateTime)                # getUpTime dates are the same as those given by the program
        
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
    
    def error_in_date_time_lists(self, program, protocol):
        """Computes the errors between two list of lists
        
        :param (list<list>) GU_program: errors between two times 
        :return: Returns error between the two lists of lists
        :rtype: (list) 
        
        """
        sum_of_squares_error_study = list()
        for i in range(0, len(program)):
            errorList = self.get_error_list_participant(program[i], protocol[i])
            error =  sum(errorList)
            sum_of_squares_error_study.append(error)
        
        plt.figure()
        plt.plot(self.participant_list, sum_of_squares_error_study)
        plt.rc('xtick', labelsize = 8)
        return sum_of_squares_error_study
    
    def get_error_list_participant(self,datetimes_program, datetimes_protocol):
        """Computes the errors between two datetime lists
        
        :param (list<datetime>): The datetims participant went to sleep over study
            according to analysis
        :param (list<datetime>): The datetimes participant went to sleep over
            study according to program
        :return: The difference of the errors in minutes between the two squared
        :rtype: (list)
        """
        errorList = list()
        #TODO:Note here that currently some of the lists are empty
        # for the program times so we are still returning null on some values
        # Will need to add some conditional statement to check that both are the same length
        
        for i in range(0, len(datetimes_protocol)):
                timeDifference = datetimes_program[i] - datetimes_protocol[i]
                error = abs(timeDifference.total_seconds()/(60*len(datetimes_program)))
                error = error**2
                errorList.append(error)
                    
        return errorList
    