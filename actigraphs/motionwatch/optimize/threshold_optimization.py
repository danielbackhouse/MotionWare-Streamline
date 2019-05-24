# Module: threshold_optimization
# Purpose: To optimize the threshold values within the algorithm
# Author: Daniel Backhouse and Alan Yan

import compute.error_analysis as err
import create.Study as study

def optimize_LO_times(sleep_study, LOprotocol):
    
    LOdates, GUdates, SleepAnalysisInfo, participant_list = sleep_study.get_in_bed_times()

    error_study, useful_participants = err.get_error_study(LOdates, LOprotocol, participant_list)
    error_average = err.total_error(error_study)
    
    return(error_average)
