""" Title: SheetManager
    Purpose: To get sleep diaries and raw data of each participant for
    baseline, midline and final assesments and store both the sleep diary
    and raw data into pandas dataframe objects
    Author: Alan Yan and Daniel Backhouse
"""
#Import extension libraries
import os
import pandas as pd

#Directories for folder locations
#TODO: changes the diretories to be in the RunMotionWareProcessing program
rawDataDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\RAW data'
sleepDiaryDirectory  = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\Edited Sleep Diary\BT Sleep Diary Edited.xlsx'
diaryLightsOutIndex = 1;
diaryGotUpIndex = 5;


def findMatching(fileName):
    """Finds the matching patient in the diary or the raw data files
    
    Takes in a file name, and gets the patient number from it. If the fileName 
    comes from a raw data sheet, it will look for the number in the sleep diary
    and if the fileName comes from the sleep diary, it will look for the 
    raw data file with that number. fileName MUST be formatted as specified in 
    the read me document.
    
    :param: fileName
    :return: Returns either True or False depending on if the number is found
    :rtype(boolean)
    """
    numbers = fileName[3:6]
    
    if fileName.endswith('.xlsx'):
        rawSleepDiary = pd.ExcelFile(sleepDiaryDirectory)
        for sheetName in rawSleepDiary.sheet_names:         
            if sheetName.find(numbers) == 3:
                return True
    else:
        rawDataAll = os.listdir(rawDataDirectory+ '\Baseline')
        for file in rawDataAll:
            if file.find(numbers) == 3:
                return True
    return False
    
def populateRawDataList():
    """Creates and populates a list containing all the trials raw data 
    in numerical order
    
    
    :param: none
    :return: list of all trials raw data
    :rtype(list)
    """
    rawDataList = []
    rawDataAll = os.listdir(rawDataDirectory+ '\Baseline')
    
    for file in rawDataAll:
        if file.endswith('.xlsx') and findMatching(file):
            rawDataList.append(pd.read_excel(rawDataDirectory + '\Baseline\\' 
                                             + file, skiprows = 12))  
        
    return rawDataList

def populateDiaryList():
    """Creates and populates a list of all sleep diaries, in numerical order
        
    Looks at all         
    :param: none
    :return: list of all trials sleep diaries
    :rtype(list)
    """
    diaryList = []
    xlsx = pd.ExcelFile(sleepDiaryDirectory)
    rawSleepDiary = pd.ExcelFile(xlsx)
    # Added sheet name list
    sheetNameList = list()
    
    for sheetName in rawSleepDiary.sheet_names:
        if findMatching(sheetName):
            diaryList.append(pd.read_excel(sleepDiaryDirectory, sheet_name = sheetName))
            sheetNameList.append(sheetName)
    return diaryList, sheetNameList        