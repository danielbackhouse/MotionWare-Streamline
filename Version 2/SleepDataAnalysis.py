""" Title: SleepDataAnalysis
    Purpose: To take the in bed point, the got out of bed point found from 
    motionWareAnalysis.py along with the raw data in order to calculate
    sleep and wake points, along with all the statistics found with the 
    MotionWare software.
    Author: Alan Yan and Daniel Backhouse
"""
#Import extension libraries
import MotionWareAnalysis
import datetime
import pandas as pd

#Threshold values used
activityThreshold = 6
requiredEpochsConsecutiveSleep = 10
requiredEpochsConsecutiveWake = 5
numberAboveThresholdAllowedSleep = 1
numberAboveThresholdAllowedWake = 2
epochLength = 1

def findTimeDifferenceInMinutes(timeOne, timeTwo):
    """Finds the difference in minutes between two date times. Time one MUST 
    be before Time two.
    
    :param: timeOne and timeTwo
    :return: Returns the number of minutes between two times
    :rtype(int)
    """
    minutes = 0
    while timeOne != timeTwo:
        timeOne += datetime.timedelta(minutes = 1)
        minutes += 1
    return minutes

def findSleepPoint(inBedPoint, formattedData, threshold = requiredEpochsConsecutiveSleep):
    """Finds the sleep point based on the inBedPoint, the formatted data and the
    threshold
    
    the inBedPoint is used as the basepoint to find the fellAsleepTime, 10 minutes
    after the fellAsleepTime are looked at and if the activity in that minute
    is greater than the threshold, then higherThanThresholdCount gains one.
    If there is more epochs above the number allowed in the 10 minutes,
    a minute is added to the fellAsleepTime, continues until a time is found.
    
    :param: inBedPoint, formattedData, threshold
    :return: Returns the time when the person fell asleep
    :rtype(datetime)
    """
    passedThreshold = False
    fellAsleepTime = inBedPoint
    while passedThreshold == False:
        higherThanThresholdCount = 0
        for minutes in range(threshold+1):
            time = fellAsleepTime + datetime.timedelta(minutes = minutes)
            if int(formattedData.loc[time, 'Activity (MW counts)']) >=  activityThreshold:
                higherThanThresholdCount += 1
        if higherThanThresholdCount <= numberAboveThresholdAllowedSleep:
            passedThreshold = True
            return fellAsleepTime
        fellAsleepTime += datetime.timedelta(minutes = epochLength)


def findWakePoint(outOfBedPoint, formattedData, threshold = requiredEpochsConsecutiveWake):
    """Finds the wake point based on the outOfBedPoint, the formatted data and the
    threshold
    
    Same idea as findSleepPoint, except different thresholds and working backwards
    from the out of bed point, only looking at 5 minute windows.
    
    :param: outOfBedPoint, formattedData, threshold
    :return: Returns the time when the person woke 
    :rtype(datetime)
    """
    passedThreshold = False
    wokeUpTime = outOfBedPoint
    while passedThreshold == False:
        higherThanThresholdCount = 0
        for minutes in range(threshold+1):
            time = wokeUpTime - datetime.timedelta(minutes = minutes)
            if int(formattedData.loc[time, 'Activity (MW counts)']) >=  activityThreshold:
                higherThanThresholdCount += 1
        if higherThanThresholdCount <= numberAboveThresholdAllowedWake:
            passedThreshold = True
            return wokeUpTime
        wokeUpTime -= datetime.timedelta(minutes = epochLength)

def findActualSleepTime(fellAsleepTime, wokeUpTime, activityArray):
    """Finds the actual sleep minutes, percent asleep, awake minutes, percent awake,
    and a sleepWakeList used for later analysis
    
    parses through the activityArray, which is an array with activity counts
    per epoch, uses the MotionWare guidelines to calculate a total activity for 
    each epoch in the sleep window. If the total is below the threshold, the
    minute is considered a sleep minute, if not, then it is an awake minute.
    
    :param: fellAsleepTime, wokeUpTime, activityArray
    :return: Returns the actual sleep minutes, awake minutes, assume sleep minutes,
    and percentages for awake and asleep.
    :rtype(int, int, float, int, float, list)
    """
    sleepMinutes = 0
    actualSleepMinutes = 0
    sleepWakeList = []
    for index in range(2,(len(activityArray)-2-1)):
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

def findSleepEfficiency(inBedPoint, outOfBedPoint, actualSleepMinutes):
    """Finds the sleep efficiency of the person, which is actual asleep over
    time in bed
    
    :param: inBedPoint, outOfBedPoint, actualSleepMinutes
    :return: Returns the sleep efficiency
    :rtype(float)
    """
    timeInBed = findTimeDifferenceInMinutes(inBedPoint, outOfBedPoint)
    return actualSleepMinutes/timeInBed*100

def findSleepLatency(inBedPoint, fellAsleepTime):
    """Finds the sleep latency of the person, which is how long it took
    for the person to fall asleep
    
    :param: inBedPoint, fellAsleepTime
    :return: Returns the minute difference between the two parameters
    :rtype(int)
    """
    return findTimeDifferenceInMinutes(inBedPoint, fellAsleepTime)

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
    meanSleepBoutLength = sum(sleepBoutLengths)/len(sleepBoutLengths)*60
    meanWakeBoutLength = sum(wakeBoutLengths)/len(wakeBoutLengths)*60
    
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
    activityList.pop(0)
    activityList.pop(0)
    activityList.reverse()
    activityList.pop(0)
    activityList.pop(0)
    activityList.pop(0)
    activityList.reverse()
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
    meanActivityPerNonZeroEpoch = totalActivity/nonZeroEpoch
    return totalActivity, meanActivityPerEpoch, meanActivityPerNonZeroEpoch

def activityToList(fellAsleepTime, wokeUpTime, formattedData):
    """Reads the formatted data and puts the activity data into a list to spee
    d up program.
    
    :param: fellAsleepTime, wokeUpTime, formattedData
    :return: Returns an array of activity data for that sleep period
    :rtype(list)
    """
    activityInNight = list()
    fellAsleepTime -= datetime.timedelta(minutes=2)
    wokeUpTime += datetime.timedelta(minutes = 2)
    while fellAsleepTime != (wokeUpTime + datetime.timedelta(minutes = 1)):
        activityInNight.append(formattedData.loc[fellAsleepTime, 'Activity (MW counts)'])
        fellAsleepTime += datetime.timedelta(minutes = 1)
    return activityInNight

def findFragmentationIndex(mobilePercent, boutsLessThanOnePercent):
    """Finds the fragmentation index, which is mobile % added to the immobile
    bouts less than one epoch %
    
    :param: mobilePercent and boutLessThanOnePercent
    :return: Returns the fragmentation index
    :rtype(float)
    """
    return mobilePercent + boutsLessThanOnePercent 

def findSleepAnalysisData(inBedPoint, outOfBedPoint, rawData):
    """This method finds all the sleep analysis data by calling the other 
    methods
    
    The method takes in the inBedPoint and outOfBedPoint found by 
    MotionWareAnalysis.py, along with the raw data to find all the sleep analysis
    data for one night. This is method to be called to find the sleep statistics,
    these are returned in a dictionary for ease of printing to an excel doc or
    onto console.
    
    :param: inBedPoint, outOfBedPoint, rawData
    :return: Returns a dictionary of all the sleep analysis stats
    :rtype(dictionary)
    """
    
    formattedData = MotionWareAnalysis.sleepDataFormatter(rawData)
    fellAsleepTime = findSleepPoint(inBedPoint, formattedData)
    wokeUpTime = findWakePoint(outOfBedPoint, formattedData)
    activityList = activityToList(fellAsleepTime, wokeUpTime, formattedData)
    timeInBedMinutes = findTimeDifferenceInMinutes(inBedPoint, outOfBedPoint)
    actualSleepMinutes, sleepMinutes, percentSleep, awakeMinutes, percentAwake, sleepWakeList = findActualSleepTime(fellAsleepTime, wokeUpTime, activityList)
    sleepEfficiency = findSleepEfficiency(inBedPoint, outOfBedPoint, actualSleepMinutes)
    sleepLatency = findSleepLatency(inBedPoint, fellAsleepTime)
    sleepBout, wakeBout, meanSleepBoutSeconds, meanWakeBoutSeconds = findBouts(sleepWakeList)
    mobileMinutes, immobileMinutes, mobilePercent, immobilePercent, mobileImmobileList = findMobileImmobileMinutes(activityList)
    immobileBout,  meanImmobileBoutSeconds, boutsLessThanOne, boutsLessThanOnePercent = findImmobileBout(mobileImmobileList)
    totalActivity, meanActivityPerEpoch, meanActivityPerNonZeroEpoch = findTotalActivity(activityList)
    fragmentationIndex = findFragmentationIndex(mobilePercent, boutsLessThanOnePercent)
    
    timeInBed = datetime.timedelta(minutes = timeInBedMinutes)
    sleepTime = datetime.timedelta(minutes = sleepMinutes)
    actualSleepTime = datetime.timedelta(minutes = actualSleepMinutes)
    awakeTime = datetime.timedelta(minutes = awakeMinutes)
    sleepLatencyTime = datetime.timedelta(minutes = sleepLatency)
    meanSleepBoutTime = datetime.timedelta(seconds = meanSleepBoutSeconds)
    meanWakeBoutTime = datetime.timedelta(seconds = meanWakeBoutSeconds)
    meanImmobileBoutTime = datetime.timedelta(seconds = meanImmobileBoutSeconds)
    
    print("Lights Out: ",  inBedPoint)
    print("Fell Asleep: ", fellAsleepTime)
    print("Woke Up: ", wokeUpTime)
    print("Got out of bed: ", outOfBedPoint)
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
    print("Mean Nonzero activity per epoch: ", round(meanActivityPerNonZeroEpoch,2))
    print("Fragmentation Index: ", round(fragmentationIndex,1))
    
    print("")
    print("")
    
    perNightDictionary = {
        "Lights Out": inBedPoint,
        "Fell Asleep": fellAsleepTime,
        "Woke Up": wokeUpTime,
        "Out Of Bed": outOfBedPoint,
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
path = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\RAW data\Baseline\BT-001_Baseline.xlsx'
rawData = pd.read_excel(path, skiprows = 12)
#rawDataList = SheetManager.populateRawDataList()

sampleSleep = datetime.datetime(2017, 4, 27, 23, 23)
samepleWake = datetime.datetime(2017, 4, 28, 6, 10)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)

sampleSleep = datetime.datetime(2017, 4, 28, 23, 16)
sampleWake = datetime.datetime(2017, 4, 29, 8, 16)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)

sampleSleep = datetime.datetime(2017, 4, 29, 23, 43)
sampleWake = datetime.datetime(2017, 4, 30, 8, 30)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)

sampleSleep = datetime.datetime(2017, 4, 30, 23, 17)
sampleWake = datetime.datetime(2017, 5, 1, 7, 18)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)

sampleSleep = datetime.datetime(2017, 5, 1, 23, 17)
sampleWake = datetime.datetime(2017, 5, 2, 7, 19)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)

sampleSleep = datetime.datetime(2017, 5, 2, 23, 11)
sampleWake = datetime.datetime(2017, 5, 3, 6, 43)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)

sampleSleep = datetime.datetime(2017, 5, 3, 23, 18)
sampleWake = datetime.datetime(2017, 5, 4, 7, 12)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)

sampleSleep = datetime.datetime(2017, 5, 4, 23, 27)
sampleWake = datetime.datetime(2017, 5, 5, 7, 13)
dictionary = findSleepAnalysisData(sampleSleep, sampleWake, rawData)
