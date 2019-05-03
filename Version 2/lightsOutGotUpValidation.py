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

# Define global variables
sleepAnalysisDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Analysis 2019-03-19.xlsx'
lightsOutIndex  = 2;
getUpIndex  = 5;

def get_sleep_analysis_times():
    """Gets the lights out and got up times of the participant as determined in
    in the sleep analysis
    
    :param: none
    :return: Returns the lights out and got up tims of the participant as 
        specified within the sleep analysis spreadsheet
    :rtype: (list)
    """
    sleepAnalysis = pd.read_excel(sleepAnalysisDirectory, 
                                  sheet_name = 'BT-001 Baseline', skiprows = 16)
    
    dates = list(sleepAnalysis)     #get the dates the study was done over
    dates.pop()
    dates.pop()
    dates.reverse()
    dates.pop()
    dates.reverse()
    
    lightsOutAnalysis = list()
    gotUpAnalysis = list()
    
    # iterate over study dates within excel sheet at specified indices
    # to get the lights out and got up values for each specific date
    for day in dates:
        lightsOutTime = sleepAnalysis.get_value(lightsOutIndex, day)
        getUpTime = sleepAnalysis.get_value(getUpIndex, day)
        
        lightsOutAnalysis.append(lightsOutTime)
        gotUpAnalysis.append(getUpTime)
    
    return lightsOutAnalysis, gotUpAnalysis


def get_program_times():
    """Gets the lights out and got up times of the participant as determined by 
    the program
    
    :param: none
    :return: Returns the lights out and got up tims of the participant as 
        specified by the program
    :rtype: (list)
    """
    
    rawDataList = SheetManager.populateRawDataList()
    diaryList = SheetManager.populateDiaryList()
    
    lightsOutTimes, gotUpTimes = MotionWareAnalysis.findSleepPoint(diaryList[0], rawDataList[0])
    
    return lightsOutTimes, gotUpTimes



