""" Title: Study
    Purpose: The study class 
    Author: Daniel Backhouse and Alan Yan
"""
# Import extension libraries
import MotionWareAnalysis
import SheetManager
import pandas as pd
#import datetime
#import numpy as np
import matplotlib.pyplot as plt

class Study:
    
    def __init__(self, sleep_analysis_directory, raw_data_directory, 
                 sleep_diary_directory, lights_out_index_diary, 
                 got_up_index_diary, lights_out_index_analysis, 
                 got_up_index_analysis, skiprows_diary, skiprows_analysis,
                 skiprows_rawdata, study_name, assesment):
        
        self.sleep_analysis_directory = sleep_analysis_directory
        self.raw_data_directory = raw_data_directory
        self.sleep_diary_directory = sleep_diary_directory
        self.lights_out_index_diary = lights_out_index_diary
        self.got_up_index_diary = got_up_index_diary
        self.lights_out_index_analysis = lights_out_index_analysis
        self.got_up_index_analysis = got_up_index_analysis
        self.skiprows_diary = skiprows_diary
        self.skiprows_analysis = skiprows_analysis
        self.skiprows_rawdata = skiprows_rawdata
        self.study_name = study_name
        self.assesment = assesment
        
        sleep_diaries, unmod_participant_list = self.get_sleep_diary_list_and_participants(
                self.sleep_analysis_directory)
        raw_data = self.get_raw_data_list(
                self.raw_data_directory)
        
        self.participant_list = self.modify_participant_list(unmod_participant_list)
        self.sleep_diaries = sleep_diaries
        self.raw_data = raw_data
        
    
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
        sleepAnalysis = pd.read_excel(sleepAnalysisDirectory, 
                                      sheet_name = sheetName,
                                      skiprows = self.skiprows_analysis )
        dates = self.get_dates(sleepAnalysis)     #get the dates the study was done over
        lightsOutAnalysisTimes = list()
        gotUpAnalysisTimes = list()
        for day in dates:
            lightsOutTime = sleepAnalysis.get_value(
                    self.lights_out_index_analysis, day)
            
            getUpTime = sleepAnalysis.get_value(self.get_up_index_analysis, day)
            lightsOutAnalysisTimes.append(lightsOutTime)         # Note here that we are assuming that the lightsOutTime dates and 
            gotUpAnalysisTimes.append(getUpTime)                # getUpTime dates are the same as those given by the program
        
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
    
    def get_study_program_times(self):
        """Gets the lights out and got up times of the participant as determined by 
        the program
        
        :param: none
        :return: Returns the lights out and got up tims of the participant as 
            specified by the program
        :rtype: (list)
        """
        lights_out_program_study_times = list()
        got_up_program_study_times = list()
        for i in range(0, len(self.sleep_diaries)):
           lightsOutTimes, gotUpTimes = self.get_participant_program_times(
                   self.raw_data[i], self.sleep_diaries[i])
           lights_out_program_study_times.append(lightsOutTimes)
           got_up_program_study_times.append(gotUpTimes)
        
 
    def get_participant_program_times(self, rawData,sleepDiary):
        """Gets the lights out and got up times of the participant as determined by 
        the program for the participant specified
        
        This program takes about two seconds per raw data and sleep diary file
        
        :param 
        :return: Returns the lights out and got up tims of the participant as 
            specified by the program
        :rtype: (list) (list)
        """
        lightsOutDateTimes, gotUpDateTimes = MotionWareAnalysis.findSleepPoint(
                sleepDiary, rawData)
        lightsOutTimes = list()
        gotUpTimes = list()
        for time in lightsOutDateTimes:
            lightsOutTimes.append(time.time())
        
        for time in gotUpDateTimes:
            gotUpTimes.append(time.time())
        
        return lightsOutTimes, gotUpTimes
    
    
    # All functions form here onward are only called within the class init   
    # *******************************************************************
    def modify_participant_list(self, participants):
        """Function that modifies the participant list for a given study and removes
        the study code from the string so that just the numbers are left
        
        :param (list) participant_list: a list of string with participant id's 
            with the study abbreviation preceding the number (ex: BT_001)
        :return: Modifies list with the abbreviation gone and only numbers (ex: 001)
        :rtype: (list)
        """
        index = len(self.study_name)
        final_index = index + 4     #This is since we assume the numbers will never exceed 
        # three digits
        modified_participant_list = list()
        for i in range(0, len(participants)):
            participant_id = participants[i]
            modified_participant_list.append(participant_id[index+1: final_index])
        
        return modified_participant_list
    
        
    #TODO: modify this function so that populateRawDataList takes a directory
    def get_raw_data_list(self, rawDataDirectory):
        """This function uses the SheetManager module and gets the raw Data
        excel files pandas data frame an stores each as a seperate entry in     
        a list
        
        :param (string) rawDataDirectory: the directory where the raw data is
        found
        :return: Returns a list of raw data files stored in dataframes
        :rtype: (list<pandas dataFrame>)
        """
        rawDataList = SheetManager.populateRawDataList()
        return rawDataList
    
    #TODO: modify this function so that populateDiaryList takes a directory as
    # input
    def get_sleep_diary_list_and_participants(self, sleepDiaryDirectory):
        """This function uses the SheetManager module and gets the sleep diary 
        files of each participant and stores each sleep diary as a seperate entry
        in a list. It also returns a list of strings containing the participant
        id's.
        
        :param (string) sleepDiaryDirectory: the directory where the raw data is
        found
        :return: Returns a list of sleep diaries stored in dataframes
        :return: Returns a list of participant id's
        :rtype: (list<pandas dataFrame>) (list<string>)
        """
        diaryList, participant_list = SheetManager.populateDiaryList()
        return diaryList, participant_list

    