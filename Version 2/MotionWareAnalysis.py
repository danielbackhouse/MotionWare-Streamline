""" Title: MotionWare Sleep Analysis VGH
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
# toSLeepIndex values and finish Sleep indedx values must be changed
# NOTE: The index values seem off by 1 because we remove the first row in
# the sleep diary upon storing it as pandas dataframe
toSleepIndex = 1
finishSleepIndex = 5
sleepDiarySkipRows = 0
sleepDiaryError = 1;    #hours

def getSleepDiary():
    """Reads the sleep diary and stores it in pandas DataFrame 

    Reads the Sleep diaries of study participants and stores the data in a 
    pandas DataFrame datatype. Raw Sleep data MUST be formatted correctly. 
    No exception will be thrown for incorrectly formatted sleep diary. (see 
    read me for sleep diary formatting). The dataframe does not store the data
    contained in the first row with the USER ID Code.
    
    Sleep diary times must be entered on 24 hour clock

    :param: none
    :return: sleep diary converted to pandas DataFrame
    :rtype: (pandas DataFrame)
    """
    #skipping row 1 for now based on current format
    
    xlsx = pd.ExcelFile('BT_Sleep_Diary.xlsx')
    sleepDiary = pd.read_excel(xlsx, sheetname='BT_022', dtype = str)
    
    #sleepDiary = pd.read_excel('BT_Sleep_Diary.xlsx', skiprows = sleepDiarySkipRows);
    
    return sleepDiary


def getSleepDates():
    """ Gets the dates the participant wore the MotionWatch 8

    :param: None
    :return: Returns the dates the particpant wore watch in chronological order
    :rtype: (list)
    """
    sleepDiary = getSleepDiary()
    dates = list(sleepDiary)
    dates.pop()  #remove baseline string from first col in dataframe
    dates.reverse()
    dates.pop()     #remove avg tring from last col in dataframe
    dates.reverse()     #flip back to chronoligcal order 
    
    return dates;
    

def getToSleepDateTimes():
    """ Gets the sleep times of the participant during study period

    This function gets the times the participant marked in their sleep diary
    that they started to try and fall alseep. It gets these times for the
    days where MotionWatch data was specified to be recorded.
    
    :param: None
    :return: Returns the time the particpant inidicated they were going to sleep
    :rtype: (list)
    """
    dates = getSleepDates()
    sleepDiary = getSleepDiary()
    toSleepList = list()
    
    for index in dates:
      
        date = index
        timeString = sleepDiary.get_value(toSleepIndex, date)
        
        #conerting time given as string in dataframe to datetime.time object
        time = datetime.datetime.strptime(timeString, '%H:%M:%S').time()
        
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


def getFinishSleepDateTimes():
    """Gets the times the participant specified they woke up in sleep diary
    
    :param: none
    :return: Returns the times the participant inidicated the woke up in diary
    :rtype: (list)
    """
    dates = getSleepDates()
    sleepDiary = getSleepDiary()
    finishSleepList = list()
     
    for index in dates:
        date = index
        timeString = sleepDiary.get_value(finishSleepIndex, date)
        #conert time given as string in dataframe to datetime.time object
        time = datetime.datetime.strptime(timeString, '%H:%M:%S').time()
        dateTime = datetime.datetime.combine(date, time)
        finishSleepList.append(dateTime)

    return finishSleepList
               

def sleepDataDateTime():
    """ Reads the sleep data and stores it in pandas DataFrame

    Reads the raw sleep data extracted from MotionWare software into CSV file 
    and stores the data in a pandas DataFrame datatype. The datetime 
    column becomes the indicies for the dataframe. Raw sleep data MUST be 
    formatted as specified in the read me document). 

    :param: none
    :return: dataframe with datetime as index, activity(int), lux(int) as cols
    :rtype: (pandas DataFrame)
    """
    sleepDataRaw = pd.read_excel('BT-022_Baseline.xlsx', skiprows = 12)
    dateTimeList = list()
    for index, row in sleepDataRaw.iterrows():
        dateTime = datetime.datetime.combine(row['Date'], row['Time'])
        dateTimeList.append(dateTime)
    
    dateTimeArray  = np.asarray(dateTimeList)
    sleepData = sleepDataRaw.set_index(dateTimeArray)
    sleepData = sleepData.drop(columns = ['Date', 'Time'])
    
    return sleepData


#TODO make this function more modular
def findSleepTime(sleepPointRange, actualSleepTime):
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
    :return: actualSleepTimes list with the times participant went to sleep
    :rtype: (list)
    """    
    
    meanActivity = sleepData['Activity (MW counts)'].mean()
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
  
    
def findSleepPoint():
    """ Finds the times the participant went to sleep and woke up

    This function utilizes the sleep diary times and sleep data to determine 
    the points at which a participant went to sleep and woke up. 
    
    :param: None
    :return: Returns two lists, one of when the participant went to sleep and 
             the other when they woke up
    :rtype: (list) (list)
    """
    sleepData = sleepDataDateTime()   # Get sleep diary from excel sheet
    lightsOutDiaryTimes = getToSleepDateTimes()      # Get sleep diary lights out times
    gotUpDiaryTimes = getFinishSleepDateTimes()      # Get sleep diary got up times
      
    actualSleepTime = list() 
    actualAwakeTime = list()
      
    for i in range(len(lightsOutDiaryTimes)):
          
          beforeLightsOutError = lightsOutDiaryTimes[i] - datetime.timedelta(hours = 1) # One hour before lights out
          afterLightsOutError = gotUpDiaryTimes[i] + datetime.timedelta(hours = 1) # One hour after got up
          sleepPointRange = sleepData.loc[beforeLightsOutError:afterLightsOutError] # range to check for actual lights out
          sleepTimes = findSleepTime(sleepPointRange, actualSleepTime)   # get the times the particiapnt went to sleep
            
          hourBeforeWakeUp = gotUpDiaryTimes[i] - datetime.timedelta(hours = 1)
          sleepRange = sleepData.loc[sleepTimes[i]: hourBeforeWakeUp] # estimated sleep range of participant (awake point estimated)

          beforeGotUpError = gotUpDiaryTimes[i] - datetime.timedelta(hours = 1) # One hour before got up
          afterGotUpError  = gotUpDiaryTimes[i] + datetime.timedelta(hours = 2) # Two hour after got up
          awakePointRange = sleepData.loc[beforeGotUpError:afterGotUpError]
          awakeTimes = findAwakeTime(awakePointRange, actualAwakeTime, gotUpDiaryTimes[i], sleepRange['Activity (MW counts)'].mean())      
        
    return sleepTimes, awakeTimes

    
"""
Main Program is executed from this point
@TODO: This will be changed to a public function within this python class
"""
# Get the particpants sleepData from the excel sheet
sleepData = sleepDataDateTime()
sleepDiary = getSleepDiary()

# Sleep times and awkaening times of participants
sleepTimes, awakeTimes = findSleepPoint()