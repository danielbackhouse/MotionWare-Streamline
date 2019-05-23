# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:19:40 2019

@author: dbackhou
"""
import pandas as pd

def trimEnds(activity, dates, times, lux):
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
#TODO: make this throw error if data is not ordered correctly in csv
def trimDataThree(filePath, skiprows):
    file = pd.read_csv(filePath, skiprows = skiprows)
    dates = file.iloc[:,0].tolist()
    times = file.iloc[:,1].tolist()
    activity = file.iloc[:,2].tolist()
    lux = file.iloc[:,3].tolist()
    
    foundBack = False
    foundFront = False    
    trimEnds(activity, dates, times, lux)
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
        trimEnds(activity, dates, times, lux)
    return dates, times, lux, activity


def trimDataFour(filePath, skiprows):
    file = pd.read_csv(filePath, skiprows = skiprows)
    dates = file.iloc[:,0].tolist()
    times = file.iloc[:,1].tolist()
    activity = file.iloc[:,2].tolist()
    lux = file.iloc[:,3].tolist()
    
    zoneList, newList = findZoneList(activity)
    while zoneList[0][0] < 200 and zoneList[0][1]-zoneList[0][0] > 40:
        for x in range(zoneList[0][1]):
            pop(0, activity, dates, times, lux)
        zoneList, newList = findZoneList(activity)
    while zoneList[-1][1] > len(activity)-200 and zoneList[0][1]-zoneList[0][0] > 40:
        for x in range(len(activity)-zoneList[-1][0]):
            pop(-1, activity, dates, times, lux)
        zoneList, newList = findZoneList(activity)
    biggestLast = 0
    smallestFirst = len(activity)
    for x in newList:
        print(newList)
        average = (x[1]+x[0])/2
        if average < len(activity)/2:
            if x[1]> biggestLast:
                biggestLast = x[1]
        else:
            if x[0] < smallestFirst:
                smallestFirst = x[0]
    newActivity = activity[biggestLast: smallestFirst]
    newDates = dates[biggestLast: smallestFirst]
    newTimes = times[biggestLast: smallestFirst]
    newLux = lux[biggestLast: smallestFirst]              
    return newDates, newTimes, newLux, newActivity

def findZoneList(activity):
    zoneList = list(list())
    newList = list(list())
    zoneTwo = list()
    index = 0 
    counter = 0
    while index < len(activity):
        if activity[index] == 0:
            length, endIndex = findLengthOfZeroSection(activity, index)
            if length > 20:
                if counter:
                    stitched = False
                    if length > 800:
                        if index-zoneList[counter-1][1] < 100:
                            zoneList[counter-1][1] = endIndex
                    if index-zoneList[counter-1][1] < 5:
                        zoneList[counter-1][1] = endIndex
                    elif zoneList[counter-1][1]-zoneList[counter-1][0] > 800 and index-zoneList[counter-1][1] < 100:
                            zoneList[counter-1][1] = endIndex
                    elif zoneList[counter-1][1]-zoneList[counter-1][0] > 1500 and index-zoneList[counter-1][1] < 300:
                            zoneList[counter-1][1] = endIndex
                    else:
                        zoneTwo = []
                        zoneTwo.append(index)
                        zoneTwo.append(endIndex)
                        zoneList.append(zoneTwo)
                        counter += 1
                else:
                    zoneTwo.append(index)
                    zoneTwo.append(endIndex)
                    zoneList.append(zoneTwo)
                    counter += 1
            index = endIndex
        else:
            index += 1
    for x in zoneList:
        if x[1]-x[0]>400:
            newList.append(x)
    return zoneList, newList
def findLengthOfZeroSection(activity, index):
    counter = 0
    newIndex = index
    while newIndex < len(activity):
        if activity[newIndex] == 0:
            counter += 1
            newIndex += 1
        else:
            return counter, newIndex
    return counter, newIndex
def pop(index, activity, dates, times, lux):
    activity.pop(index)
    dates.pop(index)
    times.pop(index)
    lux.pop(index)
    return

dates, times, lux, activity = trimDataFour(r'C:\Users\dbackhou\Desktop\BT-001.csv', 12)

