# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:48:12 2019
Test Function
@author: dbackhou
"""
import pandas as pd
import MotionWareAnalysis

sleepDiaryDirectory  = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\Edited Sleep Diary\BT Sleep Diary Edited.xlsx'
rawDataDirectory = r'C:\Users\dbackhou\Desktop\Buying Time Study Copy\RAW data\Baseline\BT-074_Baseline.xlsx'

sleepDiary  = pd.read_excel(sleepDiaryDirectory, sheet_name = 'BT_074')
rawData = pd.read_excel(rawDataDirectory, skiprows = 12)

LO_times, GU_times = MotionWareAnalysis.findSleepPoint(sleepDiary, rawData)