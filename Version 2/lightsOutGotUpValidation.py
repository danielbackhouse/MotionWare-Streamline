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
import datetime
import numpy as np
import matplotlib.pyplot as plt
# Define global variables
sleepAnalysisDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Analysis 2019-03-19.xlsx'

def get_sleep_analysis_times():
    """Gets the lights out and got up times of the participant as determined in
    in the sleep analysis
    
    :param: none
    :return: Returns the lights out and got up tims of the participant as 
        specified within the sleep analysis spreadsheet
    :rtype: (list) (list)
    """
    lightsOutIndex  = 2;
    getUpIndex  = 5;
    
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
        
        # Note here that we are assuming that the lightsOutTime dates and 
        # getUpTime dates are the same as those given by the program
        lightsOutAnalysis.append(lightsOutTime)
        gotUpAnalysis.append(getUpTime)
    
    return lightsOutAnalysis, gotUpAnalysis, dates


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

# Main execution for the time being will till testing function
lights_out_analysis_times, got_up_analysis_times,  dates = get_sleep_analysis_times()
lights_out_program_datetimes, got_up_program_datetimes = get_program_times()

lights_out_program_times  = list()
for times in lights_out_program_datetimes:
    lights_out_program_times.append(times.time())

got_up_program_times = list()    
for times in got_up_program_datetimes:
    got_up_program_times.append(times.time())


lights_out_relative_error = list()
#Error comparison
#TODO: what if the two lists aren't the same size
for i in range(0,len(lights_out_program_times)):
    error = lights_out_program_times[i].minute - lights_out_analysis_times[i].minute
    lights_out_relative_error.append(error)


#TODO: Making function to create square sum of errors
plt.figure(0)
plt.plot(got_up_analysis_times)
plt.plot(got_up_program_times)
plt.show()

plt.figure(1)
plt.plot(error)
plt.show()