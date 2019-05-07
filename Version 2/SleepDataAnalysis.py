""" Title: SleepDataAnalysis
    Purpose: 
    Author: Alan Yan and Daniel Backhouse
"""
#Import extension libraries
import SheetManager
import MotionWareAnalysis
import datetime
import pandas as pd

activitySleepThreshold = 6
activityWakeThreshold = 2
requiredEpochsConsecutiveSleep = 10
requiredEpochsConsecutiveWake = 5
numberAboveThresholdAllowedSleep = 1
numberAboveThresholdAllowedWake = 2
epochLength = 1

sleepWakeList = list()
def findTimeDifferenceInMinutes(timeOne, timeTwo):
    #time one must be before time two
    minutes = 0
    while timeOne != timeTwo:
        timeOne += datetime.timedelta(minutes = 1)
        minutes += 1
    return minutes

def findSleepPoint(inBedPoint, rawDataFile, threshold = requiredEpochsConsecutiveSleep):
    sheetData = MotionWareAnalysis.sleepDataFormatter(rawDataFile)
    passedThreshold = False
    fellAsleepTime = inBedPoint
    while passedThreshold == False:    
        higherThanThresholdCount = 0
        for minutes in range(threshold):
            time = fellAsleepTime + datetime.timedelta(minutes = minutes)
            if int(sheetData.loc[time, 'Activity (MW counts)']) >=  activitySleepThreshold:
                higherThanThresholdCount += 1
        if higherThanThresholdCount <= numberAboveThresholdAllowedSleep:
            passedThreshold = True
            return fellAsleepTime
        fellAsleepTime += datetime.timedelta(minutes = epochLength)


def findWakePoint(outOfBedPoint, rawDataFile, threshold = requiredEpochsConsecutiveWake):
    sheetData = MotionWareAnalysis.sleepDataFormatter(rawDataFile)
    passedThreshold = False
    wokeUpTime = outOfBedPoint
    while passedThreshold == False:    
        higherThanThresholdCount = 0
        for minutes in range(threshold):
            time = wokeUpTime - datetime.timedelta(minutes = minutes)
            if int(sheetData.loc[time, 'Activity (MW counts)']) >=  activityWakeThreshold:
                higherThanThresholdCount += 1
        if higherThanThresholdCount <= numberAboveThresholdAllowedWake:
            passedThreshold = True
            return wokeUpTime
        wokeUpTime -= datetime.timedelta(minutes = epochLength)
        
def findActualSleepTime(inBedPoint, outOfBedPoint, rawDataFile):
    sheetData = MotionWareAnalysis.sleepDataFormatter(rawDataFile)
    fellAsleepTime = findSleepPoint(inBedPoint,rawDataFile)
    wokeUpTime = findWakePoint(outOfBedPoint, rawDataFile)
    sleepMinutes = 0
    actualSleepMinutes = 0
    while fellAsleepTime != (wokeUpTime+ datetime.timedelta(minutes = 1)):
        #TODO: Optimize this.
        total = int(sheetData.loc[fellAsleepTime,'Activity (MW counts)']) + \
                int(sheetData.loc[fellAsleepTime-datetime.timedelta(minutes = 1),'Activity (MW counts)'])*0.2 + \
                int(sheetData.loc[fellAsleepTime+datetime.timedelta(minutes = 1),'Activity (MW counts)'])*0.2 + \
                int(sheetData.loc[fellAsleepTime-datetime.timedelta(minutes = 2),'Activity (MW counts)'])*0.04 + \
                int(sheetData.loc[fellAsleepTime+datetime.timedelta(minutes = 2),'Activity (MW counts)'])*0.04
        if total <= 20:
            sleepWakeList.append(0)
            actualSleepMinutes += 1
        else:
            sleepWakeList.append(1)
        fellAsleepTime += datetime.timedelta(minutes = 1)
        sleepMinutes += 1
    percentSleep = actualSleepMinutes/sleepMinutes * 100 
    awakeMinutes = sleepMinutes-actualSleepMinutes
    percentAwake = 100-percentSleep
    return actualSleepMinutes, sleepMinutes, percentSleep, awakeMinutes, percentAwake        
        
def findSleepPercentage(inBedPoint, outOfBedPoint, actualSleepMinutes):
    timeInBed = findTimeDifferenceInMinutes(inBedPoint, outOfBedPoint)
    return actualSleepMinutes/timeInBed
def findSleepLatency(inBedPoint, fellAsleepTime):
    return findTimeDifferenceInMinutes(inBedPoint, fellAsleepTime)

def findBouts(inBedPoint, outOfBedPoint, rawDataFile):
    sheetData = MotionWareAnalysis.sleepDataFormatter(rawDataFile)
    fellAsleepTime = findSleepPoint(inBedPoint,rawDataFile)
    wokeUpTime = findWakePoint(outOfBedPoint, rawDataFile)
    sleepMinutes = 0
    actualSleepMinutes = 0
path = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\RAW data\Baseline\BT-001_Baseline.xlsx'
rawData = pd.read_excel(path, skiprows = 12)
#rawDataList = SheetManager.populateRawDataList()
sampleTime = datetime.datetime(2017, 4, 27, 23, 23)
sOne = datetime.datetime(2017, 4, 28, 6, 10)
actualSleep, perceivedSleep, percentSleep, awakeMinutes, percentAwake = findActualSleepTime(sampleTime,sOne,rawData)
percentSleep = findSleepPercentage(sampleTime,sOne,actualSleep)
print(sleepWakeList)