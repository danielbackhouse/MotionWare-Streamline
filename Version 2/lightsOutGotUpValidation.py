""" Title: lightsOutGotUpValidation
    Purpose: Compares the lights out times and got up times determined following
    the MotionWatch 8 Protocol and the MotionWareAnalysisProgram and plots
    the relative errors between the two
    Author: Daniel Backhouse and Alan Yan
"""

import MotionWareAnalysis
import SheetManager
import pandas as pd

rawDataDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\BT Sleep Analysis 2019-03-19.xlsx'

rawDataList = SheetManager.populateRawDataList()
diaryList = SheetManager.populateDiaryList()
diaryDataPairList = [rawDataList,diaryList]

lightsOutTimes, gotUpTimes = MotionWareAnalysis.findSleepPoint(diaryList[0], rawDataList[0])

