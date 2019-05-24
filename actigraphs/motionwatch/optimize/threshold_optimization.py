# Module: threshold_optimization
# Purpose: To optimize the threshold values within the algorithm
# Author: Daniel Backhouse and Alan Yan

import compute.error_analysis as err
import time
def optimize_LO_times(sleep_study, LOprotocol):
    ws = 10
    dm = 30
    error_averages = []
    
    while ws > 3:
        print('count')
        print(ws)
        while dm > 3:
            print('Optimizing... (kinda)')
            start = time.time()
            LOdates, GUdates, SleepAnalysisInfo, participant_list = sleep_study.get_in_bed_times(ws, dm)
            error_study, useful_participants = err.get_error_study(LOdates, LOprotocol, 
                                                                   participant_list)
            error_averages.append(err.total_error(error_study))
            dm = dm - 1
            end = time.time()
            print('Time elapsed')
            print(start-end)
            print(dm)
        dm = 30
        ws = ws - 1
    
    return error_averages
