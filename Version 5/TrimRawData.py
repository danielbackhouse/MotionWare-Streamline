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
def trimData(filePath, skiprows):
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

