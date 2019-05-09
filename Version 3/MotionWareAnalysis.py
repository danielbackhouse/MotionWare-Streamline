""" Title: MotionWareSleepAnalysis 
    Purpose: To determine the sleep points and awake times from raw data and 
            sleep diaries for given.
    Author: Daniel Backhouse and Alan Yan
"""

__license__ = "Daniel Backhouse"
__revision__ = " $Id: MotionWareAnalysis.py $ "
__docformat__ = 'reStructuredText'

#supress warnings message
import warnings; warnings.simplefilter("ignore");

#Import extenstion libraries
import numpy as np
import pandas as pd
import datetime

# If cells are not formatted as spcified in readMe the 
# toSLeepIndex values and finish Sleep index values must be changed
# NOTE: The index values seem off by 1 because we remove the first row in
# the sleep diary upon storing it as pandas dataframe
toSleepIndex = 1
finishSleepIndex = 5
sleepDiarySkipRows = 0
sleepDiaryError = 1;    #hours

def getSleepDatesDiary(sleepDiary):
    """ Gets the dates the participant was supposed to be recording sleep
    diary data according to the sleep watch

    :param (pandas DataFrame) sleepDiary: Participants sleep diary
    :return: Returns the dates the particpant wore watch in chronological order
    :rtype: (list)
    """
    dates = list(sleepDiary)
    dates.pop()  #remove baseline string from first col in dataframe
    dates.reverse()
    dates.pop()     #remove avg tring from last col in dataframe
    dates.reverse()     #flip back to chronoligcal order 
    
    return dates;

def getSleepDatesRawData(sleepData):
    """ Gets the dates the participant's activity was recorded.
    
    NOTE: It is important to note here that for any old study where the analysis
    has already been done these dates are determined by the days the that were
    analyzed NOT NECCESARILY the days that the study of sleep was meant to be 
    done. For any old study this will include all activity and light data 
    collected by the watch.

    :param (pandas DataFrame) rawData: rawData file formatted correctly with 
        dates as indices
    :return: Returns the dates the particpant wore watch in chronological order
    :rtype: (list)
    """
    allDatesandTimes = list(sleepData.index)
    dates = list()
    dates.append(allDatesandTimes[0])   #Add the first date
    counter = 0

    for dateTime in allDatesandTimes:
        if(dates[counter].day != dateTime.day ):
            dates.append(dateTime)
            counter = counter + 1
    # We remove the first entry to match how the dairy keeps track of dates
    dates.reverse()
    dates.pop()
    dates.reverse()
    
    return dates;    

def getToSleepDateTimes(sleepDiary):
    """ Gets the sleep times of the participant during study period

    This function gets the times the participant marked in their sleep diary
    that they started to try and fall alseep. It gets these times for the
    days where MotionWatch data was specified to be recorded.
    
    :param (pandas DataFrame) sleepDiary: Participants sleep diary
    :return: Returns the time the particpant inidicated they were going to sleep
    :rtype: (list)
    """
    dates = getSleepDatesDiary(sleepDiary)   
    toSleepList = list()
    
    for index in dates:
      
        date = index
        time = sleepDiary.get_value(toSleepIndex, date)
        
        # If the the participant goes to sleep in the morning
        # then the day given in the index correspoinds to the day they
        # went to sleep otherwise it is the day prior to that given in the
        # sleep diary
        if time <= datetime.time(hour = 12) and time >= datetime.time(hour=0):
            dateTime = datetime.datetime.combine(date, time)
            toSleepList.append(dateTime)
        else:       
            date = date - datetime.timedelta(days = 1)
            dateTime = datetime.datetime.combine(date, time)
            toSleepList.append(dateTime)

    return toSleepList


def getFinishSleepDateTimes(sleepDiary):
    """Gets the times the participant specified they woke up in sleep diary
    
    :param (pandas DataFrame) sleepDiary: Participants sleep diary
    :return: Returns the times the participant inidicated the woke up in diary
    :rtype: (list)
    """
    dates = getSleepDatesDiary(sleepDiary)
    finishSleepList = list()
     
    for index in dates:
        date = index
        time = sleepDiary.get_value(finishSleepIndex, date)
        dateTime = datetime.datetime.combine(date, time)
        finishSleepList.append(dateTime)

    return finishSleepList
               
# This is currently the program that takes the most amount of time to execute
# so perhaps we need to consider a way of do all the processing and analysis
# without making the date and time the index entries of the dataframe 
def sleepDataFormatter(sleepDataRaw):
    """ Takes in the raw sleep data and sets date and time as indices

    Takes in the raw sleep data as a pandas dataframe and then changes
    the indicecs such that they correspond to the date and time

    :param (pandas DataFrame) sleepDataRaw: Raw sleep dataframe
    :return: dataframe with datetime as index, activity(int), lux(int) as cols
    :rtype: (pandas DataFrame)
    """
    
    dateTimeList = list()
    for index, row in sleepDataRaw.iterrows():
        dateTime = datetime.datetime.combine(row['Date'], row['Time'])
        dateTimeList.append(dateTime)
    
    dateTimeArray  = np.asarray(dateTimeList)
    sleepData = sleepDataRaw.set_index(dateTimeArray)
    sleepData = sleepData.drop(columns = ['Date', 'Time'])
    
    return sleepData


#TODO make this function more modular
def findSleepTime(sleepPointRange, actualSleepTime, meanActivity):
    """ Commputes the sleep times 

    This function computes the sleep times of the participant given the 
    sleepPointRange (sleep range is the range of time in which is was determined
    it is most likely for the participant to have fell asleep). The sleepPointRange
    value is computed by taking the sleep time specified in the sleep diary and
    the generating a time range based on the sleep diary error specified in the
    global variables of this class. The actualSleepTime is an empty list that 
    we will store the computed sleep times in. 
    
    Sleep point are determined be checking the zeroMovementCount, 
    zeroLightCount, zeroLightActiveCount and darkMotion variables. For more on
    these and what they are see the readME. 
    
    Note that if a sleep point cannot be found give the thresholds the sleep
    diary value marked down by the participant will be used as the sleep time
    
    :param (pandas DataFrame) sleepPointRange: Range of times participant fell asleep
    :param (list) actualSleepTime: empty list where sleep times will be stored
    :param (double) meanActivity: The mean activity for participant over entire
                        time wearing the Motion Watch
    :return: actualSleepTimes list with the times participant went to sleep
    :rtype: (list)
    """    
    
    zeroMovementCount = 0;
    zeroLightCount = 0;
    zeroLightActiveCount = 0;
    darkMotion = 0;
    sleepActiveCheck = False
    sleepLightCheck = False
    foundSleepTime = False
    sleepTime = datetime.datetime.now()
    sleepLightTime = datetime.datetime.now()
          
            
    for index, row in sleepPointRange.iterrows():       
             
        if foundSleepTime == False:        # Find the time the participant went to sleep
            if int(row['Activity (MW counts)']) == 0:
                zeroMovementCount = zeroMovementCount + 1 
                      
                if int(row['Light (lux)']) == 0:
                    zeroLightActiveCount = zeroLightActiveCount + 1     
                      
                if sleepActiveCheck == False:
                    sleepActiveCheck = True
                    sleepTime = row.name  
            else:
                zeroMovementCount = 0
                sleepActiveCheck = False
                zeroLightActiveCount = 0
             
            if int(row['Light (lux)']) == 0:
                zeroLightCount = zeroLightCount + 1
                      
                if int(row['Activity (MW counts)']) <= meanActivity:
                    darkMotion = darkMotion + 1;            
                
                if sleepLightCheck == False:
                    sleepLightCheck = True
                    sleepLightTime = row.name  
            else:
                zeroMovementCount = 0
                sleepLightCheck = False
                darkMotion = 0
            
            # Check all counters to see if they have exceeded the threshold values
            if darkMotion >= 5 and foundSleepTime == False: # Look here to switch threshold values for light, activity and both 
                actualSleepTime.append(sleepLightTime)
                foundSleepTime = True
                  
            if zeroLightActiveCount >= 5 and foundSleepTime == False:
                actualSleepTime.append(sleepTime)
                foundSleepTime = True
                    
            if zeroMovementCount >= 20 and foundSleepTime == False:
                actualSleepTime.append(sleepTime)
                foundSleepTime = True
                  
            if zeroLightCount >= 15 and foundSleepTime == False:
                actualSleepTime.append(sleepLightTime)
                foundSleepTime = True
                      
    return actualSleepTime
 

def findAwakeTime(awakePointRange, actualAwakeTime, diaryTime, sleepRangeMean):
    """ Finds the times the participant woke up and returns it as a list

    This function determines the points at which the participant went to sleep
    on each day of the study are returns all the times they woke up as a list.
    
    :param (pandas DataFrame) awakePointRange: Estimated range during which
                participant woke up.
    :param (list) actualAwakeTime: Empty list where awake times are stored
    :param (datetime) diaryTime: Time participant marked to have gone to sleep
                in sleep diary.
    :param (double) sleepRangeMean: mean activity count over estimated sleep range
    :return: Returns a list containing the times the participant went to sleep
    :rtype: (list) 
    """
    zeroStirringCount = 0;
    awakeFound = False
    awakeTime = datetime.datetime.now()
    
    for index, row in awakePointRange.iterrows():
        
        if awakeFound == False:
            if int(row['Light (lux)']) != 0 and int(row['Activity (MW counts)']) >= sleepRangeMean:
                zeroStirringCount = zeroStirringCount + 1
                if zeroStirringCount == 1:
                    awakeTime = row.name                
            else:
                zeroStirringCount = 0
            
            if zeroStirringCount >= 5:
                awakeFound = True
                actualAwakeTime.append(awakeTime)
                break
            
    if awakeFound == False:         # If no time is found return diary time
        actualAwakeTime.append(diaryTime)            
             
    return actualAwakeTime;
  
    
def findSleepPoint(sleepDiary, rawData):
    """ Finds the times the participant went to sleep and woke up

    This function utilizes the sleep diary times and sleep data to determine 
    the points at which a participant went to sleep and woke up. 
    
    :param (pandas dataframe) sleepDiary: sleep diary of participant
    :param (pandas datafrmae) rawData: rawData of participant
    :return: Returns two lists, one of when the participant went to sleep and 
             the other when they woke up
    :rtype: (list) (list)
    """
    try:
        sleepData = sleepDataFormatter(rawData)   # Set the indices of raw sleep data to date and time
    except:
        print (rawData)
        
    lightsOutDiaryTimes = getToSleepDateTimes(sleepDiary)      # Get sleep diary lights out times
    gotUpDiaryTimes = getFinishSleepDateTimes(sleepDiary)      # Get sleep diary got up times
    
    #TODO: newly added piece of code to handle date mismatching
    studyDates_by_diary = getSleepDatesDiary(sleepDiary)
    studyDates_by_rawdata = getSleepDatesRawData(sleepData)
    #TODO
    diaryLength = len(studyDates_by_diary)
    rawDataLength = len(studyDates_by_rawdata)
    if(diaryLength > rawDataLength):
        print('\n The raw data file spans a shorter time frame...')
        if(studyDates_by_rawdata[0] == studyDates_by_diary[0]):
            print('\n Start dates match...')
        elif(studyDates_by_rawdata[rawDataLength-1] == studyDates_by_diary[diaryLength-1]):
            print('\n End dates match...')
        else:
            print('\n Neither start date or finald date match so find matching date...')
        
        print('\n For now returning empty list on above participant...\n')
        
        sleep = list()
        awake = list()
        return sleep, awake
    if(diaryLength == rawDataLength):
        print('\n Diary date length matches that of the raw data...')
        if(studyDates_by_rawdata[0] != studyDates_by_diary[0]):
            print('\n The dates do not align which means this data was analyzed first')
            sleep = list()
            awake = list()
            return sleep, awake
    if(diaryLength < rawDataLength):
        print('\n This is probably an un-analyzed participant so in this instance we probably use diary dates')
        print('\n Or anaylsis was done incorrectly')
        
        print(rawDataLength)
        
        sleep = list()
        awake = list()
        
        return awake, sleep
        
    actualSleepTime = list() 
    actualAwakeTime = list()
    meanActivity = sleepData['Activity (MW counts)'].mean(); 
    for i in range(len(lightsOutDiaryTimes)):
          
          beforeLightsOutError = lightsOutDiaryTimes[i] - datetime.timedelta(hours = 1) # One hour before lights out
          afterLightsOutError = gotUpDiaryTimes[i] + datetime.timedelta(hours = 1) # One hour after got up
          sleepPointRange = sleepData.loc[beforeLightsOutError:afterLightsOutError] # range to check for actual lights out
          sleepTimes = findSleepTime(sleepPointRange, actualSleepTime, meanActivity)   # get the times the particiapnt went to sleep

          #TODO: add exception for if the sleep range is checking outside
          # the data we have available.
          try:
              hourBeforeWakeUp = gotUpDiaryTimes[i] - datetime.timedelta(hours = 1)
              sleepRange = sleepData.loc[sleepTimes[i]: hourBeforeWakeUp] # estimated sleep range of participant (awake point estimated)
          except:
              awake = list()
              sleep = list()
              print('\n ***Found some unknown error... most likey timestamp issue ')
              return awake,sleep
          beforeGotUpError = gotUpDiaryTimes[i] - datetime.timedelta(hours = 1) # One hour before got up
          afterGotUpError  = gotUpDiaryTimes[i] + datetime.timedelta(hours = 2) # Two hour after got up
          awakePointRange = sleepData.loc[beforeGotUpError:afterGotUpError]
          awakeTimes = findAwakeTime(awakePointRange, actualAwakeTime, gotUpDiaryTimes[i], sleepRange['Activity (MW counts)'].mean())      
        
    return sleepTimes, awakeTimes