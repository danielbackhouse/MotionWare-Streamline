""" Title: MotionWare Sleep Analysis VGH
    Purpose: To determine the sleep points and awake times from raw data and sleep diaries for given participants
    uthor: Daniel Backhouse
"""

__license__ = "Daniel Backhouse"
__revision__ = " $Id: MotionWareAnalysis.py $ "
__docformat__ = 'reStructuredText'

#supress warnings message
import warnings; warnings.simplefilter("ignore");

#Import extenstion libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

toSleepIndex = 0
finishSleepIndex = 2
sleepDiarySkipRows = 1
sleepDiaryError = 1; #hours

#TODO: Add Raises clause so that we don't allow improperly formatted CSV file 
def getSleepData():
    """ Reads the sleep data and stores it in pandas DataFrame

    Reads the raw sleep data extracted from MotionWare software into CSV file 
    and stores the data in a pandas DataFrame datatype. Raw sleep data MUST be 
    formatted as follows:
        - 3 columns of data (date and time, activity count and then lux count)
        - first row holds strings specifying which column corresponds to which
        - all subsequent rows should only include relevant data
        - dates must be in chronological order
    else an exception an exception will be thrown
    
    :param: none
    :raises ValueError if CSV formatted incorrectly
    :return: dataframe with datetime, activity (int), lux (int) as cols
    :rtype: (pandas DataFrame)
    """
    sleepData = pd.read_excel('SampleRawData.xlsx')
    sleepData = sleepData.set_index("Date")
    
    return sleepData

#TODO:  Add sleep diary format to readme
def getSleepDiary():
    """Reads the sleep diary and stores it in pandas DataFrame 

    Reads the Sleep diaries of study participants and stores the data in a 
    pandas DataFrame datatype. Raw Sleep data MUST be formatted correctly. 
    No exception will be thrown for incorrectly formatted sleep diary. (see 
    read me for sleep diary formattingg)

    :param: none
    :return: sleep diary converted to pandas DataFrame
    :rtype: (pandas DataFrame)
    """
    #skipping row 1 for now based on current format
    sleepDiary = pd.read_excel('SampleSleepDiaries.xlsx', skiprows = sleepDiarySkipRows);
    
    return sleepDiary

"""
@Function: getSleepDates()
@Parameters: None
@Returns: Returns the dates participant wore MotionWare watch as list
"""
def getSleepDates():
    """ Reads the sleep diary 

    Extended description of function.

    :param int arg1: Description of arg1.
    :param str arg2: Description of arg2.
    :raises ValueError if arg1 is equal to arg2
    :return: Description of return value
    :rtype: bool
    """
    sleepDiary = getSleepDiary()
    dates = list(sleepDiary)
    dates.reverse()
    dates.pop()
    
    return dates;
    

"""
@Function: SleepDateTimes()
@Parameter: None
@Returns: Returns a list of the to sleep times of participant from most recent day
to oldest day
"""
def getToSleepDateTimes():
    dates = getSleepDates()
    sleepDiary = getSleepDiary()
    toSleepList = list()
     
    for index in dates:
       
        date = index
        time = sleepDiary.get_value(toSleepIndex, date)
        if time <= datetime.time(hour = 12) and time >= datetime.time(hour=0):
            dateTime = datetime.datetime.combine(date, time)
            toSleepList.append(dateTime)
        else:
            date = date - datetime.timedelta(days = 1)
            dateTime = datetime.datetime.combine(date, time)
            toSleepList.append(dateTime)
        
    return toSleepList


"""
@Function: SleepDateTimes()
@Parameter: None
@Returns: Returns a list of the to sleep times of participant from most recent day
to oldest day
"""
def getFinishSleepDateTimes():
    dates = getSleepDates()
    sleepDiary = getSleepDiary()
    finishSleepList = list()
     
    for index in dates:
        date = index
        time = sleepDiary.get_value(finishSleepIndex, date)
        dateTime = datetime.datetime.combine(date, time)
        finishSleepList.append(dateTime)
    
    return finishSleepList
               
"""
@Function: sleepDataDateTime()
@Parameters: None
@Returns: Sleep data edited with date and time combined as indices 
"""
def sleepDataDateTime():
    sleepDataRaw = pd.read_excel('SampleRawData.xlsx')
    dateTimeList = list()
    for index, row in sleepDataRaw.iterrows():
        dateTime = datetime.datetime.combine(row['Date'], row['Time'])
        dateTimeList.append(dateTime)
    
    dateTimeArray  = np.asarray(dateTimeList)
    sleepData = sleepDataRaw.set_index(dateTimeArray)
    sleepData = sleepData.drop(columns = ['Date', 'Time'])
    
    return sleepData

"""
@Function: findSleepTime
@Parameters: Takes the sleep range and the sleepTime list
@Returns: The time the participant went to sleep
"""
def findSleepTime(sleepRange, actualSleepTime):
    
          meanActivity = sleepData['Activity (MW counts)'].mean()
          #Set too sleep variables
          zeroMovementCount = 0;
          zeroLightCount = 0;
          zeroLightActiveCount = 0;
          darkMotion = 0;
          sleepActiveCheck = False
          sleepLightCheck = False
          foundSleepTime = False
          sleepTime = datetime.datetime.now()
          sleepLightTime = datetime.datetime.now()
          
            
          for index, row in sleepRange.iterrows():       
             
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
                  
                  if darkMotion >= 5 and foundSleepTime == False: # Look here to switch threshold values for light, activity and both 
                      #print('dark motion')
                      actualSleepTime.append(sleepLightTime)
                      foundSleepTime = True
                  
                  if zeroLightActiveCount >= 5 and foundSleepTime == False:
                      #print('zero activity and then no Light')
                      actualSleepTime.append(sleepTime)
                      foundSleepTime = True
                    
                  if zeroMovementCount >= 20 and foundSleepTime == False:
                     #print('no movement')
                     actualSleepTime.append(sleepTime)
                     foundSleepTime = True
                  
                  if zeroLightCount >= 15 and foundSleepTime == False:
                      #print('no light')
                      actualSleepTime.append(sleepLightTime)
                      foundSleepTime = True
                      
          return actualSleepTime
 
    
"""
@Function: sleepTimeCheck
@Parameters: darkRange -  pandas dataframe corrsponding to range participant was aslseep (dataframe)
             meanActivity  - mean Activity of sleepdata (float)
             meanLux - mean lux of sleepdata (float)
             certaintyList - list of certainties for each day
@Returns: A value from 1 - 10 corresponding to the activity present during sleep
and the certainty of the sleepTime value
"""    
def sleepTimeCheck(darkRange, meanActivity, meanLux, luxVariance, activityVariance):
    meanRangeActivity  = darkRange['Activity (MW counts)'].mean()
    meanRangeLux = darkRange['Light (lux)'].mean()
    
    luxVariance.append(meanLux - meanRangeLux)
    activityVariance.append(meanActivity - meanRangeActivity)
    
    return luxVariance, activityVariance

"""
@Function: findAwakeTime
@Parameters: Takes the awake range (pandas dataframe) and the awake time list
@ Returns: A list of times the participant woke up
"""
def findAwakeTime(awakeRange, actualAwakeTime, diaryTime, darkRangeMean):
    zeroStirringCount = 0;
    awakeFound = False
    awakeTime = datetime.datetime.now()
    
    for index, row in awakeRange.iterrows():
        
        if awakeFound == False:
            if int(row['Light (lux)']) != 0 and int(row['Activity (MW counts)']) >= darkRangeMean:
                zeroStirringCount = zeroStirringCount + 1
                if zeroStirringCount == 1:
                    awakeTime = row.name
                
            else:
                zeroStirringCount = 0
            
            if zeroStirringCount >= 5:
                awakeFound = True
                actualAwakeTime.append(awakeTime)
                break
            
    # If no time is found return diary time
    if awakeFound == False:
        actualAwakeTime.append(diaryTime)            
             
    return actualAwakeTime;
  
""""
@Function: findSleepPoint()
@Parameters: sleepData (DataFrame), activityMean (float)
@Returns: The point at which participant went to sleep on given day
"""
def findSleepPoint():
      sleepData = sleepDataDateTime()
      toSleepTimes = getToSleepDateTimes() # Sleep Diary Sleep times
      finishSleepTimes = getFinishSleepDateTimes() # Sleep Diary Awaken Times
      
      meanActivity = sleepData['Activity (MW counts)'].mean()
      meanLux = sleepData['Light (lux)'].mean()
      
      
      actualSleepTime = list()
      actualAwakeTime = list()
      activityVariance = list()
      luxVariance = list()
      
      for i in range(len(toSleepTimes)):        # iterare through sleep times
          # Find too sleep times of the participant
          toSleepError = toSleepTimes[i] - datetime.timedelta(hours = 1)
          finishSleepError = finishSleepTimes[i] + datetime.timedelta(hours = 1)
          sleepRange = sleepData.loc[toSleepError:finishSleepError]
          sleepTimes = findSleepTime(sleepRange, actualSleepTime)
          
          # Analyze the sleep period of the participant to look for strange activty or lux
          hourBeforeWakeUp = finishSleepTimes[i] - datetime.timedelta(hours = 1)
          darkRange = sleepData.loc[sleepTimes[i]: hourBeforeWakeUp]
          sleepTimeCheck(darkRange, meanActivity, meanLux, luxVariance, activityVariance)
          
          # Find the awakening times of the participant
          twohourBeforeWakeUp = finishSleepTimes[i] - datetime.timedelta(hours = 1)
          finishSleepGuess  = finishSleepTimes[i] + datetime.timedelta(hours = 2)
          awakeRange = sleepData.loc[twohourBeforeWakeUp:finishSleepGuess]
          awakeTimes = findAwakeTime(awakeRange, actualAwakeTime, finishSleepTimes[i], darkRange['Activity (MW counts)'].mean())      
        
      return sleepTimes, awakeTimes

    
"""
@Main: Runs the main 
@Purpose: Runs each function to execute program
"""
##Get the particpants sleepData from the excel sheet
sleepData = sleepDataDateTime()

# Sleep times and awkaening times of participants
sleepTimes, awakeTimes = findSleepPoint()
