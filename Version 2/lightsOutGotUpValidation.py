""" Title: lightsOutGotUpValidation
    Purpose: Compares the lights out times and got up times determined following
    the MotionWatch 8 Protocol and the MotionWareAnalysisProgram and plots
    the relative errors between the two
    Author: Daniel Backhouse and Alan Yan
"""
# Import extension libraries
import MotionWareAnalysis
import SheetManager
import pandas as pd
#import datetime
import numpy as np
import matplotlib.pyplot as plt

sleepAnalysisDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Analysis 2019-03-19.xlsx'
study_name = 'BT'
assesment = 'Baseline'
lights_out_index  = 2;
get_up_index  = 5;
skiprows_analysis = 16;
#TODO: Create a function that gets the dates for a specified participant
#did the study over
dates = "Will be the dates the study goes over"

def get_study_analysis_sleep_times(participant_list):
    """Gets the lights and and got up times for the protocol method of 
    determining sleep points for the entire study
    
    Returns the lights out and got up times for the human protocol 
    in two lists of lists, one containing all the lights out time for each
    participant and the other the got up times for each participant.
    
    :param (list<string>) participant_list: A list of participant ID's
    :return: Returns the lights out and got up tims of all the participants
        within the study
    :rtype: (list<list>) (list<list>)
    """
    lights_out_analysis_study_times = list()
    got_up_analysis_study_times = list()
    
    for participant_id in participant_list:
        lightsOutTimes, gotUpTimes = get_participant_sleep_analysis_times(
                sleepAnalysisDirectory, participant_id)
        lights_out_analysis_study_times.append(lightsOutTimes)
        got_up_analysis_study_times.append(gotUpTimes)
        
    return lights_out_analysis_study_times, got_up_analysis_study_times


def get_participant_sleep_analysis_times(sleepAnalysisDirectory, participant_id):
    """Gets the lights out and got up times of the participant as determined in
    in the sleep analysis
    
    :param (string) participant_id: The participant ID to identify correct 
                    sheet
    :return: Returns the lights out and got up tims of the participant as 
        specified within the sleep analysis spreadsheet
    :rtype: (list) (list)
    """
    sheetName = study_name + '-' + participant_id + ' ' + assesment
    sleepAnalysis = pd.read_excel(sleepAnalysisDirectory, 
                                  sheet_name = sheetName,
                                  skiprows = skiprows_analysis )
    dates = get_dates(sleepAnalysis)     #get the dates the study was done over
    lightsOutAnalysisTimes = list()
    gotUpAnalysisTimes = list()
    for day in dates:
        lightsOutTime = sleepAnalysis.get_value(lights_out_index, day)
        getUpTime = sleepAnalysis.get_value(get_up_index, day)
        lightsOutAnalysisTimes.append(lightsOutTime)         # Note here that we are assuming that the lightsOutTime dates and 
        gotUpAnalysisTimes.append(getUpTime)                # getUpTime dates are the same as those given by the program
    
    return lightsOutAnalysisTimes, gotUpAnalysisTimes



def get_dates(sleepAnalysis):
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


def get_study_program_times(rawDataList, diaryList):
    """Gets the lights out and got up times of the participant as determined by 
    the program
    
    :param: none
    :return: Returns the lights out and got up tims of the participant as 
        specified by the program
    :rtype: (list)
    """
    lights_out_program_study_times = list()
    got_up_program_study_times = list()
    for i in range(0, len(diaryList)):
       lightsOutTimes, gotUpTimes = get_participant_program_times(
               rawDataList[i], diaryList[i])
       lights_out_program_study_times.append(lightsOutTimes)
       got_up_program_study_times.append(gotUpTimes)
       
       
    
    return lights_out_program_study_times, got_up_program_study_times

def get_participant_program_times(rawData,sleepDiary):
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

def plot_participant_GotUp_error(GU_program, GU_analysis):
    """Plots the relative errors of the got up times, comparing those generated
    by the program and those found following the protocol
    
    :param (list) GU_program: The Got up times found by the program
    :param (list) GU_analysis: The got up times found using the protocol
    :return: None
    """
    plt.figure()
    plt.plot(GU_program)
    plt.plot(GU_analysis)
    plt.show()

    errorList = get_participant_error_list(GU_program, GU_analysis)
    plt.figure()
    plt.plot(errorList)
    
    
def plot_participant_LightsOut_error(LO_program, LO_analysis):
    """Plots the relative errors of the lights out times, comparing those generated
    by the program and those found following the protocol
    
    :param (list) LO_program: The lights out times found by the program
    :param (list) LO_analysis: The lights out times found using the protocol
    :return: None
    """
    plt.figure()
    plt.plot(LO_program)
    plt.plot(LO_analysis)
    plt.show()

    errorList = get_participant_error_list(LO_program, LO_analysis)
    plt.figure()
    plt.plot(errorList)    
    
def get_participant_error_list(program_times, protocol_times):
    """Gets a list containing the errors (in units of minutes) between
    the times determined by the protocol method and by the program and
    places them in a list in the order of the dates
    
    :param (list) program_times: The Got up times found by the program
    :param (list) protocol_times: The got up times found using the protocol
    :return: errorList which is a list of the relative errors (absolute value)
    :rtype: (list)
    """   
    errorList = list()
    for i in range(0,len(protocol_times)):
        error = protocol_times.minute - program_times.minute
        errorList.append(error)
        
    return errorList
    

#TODO
def get_raw_data_list(rawDataDirectory):
    return False

#TODO
def get_sleep_diary_list(sleepDiaryDirectory):
    return False

#TODO
def get_participant_list(sleepDiaryDirectory):
    return False

print('\n Getting ' + assesment + ' raw data for ' + study_name + ' study... \n')  
participant_list = list()
participant_list.append('001')
rawDataList = SheetManager.populateRawDataList()
print('\n Found raw data... Getting sleep diary data...')
diaryList = SheetManager.populateDiaryList()
print('\n Found sleep diary data... Getting existing protocol sleep times... \n')

LO_analysis, GU_analysis = get_study_analysis_sleep_times(participant_list)
print('\n Found exisiting protocol sleep times... Calculating sleep times...\n')
LO_program, GU_program = get_participant_program_times(rawDataList[0], diaryList[0])
print('\n Sleep points calculated... Program completed! \n')

plot_participant_LightsOut_error(LO_program, LO_analysis[0])
plot_participant_GotUp_error(GU_program, GU_analysis[0])

