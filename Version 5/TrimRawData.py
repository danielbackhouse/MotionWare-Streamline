# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:19:40 2019

@author: dbackhou
"""
import pandas as pd

def trimData(filePath):
    file = pd.read_csv(filePath, skiprows = 12)
    dates = file.iloc[:,0].tolist()
    times = file.iloc[:,1].tolist()
    activity = file.iloc[:,2].tolist()
    lux = file.iloc[:,3].tolist()
    beginningFound = True
    while beginningFound:
        if activity[0] == 0:
            pop(0, activity, dates, times, lux)
        else:
            zeroActivity = 0
            nonZeroActivity = 0
            for x in range(0, 20):
                if activity[x] <= 10:
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
                if activity[x] <= 10:
                    zeroActivity += 1
                else:
                    nonZeroActivity += 1
            if zeroActivity>nonZeroActivity:
                pop(-1, activity, dates, times, lux)
            else:
                endFound = False
    return dates, times, lux, activity

def trimDataTwo(filePath):
    file = pd.read_csv(filePath, skiprows = 12)
    dates = file.iloc[:,0].tolist()
    times = file.iloc[:,1].tolist()
    activity = file.iloc[:,2].tolist()
    lux = file.iloc[:,3].tolist()
    beginningFound = True
    while beginningFound:
        if activity[0] == 0:
            pop(0, activity, dates, times, lux)
        else:
            zeroActivity = 0
            nonZeroActivity = 0
            sectionsAbove = 0
            sectionsBelow = 0
            for x in range(0, 100):
                if activity[x] <= 10:
                    zeroActivity += 1
                else:
                    nonZeroActivity += 1
                if (x+1)%20 == 0:
                    if zeroActivity>nonZeroActivity:
                        sectionsBelow += 1
                    else:
                        sectionsAbove += 1
                    zeroActivity = 0
                    nonZeroActivity = 0
            if sectionsBelow != 0:
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
            sectionsAbove = 0
            sectionsBelow = 0
            for x in range(-100, 0):
                if activity[x] == 0:
                    zeroActivity += 1
                else:
                    nonZeroActivity += 1
                if (x+1)%20 == 0:
                    if zeroActivity>nonZeroActivity:
                        sectionsBelow += 1
                    else:
                        sectionsAbove += 1
                    zeroActivity = 0
                    nonZeroActivity = 0
            if sectionsBelow != 0:
                pop(-1, activity, dates, times, lux)
            else:
                endFound = False
    return dates, times, lux, activity
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
    
    zoneList = findZoneList(activity)
    
    return zoneList

def findZoneList(activity):
    zoneList = list(list())
    zoneTwo = list()
    index = 0 
    counter = 0
    while index < len(activity):
        if activity[index] == 0:
            length, endIndex = findLengthOfZeroSection(activity, index)
            if length > 30:
                if counter:
                    if index-zoneList[counter-1][1] < 10:
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
                    print(zoneList)
                    counter += 1
            index = endIndex
        else:
            index += 1
    return zoneList
def findLengthOfZeroSection(activity, index):
    counter = 0
    for newIndex in range(index, len(activity)):
        if activity[newIndex] == 0:
            counter += 1
        else:
            return counter, newIndex
    return counter, newIndex
def pop(index, activity, dates, times, lux):
    activity.pop(index)
    dates.pop(index)
    times.pop(index)
    lux.pop(index)
    return

def untrimmed_data(filePath, skiprows):
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
        
#zoneList = trimDataFour(r'C:\Users\dbackhou\Desktop\BT-001_Baseline.csv', 12)

