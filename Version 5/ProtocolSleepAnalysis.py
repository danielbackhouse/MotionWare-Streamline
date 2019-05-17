# Class: ProtocolSleepAnalysis
# Author: Daniel Backhouse

import pandas as pd
import datetime

class ProtocolSleepAnalysis:
    
    def __init__(self, participant_list, study_name, assesment):
        self.sleep_analysis_directory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Analysis 2019-03-19.xlsx'
        self.lights_out_index_analysis = 2
        self.got_up_index_analysis = 5
        self.skiprows_analysis = 1
        self.participant_list = participant_list
        self.study_name = study_name
        self.assesment = assesment


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