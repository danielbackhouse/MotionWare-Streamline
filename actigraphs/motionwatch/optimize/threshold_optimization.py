# Module: threshold_optimization
# Purpose: To optimize the threshold values within the algorithm
# Author: Daniel Backhouse and Alan Yan

import compute.error_analysis as err
import numpy as np
import time

def optimize_LO_times(sleep_study, LOprotocol):
    ws = 6
    ta = 20
    error_averages = []
    std_study = []
    count = []
    indices = []
    errors = []
    print('Begining calculation....')
    index = 0
    begin = time.time()
    for dm in range(3, 10):
        for zac in range(3,10):
            for zlc in range(10,45):
                for zmc in range(10,45):
                    try:
                        start = time.time()
                        LO, GU, SI, PL = sleep_study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta)
                        error_study, UP = err.get_error_study(LO,LOprotocol,PL)
                        error_per_participant = err.get_error_per_participant(LO, LOprotocol, PL)
                        
                        count.append(err.entries_over_fifteen(error_per_participant))
                        error_averages.append(err.total_error(error_study))
                        std_study.append(np.std(list(error_study.values()), ddof = 1))
                        indices.append([dm, zac, zlc, zmc])
                        print('[dm zac zlc zmc]')
                        print([dm, zac, zlc, zmc])
                        print('Iteration number:')
                        print(index)
                        print('Time of iteration:')
                        print(time.time() - start)
                        print('Total program runtime:')
                        print(time.time() - begin)
                        index += 1
                    except:
                        print('Error with calculation:')
                        print([dm, zac, zlc, zmc])
                        errors.append([dm, zac, zlc, zmc])
                        count.append(None)
                        error_averages.append(None)
                        std_study.append(None)
                        indices.append([dm, zac, zlc, zmc])
                    
    return error_averages, std_study, count, indices