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
origSleepDiaryDirectory  = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\Edited Sleep Diary\BT Sleep Diary.xlsx'
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
        rawSleepDiary = pd.ExcelFile(origSleepDiaryDirectory)
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
    participant_id = []
    rawDataAll = os.listdir(rawDataDirectory+ '\Baseline')
    for file in rawDataAll:
        if file.endswith('.xlsx') and findMatching(file):
            rawDataList.append(pd.read_excel(rawDataDirectory + '\Baseline\\' 
                                           + file, skiprows = 12))  
            participant_id.append(file[3:6])

    return rawDataList, participant_id

def populateDiaryList():
    """Creates and populates a list of all sleep diaries, in numerical order
              
    :param: none
    :return: list of all trials sleep diaries and list of sheet names
    :rtype(list)
    """
    diaryList = []
    xlsx = pd.ExcelFile(sleepDiaryDirectory)
    rawSleepDiary = pd.ExcelFile(xlsx)
    # Added sheet name list
    sheetNameList = []
    
    for sheetName in rawSleepDiary.sheet_names:
        if findMatching(sheetName):
            diaryList.append(pd.read_excel(sleepDiaryDirectory, sheet_name = sheetName))
            sheetNameList.append(sheetName)
    return diaryList, sheetNameList        


def populateSplitDiaryLists():
    """Creates and populates a list of finished and unfinished sleep diaries
    in numerical order
                 
    :param: none
    :return: 4 lists, filled sleep diaries, unfinished sleep diaries, their respective sheet names
    :rtype(list)
    """
    filledDiaryList = []
    incompleteDiaryList = []
    xlsx = pd.ExcelFile(origSleepDiaryDirectory)
    rawSleepDiary = pd.ExcelFile(xlsx)
    # Added sheet name list
    filledSheetNameList = []
    incompleteSheetNameList = []
    
    for sheetName in rawSleepDiary.sheet_names:
        if findMatching(sheetName):
            currentSheet = pd.read_excel(origSleepDiaryDirectory, sheet_name = sheetName)
            if currentSheet.iloc[1,1:15].isnull().sum() or currentSheet.iloc[5,1:15].isnull().sum():
                incompleteDiaryList.append(currentSheet)
                incompleteSheetNameList.append(sheetName)
                print('incomplete: ' + sheetName)
            else:
                filledDiaryList.append(currentSheet)
                filledSheetNameList.append(sheetName)   
                
    return filledDiaryList,incompleteDiaryList, filledSheetNameList, incompleteSheetNameList   







 