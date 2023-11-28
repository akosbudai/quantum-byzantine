#
#  Module:  execution_manager
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
#           This module is the main configuration module and the entry point to the random circuit generation and pre-selection.
#           It is possible to explicitly set:
#           - the register size,
#           - start depth,
#           - stop depth,
#           - generation/execution cycles on given depth.
#
#           Additionally, via this module one implicitly can set the different output files belong to different execution settings and measurements:
#           - storage for generated circuit descriptor,
#           - storage for generated circuit result vector,
#           - storage for computed fidelities,
#           - acceptance fidelity thresholds.
#           
#           Therefore this module is the configurable building block of parallel executions (see the description of execution_multiprocessor_scheduler).
# 

from randomized_quantum_circuit.randomized_quantum_circuit import *
from circuit_vector_converter.circuit_vector_converter import *
from metrics.rv2metrics import *
from storage_handlers.storage_handlers import *
from randomized_quantum_circuit_visualizer.circuit_visualizer import *

import time
import math
from pathlib import Path

test_mode = False

#
#  This is a global function, handle accordingly.
#
def execution_function(**confargs):

    reg_size = 4
    depth_start = 4
    depth_stop = 14
    exec_per_depth = 1000
    exec_per_depth_start = 0

    if confargs["reg_size"] != None:
        reg_size = confargs["reg_size"]

    if confargs["depth_start"] != None:
        depth_start = confargs["depth_start"]
    
    if confargs["depth_stop"] != None:
        depth_stop = confargs["depth_stop"]
    
    if confargs["exec_per_depth"] != None:
        exec_per_depth = confargs["exec_per_depth"]
    
    if confargs["exec_per_depth_start"] != None:
        exec_per_depth = confargs["exec_per_depth_start"]

    number_of_depths = depth_stop - depth_start

    #
    #  This generates a subfolder and a base for composite_id
    #
    if confargs["exec_group_id"] != None:
        execution_group_identifier = confargs["exec_group_id"]
    else:
        execution_group_identifier = int(time.time())

    power = math.ceil(math.log((number_of_depths * exec_per_depth), 10))
    correction_multiplier = math.pow(10, power)
    composite_id = execution_group_identifier * correction_multiplier
    composite_id = int(composite_id)

    execution_group_identifier = str(execution_group_identifier)
    

    #
    #  The implicit, measurement and storage related settings are available from here.
    #  The else branch represents the default settings
    #
    if confargs["base_path"] != None:
        base_path = confargs["base_path"]
    else:
        base_path = "stored_results__local/"


    circ_path = "01_circuit_descriptors/"
    rv_path = "03_result_vectors/"
    afmet_path = "04_metrics/afmet/"
    afamet_path = "04_metrics/afamet/"
    qmmet_path = "04_metrics/qmmet/"
    figures_path = "05_figures/"


    path_fidkv_circ = base_path + circ_path + execution_group_identifier + "/"
    path_fidkv_rv = base_path + rv_path + execution_group_identifier + "/"
    path_fidkv_afmet = base_path + afmet_path + execution_group_identifier + "/"
    path_fidkv_afamet = base_path + afamet_path + execution_group_identifier + "/"
    path_fidkv_qmmet = base_path + qmmet_path + execution_group_identifier + "/"
    path_fikdv_figures = base_path + figures_path + execution_group_identifier + "/"

    #
    #  Storage path creation for circuit descriptors
    #
    p = Path(path_fidkv_circ)
    p.mkdir(exist_ok=True, parents=True)

    #
    #  Storage path creation for result vectors
    #
    p = Path(path_fidkv_rv)
    p.mkdir(exist_ok=True, parents=True)

    #
    #  Storage path creation for Aharonov fidelity
    #
    p = Path(path_fidkv_afmet)
    p.mkdir(exist_ok=True, parents=True)

    #
    #  Storage path creation for Aharonov apostrophe fidelity
    #
    p = Path(path_fidkv_afamet)
    p.mkdir(exist_ok=True, parents=True)

    #
    #  Storage path creation for Quantum mechanical fidelity
    #
    p = Path(path_fidkv_qmmet)
    p.mkdir(exist_ok=True, parents=True)
    p = Path(path_fikdv_figures)
    p.mkdir(exist_ok=True, parents=True)

    cv = CircuitVisualizer()
    cv.set_path(path_fikdv_figures)

    #
    #  This file provides a quick summary/overview about the execution results without the need to dig through into the details in the individual result files.
    #
    ficd_ex = FileIOforIdDataKVPairs(path_fidkv_circ + "exec_summary.txt")

    for i in range(depth_start, depth_stop):

        path_fidkv_circ_used = path_fidkv_circ + "d_{}".format(i) + ".txt"
        path_fidkv_rv_used = path_fidkv_rv + "d_{}".format(i) + ".txt"
        path_fidkv_afmet_used = path_fidkv_afmet + "d_{}".format(i) + ".txt"
        path_fidkv_afamet_used = path_fidkv_afamet + "d_{}".format(i) + ".txt"
        path_fidkv_qmmet_used = path_fidkv_qmmet + "d_{}".format(i) + ".txt"


        ficd = FileIOforCircDescriptor(path_fidkv_circ_used)
        fidkv_rv = FileIOforIdDataKVPairs(path_fidkv_rv_used)
        fidkv_afmet = FileIOforIdDataKVPairs(path_fidkv_afmet_used)
        fidkv_afamet = FileIOforIdDataKVPairs(path_fidkv_afamet_used)
        fidkv_qmmet = FileIOforIdDataKVPairs(path_fidkv_qmmet_used)

        #
        #  This block is for visual feedback purposes about the progress.
        #
        progress_unit = exec_per_depth / 100;
        progress_keeper = 0
        progress_actual = 0

        print("Progress status of depth " + str(i) + " is: " + str(progress_keeper) + "% \n")

        for j in range(exec_per_depth_start, (exec_per_depth_start + exec_per_depth)):

            # Status check purposes
            progress_actual = math.floor(j/progress_unit)
            if progress_keeper < progress_actual:
                progress_keeper = progress_actual
                print("Progress status of depth " + str(i) + " is: " + str(progress_keeper) + "% \n")

            
            rqc = RandomizedQuantumCircuit(reg_size, i)
            rqc.setVerboseOff()
            rqc.constructCircuit()

            circ = rqc.getConstructedRandomCircuit()

            rc = RandomCircuit(circ, 0)
            converter = CircuitVectorConverter()
            result_vector = converter.convert(rc, 'COMP')

            computer = VectorMetricsComputer()

            iv = InputVector(result_vector)
            return_value_afmet = computer.compute(iv, 'AFMET')

            return_value_afamet = computer.compute(iv, 'AFAMET')

            return_value_qmmet = computer.compute(iv, 'QMMET')

            #
            #  This is the decision part: 
            #
            #       only that circuits will be kept for further investigation, which pass the condition expressed below.
            #
            #  Of course this condition can be cutomized according to specific needs.
            #
            if (return_value_afmet > 0.93) or (return_value_afamet > 0.93) or (return_value_qmmet > 0.93):

                #
                #   Next to file savings feedback is also displayed on the terminal.
                #
                print("\n" + str(composite_id) + "\n")
                print("AFMET, result: ", return_value_afmet)
                print("AFAMET, result: ", return_value_afamet)
                print("QMMET, result: ", return_value_qmmet)

                ficd_ex.insert_data(str("execution identifier"), str(composite_id))
                ficd_ex.insert_data("AFMET, result ", str(return_value_afmet))
                ficd_ex.insert_data("AFAMET, result ", str(return_value_afamet))
                ficd_ex.insert_data("QMMET, result ", str(return_value_qmmet))


                ficd.insert_data(composite_id, rqc.getConstRandCirRepresentation())

                fidkv_rv.insert_data(composite_id, result_vector)

                fidkv_afmet.insert_data(composite_id, return_value_afmet)
                fidkv_afamet.insert_data(composite_id, return_value_afamet)
                fidkv_qmmet.insert_data(composite_id, return_value_qmmet)

                cv.circuit_drawer(str(composite_id), circ)

            composite_id = composite_id + 1

            #
            #  From here reset takes place
            #
            return_value_qmmet = None
            return_value_afamet = None
            return_value_afmet = None
            iv = None
            computer = None
            result_vector = None
            converter = None
            rc = None
            circ = None
            rqc.clearConstRandCirRepresentation()
            rqc = None
            del rqc
            
            
        fidkv_qmmet = None
        fidkv_afamet = None
        fidkv_afmet = None
        fidkv_rv = None
        ficd = None

        del fidkv_qmmet
        del fidkv_afamet
        del fidkv_afmet
        del fidkv_rv
        del ficd


#
#  Local test asset
#  A wrapper class is applied for module related test functions to avoid name collisions.
#
class TestWrapperEM:
    def __init__(self):
        pass

    def test_function(self):

        explicit_test = False

        if(explicit_test):

            # This generates a subfolder
            execution_identifier = int(time.time())

            rqc = RandomizedQuantumCircuit(4,4)
            rqc.setVerboseOn()
            rqc.constructCircuit()

            circ = rqc.getConstructedRandomCircuit()
            circ_descriptor = rqc.getConstRandCirRepresentation()

            rc = RandomCircuit(circ, 0)
            converter = CircuitVectorConverter()
            result_vector = converter.convert(rc, 'COMP')

            print("rc: ", result_vector)

            computer = VectorMetricsComputer()

            iv = InputVector(result_vector)
            return_value_afmet = computer.compute(iv, 'AFMET')
            print("AFMET, result: ", return_value_afmet)

            return_value_afamet = computer.compute(iv, 'AFAMET')
            print("AFAMET, result: ", return_value_afamet)

            return_value_qmmet = computer.compute(iv, 'QMMET')
            print("QMMET, result: ", return_value_qmmet)

            path_ficd = "stored_results__local/01_circuit_descriptors/test/tests.txt"
            ficd = FileIOforCircDescriptor(path_ficd)
            ficd.insert_data(execution_identifier, circ_descriptor)

            path_fidkv_rv= "stored_results__local/03_result_vectors/test/rv_tests.txt"
            fidkv_rv = FileIOforIdDataKVPairs(path_fidkv_rv)
            fidkv_rv.insert_data(execution_identifier, result_vector)

            path_fidkv_afmet= "stored_results__local/04_metrics/test/afmet_tests.txt"
            fidkv_afmet = FileIOforIdDataKVPairs(path_fidkv_afmet)
            fidkv_afmet.insert_data(execution_identifier, return_value_afmet)

            path_fidkv_afamet= "stored_results__local/04_metrics/test/afamet_tests.txt"
            fidkv_afamet = FileIOforIdDataKVPairs(path_fidkv_afamet)
            fidkv_afamet.insert_data(execution_identifier, return_value_afamet)

            path_fidkv_qmmet= "stored_results__local/04_metrics/test/qmmet_tests.txt"
            fidkv_qmmet = FileIOforIdDataKVPairs(path_fidkv_qmmet)
            fidkv_qmmet.insert_data(execution_identifier, return_value_qmmet)


            path_figures = "stored_results__local/05_figures/test/"

            cv = CircuitVisualizer()
            cv.set_path(path_figures)
            cv.circuit_drawer(str(execution_identifier), circ)

        else:

            execution_function(reg_size = 4, exec_group_id = 00000000, depth_start = 4, depth_stop = 5, exec_per_depth = 2, exec_per_depth_start = None, base_path = None)

if __name__ == '__main__':
    if test_mode:
        twEM = TestWrapperEM() 
        twEM.test_function()