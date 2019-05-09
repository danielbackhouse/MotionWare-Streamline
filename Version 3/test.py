# -*- coding: utf-8 -*-
"""
Created on Thu May  9 13:04:08 2019
Testing the no sleep diary  program
@author: danie
"""

import pandas as pd
import MotionWareAnalysis

sleepDiaryDirectory  = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\Edited Sleep Diary\BT Sleep Diary Edited.xlsx'
rawDataDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\RAW data\Baseline\BT-062_Baseline.xlsx'

sleepDiary  = pd.read_excel(sleepDiaryDirectory, sheet_name = 'BT_062')
rawData = pd.read_excel(rawDataDirectory, skiprows = 12)

LO_times, GU_times = MotionWareAnalysis.findSleepPoint(sleepDiary, rawData)