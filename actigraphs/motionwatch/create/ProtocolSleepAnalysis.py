# Class: ProtocolSleepAnalysis
# Author: Daniel Backhouse

import pandas as pd
import datetime

class ProtocolSleepAnalysis:
    
    def __init__(self, sleep_analysis_directory, participant_list, study_name, assesment):
        self.sleep_analysis_directory = sleep_analysis_directory
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
        lights_out_analysis = {}
        got_up_analysis = {}
        sleep_eff = {}
        frag_index = {}
        LOdic = {}
        for participant_id in self.participant_list:
            lightsOutTimes, gotUpTimes, se, fi = self.get_participant_sleep_analysis_times(
                    self.sleep_analysis_directory, participant_id)
            
            lights_out_analysis[participant_id] = lightsOutTimes
            got_up_analysis[participant_id] = (gotUpTimes)
            LOdic[participant_id] = lightsOutTimes
            sleep_eff[participant_id] = se
            frag_index[participant_id] = fi
            
        return lights_out_analysis, got_up_analysis, sleep_eff, frag_index

    
    def get_participant_sleep_analysis_times(self, sleepAnalysisDirectory, participant_id):
        """Gets the lights out and got up times of the participant as determined in
        in the sleep analysis
        
        :param (string) participant_id: The participant ID to identify correct 
                        sheet
        :return: Returns the lights out and got up tims of the participant as 
            specified within the sleep analysis spreadsheet
        :rtype: (list) (list)
        """
        LOdatetime = []
        GUdatetime = []
        
        sheetName = self.study_name + '-' + participant_id + ' ' + self.assesment
        print(sheetName)
        try:
            sleepAnalysis = pd.read_excel(sleepAnalysisDirectory, sheet_name = sheetName)
        except:
            print('No such sheet in sleep analysis excel sheet')
            return LOdatetime, GUdatetime, list(), list()
        
        lightsOutDates = sleepAnalysis.iloc[15,1:15].tolist()
        lightsOutTimes = sleepAnalysis.iloc[18,1:15].tolist()
        gotUpDates = sleepAnalysis.iloc[17,1:15].tolist()
        gotUpTimes = sleepAnalysis.iloc[21, 1:15].tolist()
        
        fragmentation = sleepAnalysis.iloc[45, 1:15].tolist()
        sleep_effeciency = sleepAnalysis.iloc[28, 1:15].tolist()

        
        for i in range(0, len(lightsOutDates)):
            try:
                LOdatetime.append(datetime.datetime.combine(lightsOutDates[i], lightsOutTimes[i]))
                GUdatetime.append(datetime.datetime.combine(gotUpDates[i], gotUpTimes[i]))
            except:
                print('date formatted incorectly, compensating...')
                
            try:
                LOdate = datetime.datetime.strptime(lightsOutDates[i], '%m/%d/%Y')
                GUdate = datetime.datetime.strptime(gotUpDates[i], '%m/%d/%Y')
                LOdatetime.append(datetime.datetime.combine(LOdate, lightsOutTimes[i]))
                GUdatetime.append(datetime.datetime.combine(GUdate, gotUpTimes[i]))
            except:
                print('could not format date properly...')
             
        return LOdatetime, GUdatetime, sleep_effeciency, fragmentation
            