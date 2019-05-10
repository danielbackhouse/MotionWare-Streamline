""" Title: Study
    Purpose: The study class 
    Author: Daniel Backhouse and Alan Yan
"""
# Import extension libraries
import SheetManager
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import FindInBedTimes
############### Note participant list changes to just the diaries that are 
## properly filled once use_sleep_diaries has been called 
class Study:
    
    def __init__(self, sleep_analysis_directory, raw_data_directory, 
                 lights_out_index_analysis, got_up_index_analysis, 
                 skiprows_analysis, skiprows_rawdata, study_name, assesment):
        
        self.sleep_analysis_directory = sleep_analysis_directory
        self.raw_data_directory = raw_data_directory
        self.lights_out_index_analysis = lights_out_index_analysis
        self.got_up_index_analysis = got_up_index_analysis
        self.skiprows_analysis = skiprows_analysis
        self.skiprows_rawdata = skiprows_rawdata
        self.study_name = study_name
        self.assesment = assesment
        print('Getting raw activity and lux data for participants...')
        raw_data_all, raw_data_id = self.get_raw_data_list()
        print('\n Found raw activity and lux data...\n')
        self.raw_data = raw_data_all
        self.participant_list = raw_data_id

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
        LOdateList = list()
        GUdateList = list()
        LOtimeList = list()
        GUtimeList = list()
        for file in self.raw_data:
            print(self.participant_list[index])
            dates = file.iloc[:,0].values
            time = file.iloc[:,1].values
            activity = file.iloc[:,2].values
            lux = file.iloc[:,3].values
            LOdates, LOtimes, GUdates, GUtimes = FindInBedTimes.find_in_bed_time(
                    dates, time, activity, lux, window_size)
            LOdateList.append(LOdates)
            LOtimeList.append(LOtimes)
            GUdateList.append(GUdates)
            GUtimeList.append(GUtimes)
        
            index = index + 1
    
        return LOdateList, LOtimeList, GUdateList, GUtimeList    
        
    #TODO: modify this function so that populateRawDataList takes a directory
    def get_raw_data_list(self ):
        """This function uses the SheetManager module and gets the raw Data
        excel files pandas data frame an stores each as a seperate entry in     
        a list
        
        :param (string) rawDataDirectory: the directory where the raw data is
        found
        :return: Returns a list of raw data files stored in dataframes
        :rtype: (list<pandas dataFrame>)
        """
        #TODO Populating raw data list without sleep Diaries for now
        rawDataList, participants = SheetManager.populateRawDataNoDiary(self.raw_data_directory)
        return rawDataList, participants
    
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
        print(participant_id)
        sheetName = self.study_name + '-' + participant_id + ' ' + self.assesment
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
                getUpDateTime = datetime.datetime.combine(strDate, getUpTime)
                lightsOutDateTime = datetime.datetime.combine(strDate, lightsOutTime)
            else:
                getUpDateTime = datetime.datetime.combine(day, getUpTime)
                lightsOutDateTime = datetime.datetime.combine(day, lightsOutTime)
                
            lightsOutAnalysisTimes.append(lightsOutDateTime)         # Note here that we are assuming that the lightsOutTime dates and 
            gotUpAnalysisTimes.append(getUpDateTime)                # getUpTime dates are the same as those given by the program
        
        return lightsOutAnalysisTimes, gotUpAnalysisTimes

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
    
    def get_error_list_participant(self,participant_times_program, participant_times_protocol):
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
        for i in range(0, len(participant_times_program)):
            timeDifference = participant_times_program[i] - participant_times_protocol[i]
            error = abs(timeDifference.total_seconds()/(60*len(participant_times_program)))
            error = error**2
            errorList.append(error)
        
        return errorList