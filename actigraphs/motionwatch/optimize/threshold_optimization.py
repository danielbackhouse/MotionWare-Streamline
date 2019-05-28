# Module: threshold_optimization
# Purpose: To optimize the threshold values within the algorithm
# Author: Daniel Backhouse and Alan Yan

import compute.error_analysis as err
import time
import numpy as np 

def optimize_LO_times(sleep_study, LOprotocol):
    ws = 10
    dm = 30
    zmc = 45
    zac = 5
    zlc = 30
    ta = 20
    
    error_averages = []
    std_study = []
    while ws > 3:
        print('count')
        print(ws)
        while dm > 3:
            print('Optimizing... (kinda)')
            start = time.time()
            LOdates, GUdates, SleepAnalysisInfo, participant_list = sleep_study.get_in_bed_times(
                    ws,dm,zmc, zac, zlc, ta)
            error_study, useful_participants = err.get_error_study(LOdates, LOprotocol, 
                                                                   participant_list)
            error_averages.append(err.total_error(error_study))
            std_study.append(np.std(list(error_study.values()), ddof = 1))
            dm = dm - 1
            end = time.time()
            print('Time elapsed')
            print(start-end)
            print(dm)
        dm = 30
        ws = ws - 1
    
    return error_averages, std_study

def gradient_descent(X, max_iterations, learning_rate, study, protocol):
    error = function(X, study, protocol)
    
    for i in range(0, max_iterations):
        print('Iteration number:')
        print(i)

        
    return error, X

def gradient(X, learning_rate, study, protocol):
    Xahead = X+learning_rate    deltaX = Xahead - X
    Yahead = function(X, study, protocol)
    Y = function(X, study, protocol)
    partial_derivatives = (Yahead - Y)/deltaX  #X will be made into a vector containing the weights
    
    return partial_derivatives
    
def function(X, study, protocol):
    LO, GU, SI, PL = study.get_in_bed_times(X)
    error_study, useful_participants = err.get_error_study(LO, protocol, PL)
    Y = err.total_error(error_study)
    return Y