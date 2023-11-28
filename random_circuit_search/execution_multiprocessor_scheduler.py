#
#  Module:  execution_multiprocessor_scheduler
#  Version: 0.0.1
#
#  Author:  Istvan Finta
#           https://tech.ronizongor.com
#
#  General notes: 
#           - this is an experimental code for experimental purposes. For production use refactoring is required,
#           - altough IBM has it's own RandomCircuit class this code serves as a part of wider generator, selector and optimizer 'framework'.                
#
#  Description:
#           This module is responsible for the parallel execution of the properly configured execution_manager modules.
#           The configuration covers the extent of the parallelism as well.
#           This commited version is shipped with an already applied preconfiguration.
#           


import multiprocessing
import time
import random
import execution_manager

exec_per_depth = 1000000
exec_group_base = int(time.time())
exec_group_id = exec_group_base * exec_per_depth
depth_start=7

if __name__ == '__main__':
    processes = [ ]
    for i in range(1,6):
        t = multiprocessing.Process(target=execution_manager.execution_function, kwargs={'reg_size':4, 'exec_group_id':exec_group_id, 'depth_start':(depth_start+i), 'depth_stop':(depth_start+1+i), 'exec_per_depth':exec_per_depth, 'exec_per_depth_start': (i*exec_per_depth), 'base_path':None})
        processes.append(t)

    for one_process in processes:
        one_process.start()

    for one_process in processes:
        one_process.join()

    print("Done!")
