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
def gradient_descent(study, protocol):
    interval = 1
    learning_rate = .2
    ws = 5
    dm = 5
    zmc  = 6
    zac = 4
    zlc = 4
    ta = 4
    totalGrad = 2
    iteration = 1
    
    error_averages = []
    std_study = []
    while iteration < 1000 and totalGrad > 1:
        print(iteration)
        ws = int(ws)
        dm = int(dm)
        zmc = int(zmc)
        zac = int(zac)
        zlc = int(zlc)
        ta = int(ta)
        
        LOdates, GUdates, SleepAnalysisInfo, participant_list = study.get_in_bed_times(
                    ws,dm,zmc, zac, zlc, ta)
        error_study, useful_participants = err.get_error_study(LOdates, protocol, 
                                                               participant_list)
        error_averages.append(err.total_error(error_study))
        std_study.append(np.std(list(error_study.values()), ddof = 1))
        
        start = time.time()

        WSahead = function(ws+interval, dm, zmc, zac, zlc, ta, study, protocol)
        WSbehind =  function(ws-interval, dm, zmc, zac, zlc, ta, study, protocol)
        WSMove = (WSahead-WSbehind)/(interval*2)
        
        DMahead = function(ws, dm+interval, zmc, zac, zlc, ta, study, protocol)
        DMbehind =  function(ws, dm-interval, zmc, zac, zlc, ta, study, protocol)
        DMMove = (DMahead-DMbehind)/(interval*2)
        
        ZMCahead = function(ws, dm, zmc+interval, zac, zlc, ta, study, protocol)
        ZMCbehind =  function(ws, dm, zmc-interval, zac, zlc, ta, study, protocol)
        ZMCMove = (ZMCahead-ZMCbehind)/(interval*2)
        
        ZACahead = function(ws, dm, zmc, zac+interval, zlc, ta, study, protocol)
        ZACbehind =  function(ws, dm, zmc, zac, zlc-interval, ta, study, protocol)
        ZACMove = (ZACahead-ZACbehind)/(interval*2)
        
        ZLCahead = function(ws, dm, zmc, zac, zlc+interval, ta, study, protocol)
        ZLCbehind =  function(ws, dm, zmc, zac, zlc-interval, ta, study, protocol)
        ZLCMove = (ZLCahead-ZLCbehind)/(interval*2)
        
        TAahead = function(ws, dm, zmc, zac, zlc, ta+interval, study, protocol)
        TAbehind =  function(ws, dm, zmc, zac, zlc, ta-interval, study, protocol)
        TAMove = (TAahead-TAbehind)/(interval*2)
        
        ws -= WSMove*learning_rate
        dm -= DMMove*learning_rate
        zmc -= ZMCMove*learning_rate
        zac -= ZACMove*learning_rate
        zlc -= ZLCMove*learning_rate
        ta -= TAMove*learning_rate
        
        totalGrad = (WSMove*learning_rate)**2 + (DMMove*learning_rate)**2 + (ZMCMove*learning_rate)**2 + (ZACMove*learning_rate)**2 + (ZLCMove*learning_rate)**2 + (TAMove*learning_rate)**2
        
        totalGrad = totalGrad**(1/2)
        end = time.time()
        print('Time elapsed')
        print(end-start)
        print(totalGrad)
        print(ws, dm, zmc, zac, zlc, ta, error_averages, std_study)
        print('')
        iteration += 1
    
    return ws, dm, zmc, zac, zlc, ta, error_averages, std_study
        
        
    
def function(ws, dm, zmc, zac, zlc, ta, study, protocol):
    LOdates, GUdates, SleepAnalysisInfo, participant_list = study.get_in_bed_times(
                    ws,dm,zmc, zac, zlc, ta)
    LO, GU, SI, PL = study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta)
    error_study, useful_participants = err.get_error_study(LO, protocol, PL)
    Y = err.total_error(error_study)
    return Y