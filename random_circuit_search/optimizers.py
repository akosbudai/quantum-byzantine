#
#  Module:  optimizers
#  Version: 0.0.1
#
#  Author:  Istvan Finta
#           https://tech.ronizongor.com
#
#  General notes: 
#           - this is an experimental code for experimental purposes. For production use refactoring is required, eg.: this solution re-read the full circuit each and every time to check small differences. This is needless, only the new vector updated modification should be applied to the circuit, which is already in the memory.
#           - altough IBM has it's own RandomCircuit class this code serves as a part of wider generator, selector and optimizer package.
#
#  Description:
#           This module is responsible to implement three types of circuit optimization approaches. These are:
#           - Dimension Analysis,
#           - Nearest Neighbor Search,
#           - Gradient Search.
#
#  Prerequisites:
#           - the circuit to be analysed should be stored according to the format implemented in storage_handlers.py module,
#           - gate transformations has to be implemented. 
#
#  Important:
#           Actual implementation prints the results to the terminal only. For storage purposes redirect the terminal output to a file (or write own file handler).
#

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, IBMQ

from storage_handlers.storage_handlers import *
from circuit_vector_converter.circuit_vector_converter import *
from metrics.rv2metrics import *

import math
from math import pi
from pathlib import Path
from operator import add

test_mode = True

#
#    Based on dimension_component_analyser.py.
#
class OptimizerDimensionAnalysis:

    def __init__(self):

        #
        # Switches.
        #
        self.print_csv = 1
        self.print_verbose = 1
        self.print_counter = 1
        self.print_subconfig = 1
        self.print_subresults = 1
        self.print_subcircuits = 1
        self.print_main_result = 1
        self.print_main_circuits = 1


        self.source_circuit_path = "stored_results__local/01_circuit_descriptors/aharonov/cabello_reduced.txt"
        self.source_circuit = "cabello_u"

        self.angle_resolution = pi/180
        self.resolution_multiplier = 1
        self.max_value = 360/self.resolution_multiplier

        self.ficd = FileIOforCircDescriptor(self.source_circuit_path)
        self.circ_restored = self.ficd.read_data_with_circ_id(self.source_circuit)

        self.initial_vector = self.ficd.get_degree_mask()
        self.number_of_params = len(self.initial_vector)

        self.new_actual_vector = []
        self.alignment_vector = []

        self.degree_mask = False

        self.qmmet_max = 0
        self.actual_qmmet_max = 0
        self.max_vector = []

        self.global_case_counter = 0


    def restore_and_init(self):

        if self.degree_mask:
            if print_verbose:
                print("Initial vector-1: ", self.initial_vector)
                print("Initial degree mask: ", self.degree_mask)

            self.initial_vector = list( map(add, self.initial_vector, self.degree_mask))

            if self.print_verbose:
                print("Initial vector-2: ", self.initial_vector)

            self.circ_restored = self.ficd.read_data_with_degree_mask(self.source_circuit, self.initial_vector)

        if self.print_verbose:
            print(self.circ_restored)

        rc = RandomCircuit(self.circ_restored, 0)
        converter = CircuitVectorConverter()
        result_vector = converter.convert(rc, 'COMP')
        computer = VectorMetricsComputer()
        iv = InputVector(result_vector)
        return_value_qmmet = computer.compute(iv, 'QMMET')

        if self.print_verbose:
            print("return_value_qmmet: ", return_value_qmmet)

        self.actual_qmmet_max = return_value_qmmet
        self.new_actual_vector = self.initial_vector[:]

        for i in range(0, self.number_of_params):
            self.alignment_vector.append(int(0))


    def compute_and_move(self, actual_vector):

        actual_vector = actual_vector
        case_counter = 0
        best_circ = 0

        #
        # Cycle for dimensions.
        #
        for i in range(0, self.number_of_params):
            changing_alignment_vector = self.alignment_vector[:]

            #
            # Cycle to traversal the selected dimension next to the given resolution.
            #
            for j in range(0, int(self.max_value)):
                changing_alignment_vector[i] = changing_alignment_vector[i] + (self.resolution_multiplier * self.angle_resolution)
                degree_mask = list( map(add, changing_alignment_vector, actual_vector))

                if self.print_verbose:
                    print("degree_mask: ", degree_mask)

                circ_restored_1 = self.ficd.read_data_with_degree_mask(self.source_circuit, degree_mask)

                if self.print_subcircuits:
                    print(circ_restored_1)

                rc = RandomCircuit(circ_restored_1, 0)
                converter = CircuitVectorConverter()
                result_vector = converter.convert(rc, 'COMP')
                computer = VectorMetricsComputer()
                iv = InputVector(result_vector)
                return_value_afmet = computer.compute(iv, 'AFMET')
                return_value_afamet = computer.compute(iv, 'AFAMET')
                return_value_qmmet = computer.compute(iv, 'QMMET')

                if self.print_subresults:
                    print("qmmet: ", return_value_qmmet)
                    print("vector: ", degree_mask)


                if self.qmmet_max < return_value_qmmet:
                    self.qmmet_max = return_value_qmmet
                    max_vector = degree_mask[:]

                if self.print_main_result:
                    print("New qmmet max is: ", self.qmmet_max)
                    print("New qmmet vector: ", max_vector)

                if self.print_counter:
                    print("case_counter: ", case_counter)

                if self.print_csv:
                    print("{}; {}; {}".format(case_counter, return_value_qmmet, degree_mask))

                case_counter = case_counter + 1
                self.global_case_counter = self.global_case_counter + 1

                best_circ = circ_restored_1

        return best_circ


    def seek_an_find(self):
        self.restore_and_init()
        self.compute_and_move(self.new_actual_vector)



#
#    Based on optimizer_manager_v06.py.
#
class OptimizerNearestNeighborSearch:

    def __init__(self):

        #
        # Switches.
        #
        self.print_csv = 1
        self.print_verbose = 1
        self.print_counter = 1
        self.print_subconfig = 1
        self.print_subresults = 1
        self.print_subcircuits = 1
        self.print_main_result = 1
        self.print_main_circuits = 1


        self.source_circuit_path = "stored_results__local/01_circuit_descriptors/aharonov/cabello_reduced.txt"
        self.source_circuit = "cabello_u"

        self.angle_resolution = pi/180
        self.resolution_multiplier = 1

        self.ficd = FileIOforCircDescriptor(self.source_circuit_path)
        self.circ_restored = self.ficd.read_data_with_circ_id(self.source_circuit)

        self.initial_vector = self.ficd.get_degree_mask()
        self.number_of_params = len(self.initial_vector)

        self.new_actual_vector = []
        self.alignment_vector = []

        self.degree_mask = False

        self.qmmet_max = 0
        self.actual_qmmet_max = 0
        self.max_vector = []

        self.global_case_counter = 0


    def restore_and_init(self):
    
        if self.degree_mask:
            if self.print_verbose:
                print("Initial vector-1: ", self.initial_vector)
                print("Initial degree mask: ", self.degree_mask)

            self.initial_vector = list( map(add, self.initial_vector, self.degree_mask))

            if self.print_verbose:
                print("Initial vector-2: ", self.initial_vector)

            self.circ_restored = self.ficd.read_data_with_degree_mask(self.source_circuit, self.initial_vector)

        if self.print_verbose:
            print(self.circ_restored)

        rc = RandomCircuit(self.circ_restored, 0)
        converter = CircuitVectorConverter()
        result_vector = converter.convert(rc, 'COMP')
        computer = VectorMetricsComputer()
        iv = InputVector(result_vector)
        return_value_qmmet = computer.compute(iv, 'QMMET')

        if self.print_verbose:
            print("return_value_qmmet: ", return_value_qmmet)

        self.actual_qmmet_max = return_value_qmmet
        self.new_actual_vector = self.initial_vector[:]

        for i in range(0, self.number_of_params):
            self.alignment_vector.append(int(0))


    def compute_and_move(self, actual_vector):
    
        actual_vector = actual_vector[:]

        case_counter = 0
        best_circ = 0

        #
        # Cycle for visiting all neighbor of a given vector.
        #
        for i in range(0, 2*self.number_of_params):
        #for i in range(0, self.number_of_params):

            changing_alignment_vector = self.alignment_vector[:]

            if(i < self.number_of_params):
              changing_alignment_vector[i] = changing_alignment_vector[i] + (self.resolution_multiplier * self.angle_resolution)
            else:
              changing_alignment_vector[(i - self.number_of_params)] = changing_alignment_vector[(i - self.number_of_params)] - (self.resolution_multiplier * self.angle_resolution)
            #changing_alignment_vector[i] = changing_alignment_vector[i] + (self.resolution_multiplier * self.angle_resolution)
            degree_mask = list( map(add, changing_alignment_vector, actual_vector))

            if self.print_verbose:
                print("degree_mask: ", degree_mask)

            circ_restored_1 = self.ficd.read_data_with_degree_mask(self.source_circuit, degree_mask)

            if self.print_subcircuits:
                print(circ_restored_1)

            rc = RandomCircuit(circ_restored_1, 0)
            converter = CircuitVectorConverter()
            result_vector = converter.convert(rc, 'COMP')
            computer = VectorMetricsComputer()
            iv = InputVector(result_vector)
            return_value_afmet = computer.compute(iv, 'AFMET')
            return_value_afamet = computer.compute(iv, 'AFAMET')
            return_value_qmmet = computer.compute(iv, 'QMMET')

            if self.print_subresults:
                print("qmmet: ", return_value_qmmet)
                print("vector: ", degree_mask)


            #
            # Selection: if the current return value is higher then replace the old value and parameters with the new one.
            #
            if self.actual_qmmet_max < return_value_qmmet:
                self.actual_qmmet_max = return_value_qmmet
                max_vector = degree_mask[:]
                self.new_actual_vector = max_vector

                if self.print_main_result:
                    print("New qmmet max is: ", self.actual_qmmet_max)
                    print("New qmmet vector: ", max_vector)

            if self.print_counter:
                print("case_counter: ", case_counter)

            if self.print_csv:
                print("{}; {}; {}".format(case_counter, return_value_qmmet, degree_mask))

            case_counter = case_counter + 1
            self.global_case_counter = self.global_case_counter + 1


    def seek_an_find(self):

        self.restore_and_init()

        if self.print_verbose:
            print("qmmet_max: ", self.qmmet_max)
            print("actual_qmmet_max: ", self.actual_qmmet_max)
            print("global_case_counter: ", self.global_case_counter)

        while self.actual_qmmet_max > self.qmmet_max:
            self.qmmet_max = self.actual_qmmet_max

            if self.print_verbose:
                print("new_actual_vector: ", self.new_actual_vector)

            self.compute_and_move(self.new_actual_vector)
            #brc = self.compute_and_move(self.new_actual_vector)

            if self.print_verbose:
                print("qmmet_max: ", self.qmmet_max)
                print("actual_qmmet_max: ", self.actual_qmmet_max)
                print("global_case_counter: ", self.global_case_counter)



#
#    Based on optimizer_manager_v06.py.
#
class OptimizerGradientSearch:

    def __init__(self):

        #
        # Switches.
        #
        self.print_csv = 1
        self.print_verbose = 0
        self.print_counter = 0
        self.print_subconfig = 0
        self.print_subresults = 0
        self.print_subcircuits = 0
        self.print_main_result = 0
        self.print_main_circuits = 0

        self.source_circuit_path = "stored_results__local/01_circuit_descriptors/aharonov/cabello_reduced.txt"
        self.source_circuit = "cabello_u"

        self.angle_resolution = pi/180
        self.resolution_multiplier = 1

        self.ficd = FileIOforCircDescriptor(self.source_circuit_path)
        self.circ_restored = self.ficd.read_data_with_circ_id(self.source_circuit)

        self.initial_vector = self.ficd.get_degree_mask()
        self.number_of_params = len(self.initial_vector)

        self.new_actual_vector = []
        self.alignment_vector = []

        self.qmmet_max = 0
        self.actual_qmmet_max = 0
        self.max_vector = []

        self.global_case_counter = 0


    def restore_and_init(self):
    
        if self.degree_mask:
            if self.print_verbose:
                print("Initial vector-1: ", self.initial_vector)
                print("Initial degree mask: ", self.degree_mask)

            self.initial_vector = list( map(add, self.initial_vector, self.degree_mask))

            if self.print_verbose:
                print("Initial vector-2: ", self.initial_vector)

            self.circ_restored = self.ficd.read_data_with_degree_mask(self.source_circuit, self.initial_vector)

        if self.print_verbose:
            print(self.circ_restored)

        rc = RandomCircuit(self.circ_restored, 0)
        converter = CircuitVectorConverter()
        result_vector = converter.convert(rc, 'COMP')
        computer = VectorMetricsComputer()
        iv = InputVector(result_vector)
        return_value_qmmet = computer.compute(iv, 'QMMET')

        if self.print_verbose:
            print("return_value_qmmet: ", return_value_qmmet)

        self.actual_qmmet_max = return_value_qmmet
        self.new_actual_vector = self.initial_vector[:]

        for i in range(0, number_of_params):
            self.alignment_vector.append(int(0))


    def compute_and_move(self, actual_vector):
    
        actual_vector = actual_vector[:]

        case_counter = 0
        best_circ = 0

        for i in range(0, (2**self.number_of_params)):

            
            #
            #    eg.:
            #    number_of_params = 16, i = 15
            #    u = format(15, "0" + str(number_of_params) + "b")
            #
            #    u : 0000000000001111
            #
            u = format(i, "0" + str(self.number_of_params) + "b")
            position_counter = 0
            positions_of_changing_params = []
            alignment_vector = []

            #
            # In this cycle selection of affected values in the vector are determined and collected into a separated array: positions_of_changing_params.
            #
            for d in u:

                alignment_vector.append(((self.resolution_multiplier * self.angle_resolution) * int(d)))

                if int(d) > 0:
                    positions_of_changing_params.append(position_counter)

                position_counter = position_counter + 1

            if self.print_minor_verbose:
                print("actual_vector: ", actual_vector)
                print("alignment_vector-1: ", alignment_vector)
                print("positions_of_changing_params: ", positions_of_changing_params)
            
            #
            # Based on the array each and every combination based selection takes place to alter the current vector, then test against the quantum mechanical fidelity.
            #
            for j in range(0, (2**len(positions_of_changing_params))):

                v = format(j, "0" + str(len(positions_of_changing_params)) + "b")

                if self.print_minor_verbose:
                    print('v: ', v)

                instantaneous_counter = 0
                changing_alignment_vector = alignment_vector[:]

                if self.print_minor_verbose:
                    print("changing_alignment_vector-1: ", changing_alignment_vector)

                for k in v:

                    #
                    # Since this implementation heavily based on my memories here more investigation should be performed:
                    # Maybe this code examining changing values only one direction (-), instead of two (+,-).
                    # Therefore, this 'j' cycle should be executed twice and in the second round with opposite sign compared to the first round.
                    #
                    if int(k) > 0:
                        changing_alignment_vector[positions_of_changing_params[instantaneous_counter]] = (-1)*alignment_vector[positions_of_changing_params[instantaneous_counter]]

                    instantaneous_counter = instantaneous_counter + 1

                if self.print_minor_verbose:
                    print("changing_alignment_vector-2: ", changing_alignment_vector)

                degree_mask = list( map(add, changing_alignment_vector, actual_vector))

                if self.print_minor_verbose:
                    print("degree_mask: ", degree_mask)

                circ_restored_1 = self.ficd.read_data_with_degree_mask(self.source_circuit, degree_mask)

                if self.print_subcircuits:
                    print(circ_restored_1)

                rc = RandomCircuit(circ_restored_1, 0)
                converter = CircuitVectorConverter()
                result_vector = converter.convert(rc, 'COMP')
                computer = VectorMetricsComputer()
                iv = InputVector(result_vector)
                return_value_afmet = computer.compute(iv, 'AFMET')
                return_value_afamet = computer.compute(iv, 'AFAMET')
                return_value_qmmet = computer.compute(iv, 'QMMET')
            
                if self.print_subresults:
                    print("AFMET: ", return_value_afmet)
                    print("AFAMET: ", return_value_afamet)
                    print("QMMET: ", return_value_qmmet)
                    print("case_counter: ", case_counter)

                case_counter = case_counter + 1
                self.global_case_counter = self.global_case_counter + 1

                if self.print_csv_detailed:
                    if self.actual_qmmet_max > self.qmmet_max:
                        print("{}; {}; {}; {}".format(self.global_case_counter, self.actual_qmmet_max, return_value_qmmet, degree_mask))
                    else:
                        print("{}; {}; {}; {}".format(self.global_case_counter, self.qmmet_max, return_value_qmmet, degree_mask))

                if return_value_qmmet > self.actual_qmmet_max:
                    self.new_actual_vector = degree_mask[:]
                    self.actual_qmmet_max = return_value_qmmet

                    best_circ = circ_restored_1
      
        return best_circ


    def seek_an_find(self):

        self.restore_and_init()

        if self.print_verbose:
            print("qmmet_max: ", self.qmmet_max)
            print("actual_qmmet_max: ", self.actual_qmmet_max)
            print("global_case_counter: ", self.global_case_counter)

        while self.actual_qmmet_max > self.qmmet_max:
            self.qmmet_max = self.actual_qmmet_max

            if self.print_verbose:
                print("new_actual_vector: ", self.new_actual_vector)

            #compute_and_move(new_actual_vector)
            brc = self.compute_and_move(self.new_actual_vector)

            if self.print_verbose:
                print("qmmet_max: ", self.qmmet_max)
                print("actual_qmmet_max: ", self.actual_qmmet_max)
                print("global_case_counter: ", self.global_case_counter)

            if self.print_main_circuits:
                print(brc)

#
#  Local test asset
#  A wrapper class is applied for module related test functions to avoid name collisions.
#
class TestWrapperOP:
    def __init__(self):
        pass

    def test_1_function(self):
        oda = OptimizerDimensionAnalysis()
        oda.restore_and_init()
        oda.seek_an_find()
    
    def test_2_function(self):
        onns = OptimizerNearestNeighborSearch()
        onns.restore_and_init()
        onns.seek_an_find()

    def test_3_function(self):
        ogs = OptimizerGradientSearch()
        ogs.restore_and_init()
        ogs.seek_an_find()

if __name__ == '__main__':
    if test_mode:
        twOP = TestWrapperOP() 
        #twOP.test_1_function()
        twOP.test_2_function()
        #twOP.test_3_function()