# Module: threshold_optimization
# Purpose: To optimize the threshold values within the algorithm
# Author: Daniel Backhouse and Alan Yan

import compute.error_analysis as err
import time
import numpy as np 

def optimize_LO_times(sleep_study, LOprotocol):
    ws = 4
    dm = 4
    zmc = 45
    zac = 5
    zlc = 30
    ta = 20
    
    error_averages = []
    std_study = []
    error_averages.append([])
    std_study.append([])
    ws = np.linspace(4,10,7)
    dm = np.linspace(4,30,27)
    WS, DM = np.meshgrid(ws, dm)    
    
    for rows in WS:
            LOdates, GUdates, SleepAnalysisInfo, participant_list = sleep_study.get_in_bed_times(
                    ws,dm,zmc, zac, zlc, ta)
            error_study, useful_participants = err.get_error_study(LOdates, LOprotocol, 
                                                                   participant_list)
            error_averages.append[index](err.total_error(error_study))
            std_study.append[index](np.std(list(error_study.values()), ddof = 1))

    
    return error_averages, std_study, WS, DM