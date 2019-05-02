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
import numpy as np
import pandas as pd
import datetime

# If cells are not formatted as spcified in readMe the 
# toSLeepIndex values and finish Sleep indedx values must be changed
# NOTE: The index values seem off by 1 because we remove the first row in
# the sleep diary upon storing it as pandas dataframe
toSleepIndex = 0
finishSleepIndex = 2
sleepDiarySkipRows = 1
sleepDiaryError = 1; #hours

def getSleepDiary():
    """Reads the sleep diary and stores it in pandas DataFrame 

    Reads the Sleep diaries of study participants and stores the data in a 
    pandas DataFrame datatype. Raw Sleep data MUST be formatted correctly. 
    No exception will be thrown for incorrectly formatted sleep diary. (see 
    read me for sleep diary formatting). The dataframe does not store the data
    contained in the first row with the USER ID Code.

    :param: none
    :return: sleep diary converted to pandas DataFrame
    :rtype: (pandas DataFrame)
    """
    #skipping row 1 for now based on current format
    sleepDiary = pd.read_excel('SampleSleepDiaries.xlsx', skiprows = sleepDiarySkipRows);
    
    return sleepDiary


def getSleepDates():
    """ Gets the dates the participant wore the MotionWatch 8

    :param: None
    :return: Returns the dates the particpant wore watch in chronological order
    :rtype: (list)
    """
    sleepDiary = getSleepDiary()
    dates = list(sleepDiary)
    dates.reverse()
    dates.pop()
    
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
        time = sleepDiary.get_value(toSleepIndex, date)
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
        time = sleepDiary.get_value(finishSleepIndex, date)
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
    sleepDataRaw = pd.read_excel('SampleRawData.xlsx')
    dateTimeList = list()
    for index, row in sleepDataRaw.iterrows():
        dateTime = datetime.datetime.combine(row['Date'], row['Time'])
        dateTimeList.append(dateTime)
    
    dateTimeArray  = np.asarray(dateTimeList)
    sleepData = sleepDataRaw.set_index(dateTimeArray)
    sleepData = sleepData.drop(columns = ['Date', 'Time'])
    
    return sleepData


#TODO make this function more modular
def findSleepTime(sleepRange, actualSleepTime):
    """ Commputes the sleep times 

    This function computes the sleep times of the participant given the 
    sleeprange (sleep range is the range of time in which is was determined
    it is most likely for the participant to have fell asleep). The sleepRange
    value is computed by taking the sleep time specified in the sleep diary and
    the generating a time range based on the sleep diary error specified in the
    global variables of this class. The actualSleepTime is an empty list that 
    we will store the computed sleep times in. 
    
    Sleep point are determined be checking the zeroMovementCount, 
    zeroLightCount, zeroLightActiveCount and darkMotion variables. For more on
    these and what they are see the readME. 
    
    Note that if a sleep point cannot be found give the thresholds the sleep
    diary value marked down by the participant will be used as the sleep time
    
    :param (pandas DataFrame) sleepRange: Range of times participant fell asleep
    :param (list) actualSleepTime: empty list where sleep times will be stored
    :return: actualSleepTimes list with the times participant went to sleep
    :rtype: (list)
    """    
    
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
      sleepData = sleepDataDateTime()   # Get sleep diary from excel sheet
      toSleepTimes = getToSleepDateTimes()      # Get sleep diary lights out times
      finishSleepTimes = getFinishSleepDateTimes()      # Get sleep diary got up times
        
      actualSleepTime = list() 
      actualAwakeTime = list()
      
      for i in range(len(toSleepTimes)):        # iterare through sleep times
          # Find too sleep times of the participant
          toSleepError = toSleepTimes[i] - datetime.timedelta(hours = 1)
          finishSleepError = finishSleepTimes[i] + datetime.timedelta(hours = 1)
          sleepRange = sleepData.loc[toSleepError:finishSleepError]
          sleepTimes = findSleepTime(sleepRange, actualSleepTime)
          
          # Analyze the sleep period of the participant to look for strange activty or lux
          hourBeforeWakeUp = finishSleepTimes[i] - datetime.timedelta(hours = 1)
          darkRange = sleepData.loc[sleepTimes[i]: hourBeforeWakeUp]
          #sleepTimeCheck(darkRange, meanActivity, meanLux, luxVariance, activityVariance)
          
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
