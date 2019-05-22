# Module: raw_data_editor
# Purpose: This module is used to get and edit raw data CSV files containing 
# activity and light data
# Authors: Alan Yan
import pandas as pd
import datetime
#TODO: create open file function as I don't have so much copy pasted code

def study_trimmed_data(filePath, skiprows, startdate, enddate):
    """ Get's the trimmed data from specified file path based on the 
    start and enddates
    
    This function will cut off the activity, date, time and light data at the 
    dates specified in the parameters of the function. Generally these dates
    will be taken from a sleep diary or tracking file associated with the 
    motionwatch data collection
    
        
    :param (string) filepath: the filepath of the raw data CSV file
    :param (int) skiprows: the number of rows to skip when reading in data from
    CSV
    :param (datetime) startdate: the startdate to cut of data at
    :param (datetime) enddate: the enddate to cut the data at
    :raises: Print error if one of the 4 paramters are missing in the CSV
    """
    try:
        file = pd.read_csv(filePath, skiprows = skiprows)
    except:
        print('Failed to open file at ' + filePath)
    try:
        dates = file.iloc[:,0].tolist()
    except:
        print('Error no dates found in csv file at ' + filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        times = file.iloc[:,1].tolist()
    except:
        print('Error no times found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        activity = file.iloc[:,2].tolist()
    except:
        print('Error no activity data found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        lux = file.iloc[:,3].tolist()
    except:
        print('Error no light exposure data found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
    
    start = 0
    end = len(activity)-1
    for index in range(0, len(dates)):
        dateTime = datetime.datetime.strptime(
                dates[index], '%Y-%m-%d') 
        if(dateTime == startdate - datetime.timedelta(days = 1)):
            start = index
            break
         
    index = len(dates) - 1
    while index >= start:
        dateTime = datetime.datetime.strptime(
                dates[index], '%Y-%m-%d')
        if(dateTime == enddate + datetime.timedelta(days=1)):
            end = index
            break
        index = index - 1
    
    return dates[start:end], times[start:end], lux[start:end], activity[start:end]

def trimmed_data(filePath, skiprows):
    """ Gets the trimmed data from the specified file path 
    
    :param (string) filepath: the filepath of the raw data CSV file
    :param (int) skiprows: the number of rows to skip when reading in data from
    CSV
    :return: returns 4 array containing the dates, times, lux and activity
        found in the raw data CSV
    :raises: Print error if one of the 4 paramters are missing in the CSV
    """
    try:
        file = pd.read_csv(filePath, skiprows = skiprows)
    except:
        print('Failed to open file at ' + filePath)
    try:
        dates = file.iloc[:,0].tolist()
    except:
        print('Error no dates found in csv file at ' + filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        times = file.iloc[:,1].tolist()
    except:
        print('Error no times found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        activity = file.iloc[:,2].tolist()
    except:
        print('Error no activity data found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        lux = file.iloc[:,3].tolist()
    except:
        print('Error no lught exposure data found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
        
    foundBack = False
    foundFront = False    
    trim_ends(activity, dates, times, lux)
    while foundBack == False and foundFront  == False:
        if foundFront == False:
            for item in range(60*24*2):
                nonZero = 0
                for x in range(300):
                    if activity[item+x]:
                        nonZero += 1
                if nonZero <= 2:
                    for y in range(item+1):
                        pop(0,activity,dates,times,lux)
                    break
                if item == 60*24-1:
                    foundFront = True
        if foundBack == False:
            for item in range(len(activity)-60*24*2,len(activity)-300):
                nonZero = 0
                for x in range(300):
                    if activity[item+x]:
                        nonZero += 1
                if nonZero <= 2:
                    for y in range(len(activity)-(item+1)):
                        pop(-1,activity,dates,times,lux)
                    break
                if item == len(activity)-300-1:
                    foundBack = True
        trim_ends(activity, dates, times, lux)
    return dates, times, lux, activity

def untrimmed_data(filePath, skiprows):
    """ Gets the untrimmed data from the specified file path 
    
    :param (string) filepath: the filepath of the raw data CSV file
    :param (int) skiprows: the number of rows to skip when reading in data from
    CSV
    :return: returns 4 array containing the dates, times, lux and activity
        found in the raw data CSV
    :raises: Print error if one of the 4 paramters are missing in the CSV
    """
    try:
        file = pd.read_csv(filePath, skiprows = skiprows)
    except:
        print('Failed to open file at ' + filePath)
    try:
        dates = file.iloc[:,0].tolist()
    except:
        print('Error no dates found in csv file at ' + filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        times = file.iloc[:,1].tolist()
    except:
        print('Error no times found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        activity = file.iloc[:,2].tolist()
    except:
        print('Error no activity data found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
    try:
        lux = file.iloc[:,3].tolist()
    except:
        print('Error no lught exposure data found in csv file at ' +  filePath)
        print('Make sure raw activity and light file is formatted correctly')
        
    return dates, times, lux, activity


def trim_ends(activity, dates, times, lux):
    """ Function trims the ends of all 4 import pieces of data
    
    :param (arr) activity: array containing the activity
    :param (arr) dates: array containing the dates
    :param (arr) times: array containing the times
    :param (arr) lux: array containing the lux
    :return: None
    """
    beginningFound = True
    while beginningFound:
        if activity[0] == 0:
            pop(0, activity, dates, times, lux)
        else:
            zeroActivity = 0
            nonZeroActivity = 0
            for x in range(0, 20):
                if activity[x] == 0:
                    zeroActivity += 1
                else:
                    nonZeroActivity += 1
            if zeroActivity>nonZeroActivity:
                pop(0, activity, dates, times, lux)
            else:
                beginningFound = False
    
    endFound = True
    while endFound:
        if activity[-1] == 0:
            pop(-1, activity, dates, times, lux)
        else:
            zeroActivity = 0
            nonZeroActivity = 0
            for x in range(-20, 0):
                if activity[x] == 0:
                    zeroActivity += 1
                else:
                    nonZeroActivity += 1
            if zeroActivity>nonZeroActivity:
                pop(-1, activity, dates, times, lux)
            else:
               endFound = False    

def pop(index, activity, dates, times, lux):
    activity.pop(index)
    dates.pop(index)
    times.pop(index)
    lux.pop(index)
    return