""" Title: SleepDataAnalysis
    Purpose: To take the in bed point, the got out of bed point found from 
    motionWareAnalysis.py along with the raw data in order to calculate
    sleep and wake points, along with all the statistics found with the 
    MotionWare software.
    Author: Alan Yan and Daniel Backhouse
"""
#Import extension libraries
import datetime

#Threshold values used
activityThreshold = 6
requiredEpochsConsecutiveSleep = 10
requiredEpochsConsecutiveWake = 5
minutesAboveThresholdAllowedSleep = 1
minutesAboveThresholdAllowedWake = 2
epochLength = 1
errors = 0

def findSleepPoint(activity, datetime, minutesRange = requiredEpochsConsecutiveSleep):
    """Finds the sleep point for one sleep period
    
    Uses the activity and datetime arrays to look 10 minutes ahead of a time, 
    starting with the in bed time, if more minutes are above the allowed threshold, 
    then it moves one miunte later and tried again, until there is a 10 minute window
    after a time, where the minutes above the activity threshold
    are less than or equal to the number of minutes threshold
    
    :param: activity, datetime, minutesRange
    :return: Returns the sleep point as a datetime and the index for the activity list
    :rtype(datetime, int)
    """
    passedThreshold = False
    index = 0
    while passedThreshold == False and index < len(activity)-10:
        higherThanThresholdCount = 0
        for minutes in range(minutesRange+1):
            if activity[index + minutes] >=  activityThreshold:
                higherThanThresholdCount += 1
        if higherThanThresholdCount <= minutesAboveThresholdAllowedSleep:
            passedThreshold = True
            return datetime[index], index
        index += 1
        if index == len(activity)-10:
            return 'N/A', 'N/A'
        
def findWakePoint(activity, datetime, minutesThreshold = requiredEpochsConsecutiveWake):
    """Finds the wake point for one sleep period
    
    Uses the activity and datetime arrays to look 5 minutes before a time, starting
    with the out of bed time, if more minutes are above the threshold, then
    it moves one miunte earlier and tried again, until there is a 5 minute window
    before a time, where the number minutes above the activity threshold
    are less than or equal to the number of minutes threshold
    
    
    :param: activity, datetime, minutesRange
    :return: Returns the wake point as a datetime and the index for the activity list
    :rtype(datetime, int)
    """
    passedThreshold = False
    index = len(activity)-1
    while passedThreshold == False and index >= 5:
        higherThanThresholdCount = 0
        for minutes in range(minutesThreshold+1):
            if activity[index - minutes] >=  activityThreshold:
                higherThanThresholdCount += 1
        if higherThanThresholdCount <= minutesAboveThresholdAllowedWake:
            passedThreshold = True
            return datetime[index-10], index-10
        index -= 1
        if index == 4:
            return 'N/A', 'N/A'


def findActualSleepTime(activityArray):
    """Finds the actual sleep minutes, percent asleep, awake minutes, percent awake,
    and a sleepWakeList used for later analysis
    
    parses through the activityArray, which is an array with activity counts
    per epoch, uses the MotionWare guidelines to calculate a total activity for 
    each epoch in the sleep window. If the total is below the threshold, the
    minute is considered a sleep minute, if not, then it is an awake minute.
    
    :param: activityArray
    :return: Returns the actual sleep minutes, awake minutes, assume sleep minutes,
    and percentages for awake and asleep.
    :rtype(int, int, float, int, float, list)
    """
    sleepMinutes = 0
    actualSleepMinutes = 0
    sleepWakeList = []
    for index in range(2,(len(activityArray)-2)):
        total = activityArray[index-2]*0.04 + activityArray[index-1]*0.2 + \
                activityArray[index] + activityArray[index+1]*0.2 + activityArray[index+2]*0.04
        if total <= 20:
            sleepWakeList.append(0)
            actualSleepMinutes += 1
        else:
            sleepWakeList.append(1)
        sleepMinutes += 1
        
        
    percentSleep = actualSleepMinutes/sleepMinutes * 100
    awakeMinutes = sleepMinutes-actualSleepMinutes
    percentAwake = 100-percentSleep
    return actualSleepMinutes, sleepMinutes, percentSleep, awakeMinutes, percentAwake, sleepWakeList

def findSleepEfficiency(timeInBed, actualSleepMinutes):
    """Finds the sleep efficiency
    
    Sleep efficiency is the actual sleep minutes over the time in bed
    
    :param: timeInBed and the actualSleepMinutes
    :return: sleep efficiency %
    :rtype(float)
    """
    return actualSleepMinutes/timeInBed*100

def findBouts(sleepWakeList):
    """Finds the number of sleep and awake bouts, along with the
    mean length for both
    
    Uses the sleep wake list, which is an array of 1s and 0s, to find 
    continuous sections of sleeping and awake periods, which is what a bout is.
    After the for loop, checks the last element of the list, which is the
    waking time to add the last bout.
    
    :param: sleepWakeList
    :return: returns the number of sleeping and awake bouts, along with
    their mean lengths
    :rtype(int, int, float, float)
    """
    sleepBout = 0
    wakeBout = 0
    wakeOrSleep = -1
    sleepBoutLengths = []
    wakeBoutLengths = []
    boutCount = 0
    for item in sleepWakeList:
        if item:
            if wakeOrSleep == 0:
                sleepBoutLengths.append(boutCount)
                sleepBout += 1
                boutCount = 0
            wakeOrSleep = 1
        else:
            if wakeOrSleep == 1:
                wakeBoutLengths.append(boutCount)
                wakeBout += 1
                boutCount = 0
            wakeOrSleep = 0
        boutCount += 1
    if sleepWakeList[-1]:
        if wakeOrSleep  == 1:
            wakeBoutLengths.append(boutCount)
            wakeBout += 1
    else:
        if wakeOrSleep == 0:
            sleepBoutLengths.append(boutCount)
            sleepBout += 1
    if len(sleepBoutLengths):     
        meanSleepBoutLength = sum(sleepBoutLengths)/len(sleepBoutLengths)*60
    else:
        meanSleepBoutLength = 0
    if len(wakeBoutLengths):
        meanWakeBoutLength = sum(wakeBoutLengths)/len(wakeBoutLengths)*60
    else:
        meanWakeBoutLength = 0
    
    return sleepBout, wakeBout, meanSleepBoutLength, meanWakeBoutLength
            
def findMobileImmobileMinutes(activityList):
    """Finds the mobile and immmobile minutes, along with their percentages
    and returns a mobile immobile list, similar to the sleep wake list
    
    The activity list is shortened to take two elements off the front and 
    three from the back, since there is no more activity total per epoch calculations.
    The activity list is now from the start of sleep to the minute before waking up
    The mobile minutes are then counted based on a threshold, same with immobile
    and then percentages are easily calculated.
    
    :param: activityList
    :return: Returns mobile and immobile minutes, along with their percentages,
    and a mobile immobile list
    :rtype(int, int, float, float, list)
    """
    mobileMinutes = 0
    immobileMinutes = 0
    mobileImmobileList = []
    for item in activityList:
        if item >= 4:
            mobileMinutes += 1
            mobileImmobileList.append(1)
        else:
            immobileMinutes += 1
            mobileImmobileList.append(0)
    
    mobilePercent = mobileMinutes/(mobileMinutes + immobileMinutes)*100
    immobilePercent = immobileMinutes/(mobileMinutes + immobileMinutes)*100
    return mobileMinutes, immobileMinutes, mobilePercent, immobilePercent, mobileImmobileList

def findImmobileBout(mobileImmobileList):
    """Finds more statistics on the immobile bout information.
    
    Runs through the mobile immobile list to count immobile bouts and calculate
    mean immobile bout length and immobile bout less than or equal to one
    minute, and the percentage of those over all immobile bouts.
    
    :param: mobileImmobileList
    :return: Returns number of immobile bouts, the mean length of immobile bouts,
    the immobile bouts less than one minute and the percentage of those versus the
    total immobile bout count
    :rtype(int, float, int, float)
    """
    immobileBout = 0
    immobileBoutLengths = []
    boutCount = 0
    mobileOrImmobile = -1
    boutsLessThanOne = 0
    
    for item in mobileImmobileList:
        if item:
            if mobileOrImmobile == 0:
                immobileBoutLengths.append(boutCount)
                immobileBout += 1
                boutCount = 0
            mobileOrImmobile = 1
        else:
            if mobileOrImmobile == 1:
                boutCount = 0
            mobileOrImmobile = 0
        boutCount += 1
    if mobileImmobileList[-1] == 0:
        if mobileOrImmobile == 0:
            immobileBoutLengths.append(boutCount)
            immobileBout += 1
    for item in immobileBoutLengths:
        if item <= 1:
            boutsLessThanOne += 1
    boutsLessThanOnePercent = boutsLessThanOne/immobileBout*100
    
    meanImmobileBoutLength = sum(immobileBoutLengths)/len(immobileBoutLengths)*60
    
    return immobileBout,  meanImmobileBoutLength, boutsLessThanOne, boutsLessThanOnePercent
        
def findTotalActivity(activityList):
    """Finds the total activity over the assumes sleep period, as well as the 
    mean avtivity per epoch and mean activity per non zero epoch
    
    :param: activityList
    :return: Returns the total activity, the mean activity per epoch and the
    mean activity per non zero epoch
    :rtype(float)
    """
    nonZeroEpoch = 0
    totalActivity = sum(activityList)
    meanActivityPerEpoch = totalActivity/len(activityList)
    for item in activityList:
        if item:
            nonZeroEpoch += 1
    if nonZeroEpoch:
        meanActivityPerNonZeroEpoch = totalActivity/nonZeroEpoch
    else:
        meanActivityPerNonZeroEpoch = 0
    return totalActivity, meanActivityPerEpoch, meanActivityPerNonZeroEpoch

def findFragmentationIndex(mobilePercent, boutsLessThanOnePercent):
    """Finds the fragmentation index, which is mobile % added to the immobile
    bouts less than one epoch %
    
    :param: mobilePercent and boutLessThanOnePercent
    :return: Returns the fragmentation index
    :rtype(float)
    """
    return mobilePercent + boutsLessThanOnePercent 

def findSleepAnalysisData(activity, datetimes):
    """This method finds all the sleep analysis data by calling the other 
    methods
    
    The method takes in the activity list and datetimes list found by 
    FindInBedTimes.py, to find all the sleep analysis data for one sleep period. 
    This is the method to be called to find the sleep statistics,
    these are returned in a dictionary for ease of printing to an excel doc or
    onto console. Also includes error management and warnings.
    
    :param: activity, datetimes
    :return: Returns a dictionary of all the sleep analysis stats
    :rtype(dictionary)
    """
    global errors
    
    #Calcs
    trimmedActivity = activity[10:-10]
    sleepActivity = activity[8:-8]
    fellAsleepTime, sleepIndex = findSleepPoint(activity[10:], datetimes)
    wokeUpTime, wakeIndex = findWakePoint(activity[:-10], datetimes)
    
    #ERRORS
    if wokeUpTime == 'N/A' or fellAsleepTime == 'N/A':
        print("ERROR: CANNOT FIND SLEEP OR WAKE POINT BASED ON DATA")
        print("")
        print("Info:")
        errors +=1
        print('Activity: ' ,activity)
        print('Acitivty List Length: ', len(activity))
        print('Start: ', datetimes[0])
        print('End', datetimes[-1])
        #input("To Skip and Continue, Press Enter")
        
        return -1
    
    #Calcs
    timeInBedMinutes = len(trimmedActivity)-1
    actualSleepMinutes, sleepMinutes, percentSleep, awakeMinutes, percentAwake, sleepWakeList = findActualSleepTime(sleepActivity[sleepIndex+2-2:wakeIndex+2+2])
    sleepEfficiency = findSleepEfficiency(timeInBedMinutes, actualSleepMinutes)
    sleepLatency = sleepIndex
    sleepBout, wakeBout, meanSleepBoutSeconds, meanWakeBoutSeconds = findBouts(sleepWakeList)
    mobileMinutes, immobileMinutes, mobilePercent, immobilePercent, mobileImmobileList = findMobileImmobileMinutes(trimmedActivity[sleepIndex: wakeIndex])
    immobileBout,  meanImmobileBoutSeconds, boutsLessThanOne, boutsLessThanOnePercent = findImmobileBout(mobileImmobileList)
    totalActivity, meanActivityPerEpoch, meanActivityPerNonZeroEpoch = findTotalActivity(trimmedActivity[sleepIndex:wakeIndex])
    fragmentationIndex = findFragmentationIndex(mobilePercent, boutsLessThanOnePercent)
    
    #Integers to Time
    timeInBed = datetime.timedelta(minutes = timeInBedMinutes)
    sleepTime = datetime.timedelta(minutes = sleepMinutes)
    actualSleepTime = datetime.timedelta(minutes = actualSleepMinutes)
    awakeTime = datetime.timedelta(minutes = awakeMinutes)
    sleepLatencyTime = datetime.timedelta(minutes = sleepLatency)
    meanSleepBoutTime = datetime.timedelta(seconds = meanSleepBoutSeconds)
    meanWakeBoutTime = datetime.timedelta(seconds = meanWakeBoutSeconds)
    meanImmobileBoutTime = datetime.timedelta(seconds = meanImmobileBoutSeconds)
    
    #ERRORS
    if meanWakeBoutSeconds == 0:
        print("Warning: There are no wake bouts, this is possible, but likely a trimming error")
        print('SleepWakeList: ', sleepWakeList)
        print('Start: ', datetimes[0])
        print('End', datetimes[-1])
        #answer = input("Click Enter to continue, 'N' to skip and continue")
        #if(answer == 'N'):
         #   errors += 1
         #   return -1
    if meanActivityPerNonZeroEpoch == 'N/A':
        print("Warning: No Nonzero Epoches")
        #answer = input("Click Enter to continue, 'N' to skip and continue")
        #if(answer == 'N'):
        #    errors += 1
        #    return -1    
    if meanSleepBoutSeconds == 0:
        print("ERROR: THERE IS NO SLEEP BOUTS, THIS SHOULD NEVER HAPPEN")
        print("")
        print("Info:")
        errors += 1
        print('Activity: ' ,activity)
        print('Acitivty List Length: ', len(activity))
        print('Start: ', datetimes[0])
        print('End', datetimes[-1])
        #input("To Skip and Continue, Press Enter")
        return -1
    if sleepEfficiency > 100 or percentSleep > 100 or percentAwake > 100 or mobilePercent > 100 or immobilePercent > 100:
        print("ERROR: PERCENTAGE OVER 100, SHOULD NEVER HAPPEN")
        errors += 1
        #input("To Skip and Continue, Press Enter")
        return -1
    
    #Output
    print("Lights Out: ",  datetimes[0])
    print("Fell Asleep: ", fellAsleepTime)
    print("Woke Up: ", wokeUpTime)
    print("Got out of bed: ", datetimes[-1])
    print("Time in bed: ", timeInBed)
    print("Assumed sleep: ", sleepTime)
    print("Actual sleep time: " , actualSleepTime)
    print("Actual sleep %: " , round(percentSleep, 1))
    print("Actual wake time: " , awakeTime)
    print("Actual wake %: " , round(percentAwake,1))
    print("Sleep efficiency %: " , round(sleepEfficiency,1))
    print("Sleep latency: " , sleepLatencyTime)
    print("Sleep bouts", sleepBout)
    print("Wake bouts", wakeBout)
    print("Ave sleep bouts", meanSleepBoutTime)
    print("Ave wake bouts", meanWakeBoutTime)
    print("immobile mins: ", immobileMinutes)
    print("immobile %: ", round(immobilePercent,1))
    print("mobile mins:", mobileMinutes )
    print("mobile %: ", round(mobilePercent,1))
    print("Immobile bouts: ", immobileBout)
    print("mean immobile bout: ", meanImmobileBoutTime)
    print("Immobile bouts <= 1 ", boutsLessThanOne)
    print("Immobile bouts <= 1% ", round(boutsLessThanOnePercent,1))
    print("Total Activity: ", totalActivity )
    print("Mean Activity per epoch: ", round(meanActivityPerEpoch,2))
    if meanActivityPerNonZeroEpoch == 'N/A':
        print("Mean Nonzero activity per epoch: ", meanActivityPerNonZeroEpoch)
    else:
        print("Mean Nonzero activity per epoch: ", round(meanActivityPerNonZeroEpoch,2))
    print("Fragmentation Index: ", round(fragmentationIndex,1))
    print("")
    print("")   
    print('Number of Incomplete Days Due to Error In Data: ',errors)
    
    #Actual Returned
    perNightDictionary = {
        "Lights Out": datetimes[0],
        "Fell Asleep": fellAsleepTime,
        "Woke Up": wokeUpTime,
        "Out Of Bed": datetimes[-1],
        "Time in bed": timeInBed,
        "Assumed sleep": sleepTime,
        "Actual sleep time": actualSleepTime,
        "Actual sleep %:": percentSleep,
        "Actual wake time": awakeTime,
        "Actual wake %:": percentAwake,
        "Sleep efficiency %": sleepEfficiency,
        "Sleep latency": sleepLatencyTime,
        "Sleep bouts": sleepBout,
        "Wake bouts": wakeBout,
        "Mean Sleep bouts": meanSleepBoutTime,
        "Mean Wake bouts": meanWakeBoutTime,
        "Immobile mins": immobileMinutes,
        "Immobile %": immobilePercent,
        "Mobile mins": mobileMinutes ,
        "Mobile %": mobilePercent,
        "Immobile bouts": immobileBout,
        "Mean Immobile bout": meanImmobileBoutTime,
        "Immobile bouts <= 1": boutsLessThanOne,
        "Immobile bouts <= 1%": boutsLessThanOnePercent,
        "Total Activity": totalActivity,
        "Mean Activity Per Epoch": meanActivityPerEpoch,
        "Mean Nonzero Activity Per Epoch": meanActivityPerNonZeroEpoch,
        "Fragmentation Index": fragmentationIndex
    }
    return perNightDictionary

#TEST with BT-001 First 8 days
def convert_date_time(dates, times):
    """ Converts date and time arrays (stored as strings) and combines them 
    both to form one datetime array
    """
    datetime_arr = []
    for i  in range(0, len(dates)):
        datetimeString = dates[i] + ' ' + times[i]
        datetime_arr.append(datetime.datetime.strptime(datetimeString, '%Y-%m-%d %I:%M:%S %p'))
        
    return datetime_arr