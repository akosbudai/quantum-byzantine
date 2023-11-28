#
#  Module:  existing_circ_handler
#  Version: 0.0.1
#
#  Author:  Istvan Finta
#           https://tech.ronizongor.com
#
#  General notes: 
#           - this is an experimental package for experimental purposes. For production use refactoring is required,
#           - altough IBM has it's own RandomCircuit class this code serves as a part of wider generator, selector and optimizer package.
#
#  Description:
#           This module is responsible for the remote execution of the quantum circuits on the IBM machines.
#           It can be set to execute in simulator mode, or enque into real machines queue.
#           After predefined shots the result fetched from the remote server and saved into the given path.
#

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, IBMQ

from storage_handlers.storage_handlers import *

import time
import math
from pathlib import Path

IBMQ.save_account('YOUR_HASH_COMES_HERE')
source_circuit_path = ""                        #  Selected path comes here, like: "stored_results__local/01_circuit_descriptors/1589474619000000/d_10.txt"
source_circuit = ""                             #  Selected circuit id comes here, like: "15894746190000001295856"

destination_path = ""                           #  Output file comes here, like: "stored_results__local/03_result_vectors/00_executions/15894746190000001295856.txt"

def restore_and_execute():
    ficd = FileIOforCircDescriptor(source_circuit_path)
    circ_restored = ficd.read_data(source_circuit)
    c = circ_restored.clbits
    q = circ_restored.qubits
    circ_restored.measure(q, c)

    print("Variable: ", circ_restored)

    fikvp = FileIOforIdDataKVPairs(destination_path)

    #
    # Execute the circuit
    #
    for i in range(0,1000):
        job = execute(circ_restored, backend = Aer.get_backend('qasm_simulator'), shots=1024)
        result = job.result()
    
        #
        # Print the result
        #
        result_vector = result.get_counts(circ_restored)
        print(result_vector)
    
        fikvp.insert_data(source_circuit, result_vector)

if __name__ == '__main__':
    restore_and_execute()