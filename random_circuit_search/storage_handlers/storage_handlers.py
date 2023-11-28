#
#  Module:  storage_handlers
#  Version: 0.0.1
#
#  Author:  Istvan Finta
#           https://tech.ronizongor.com
#
#  General notes: 
#           - this is an experimental code for experimental purposes. For production use refactoring is required,
#           - altough IBM has it's own RandomCircuit class this code serves as a part of wider generator, selector and optimizer package.
#
#  Description:
#           This module is responsible to store and retrive the results to and from files.
#           In case of file operations the id based similarities are not handled implicitly.
#
#  File types: 
#           circuit_id, storage_format, selected_info (circuit representation/description, computed metrics)
#
#  Interface is implemented via the following methods:
#           create_data
#           insert_data
#           read_data
#

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

import numpy

import math
from math import pi

test_mode = False

#
#  Reslover may use the info read from external config file.
#  Not yet implemented.
#
class ResolveNametoStorage:
    def __init__(self):
        pass

#
#  The circuit and the related params should be stored in a divided fashion later.
#  Besides the register size and depth other info also should be stored, like the applied gate-set.
#
class FileIOforCircDescriptor:
    def __init__(self, filename):
        self.filename = filename

    def create_data():
        pass


    def read_data(self, circ_id):
        self.f = open(self.filename, "r")
        self.identifier = circ_id
        self.register = 0
        self.depth = 0
        self.read_config = 0
        self.column_occupied = []
        self.column_pointer = 0

        self.q = None
        self.c = None
        self.circ = None

        self.verbose = 0

        for line in self.f:

            if self.read_config == 1:
                if self.verbose == 1:
                    print("line: {}".format(line))

                if line.find("registers") != -1:
                    a = line.split(",")
                    self.register = int((a[0].split(":"))[1])
                    self.depth = int((a[1].split(":"))[1])

                    if self.verbose == 1:
                        print("registers: {}".format(str(self.register)))
                        print("depth: {}".format(str(self.depth)))

                    self.q = QuantumRegister(self.register)
                    self.c = ClassicalRegister(self.register)
                    self.circ = QuantumCircuit(self.q, self.c)

                    for i in range (0, self.register):
                        self.column_occupied.append("1")

                    if self.verbose == 1:
                        print(self.column_occupied)

                    continue


                if self.register > 0:

                    if line.find("wire") != -1:
                        if self.verbose == 1:
                            print("wire")
                            print(self.column_occupied)

                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("x-gate") != -1:
                        if self.verbose == 1:
                            print("x-gate")
                            print(self.column_occupied)

                        self.circ.x(self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("h-gate") != -1:
                        if self.verbose == 1:
                            print("h-gate")
                            print(self.column_occupied)

                        self.circ.h(self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("A, B") != -1:
                        if self.verbose == 1:
                            print("inside A, B line: {}".format(line))
                            print(self.column_occupied)

                        controlers = (line.split(":")[1]).split(",")

                        if self.verbose == 1:
                            print("controlers[0]: {}".format(str(int(controlers[0]))))
                            print("controlers[1]: {}".format(str(int(controlers[1]))))

                        self.column_occupied[int(controlers[0])] = "0"
                        self.column_occupied[int(controlers[1])] = "0"

                        self.circ.cx(int(controlers[0]), int(controlers[1]))

                        if self.verbose == 1:
                            print("AB-0: {}".format(self.column_occupied[int(controlers[0])]))
                            print("AB-1: {}".format(self.column_occupied[int(controlers[1])]))

                    if line.find("B, A") != -1:
                        if self.verbose == 1:
                            print("inside B, A")
                            print(self.column_occupied)

                        controlers = (line.split(":")[1]).split(",")

                        if self.verbose == 1:
                            print("controlers[0]: {}".format(str(int(controlers[0]))))
                            print("controlers[1]: {}".format(str(int(controlers[1]))))

                        self.column_occupied[int(controlers[0])] = "0"
                        self.column_occupied[int(controlers[1])] = "0"

                        self.circ.cx(int(controlers[0]), int(controlers[1]))

                        if self.verbose == 1:
                            print("BA-0: {}".format(self.column_occupied[int(controlers[0])]))
                            print("BA-1: {}".format(self.column_occupied[int(controlers[1])]))
                    
                    if line.find("t-gate") != -1:
                        if self.verbose == 1:
                            print("inside t-gate")
                            print(self.column_occupied)

                        self.circ.t(self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("s-gate") != -1:
                        if self.verbose == 1:
                            print("inside s-gate")
                            print(self.column_occupied)

                        self.circ.s(self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"
                    
                    if line.find("tdg-gate") != -1:
                        if self.verbose == 1:
                            print("inside tdg-gate")
                            print(self.column_occupied)

                        self.circ.tdg(self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"

                    self.handleNextFreeSlot()

            if line.find(str("execution identifier: {}".format(self.identifier))) != -1:
                self.read_config = 1

            if ((self.read_config == 1) and line.find("end-of-descriptor") != -1) :
                self.read_config = 0
                break

        self.f.close()

        return self.circ

    def read_data_with_circ_id(self, circ_id):
        self.f = open(self.filename, "r")
        self.identifier = circ_id
        self.register = 0
        self.depth = 0
        self.read_config = 0
        self.column_occupied = []
        self.column_pointer = 0

        self.initial_degree_mask = []

        self.q = None
        self.c = None
        self.circ = None

        self.verbose = 0

        for line in self.f:

            if self.read_config == 1:
                if self.verbose == 1:
                    print("line: {}".format(line))
                if line.find("registers") != -1:
                    a = line.split(",")
                    self.register = int((a[0].split(":"))[1])
                    self.depth = int((a[1].split(":"))[1])

                    if self.verbose == 1:
                        print("registers: {}".format(str(self.register)))
                        print("depth: {}".format(str(self.depth)))

                    self.q = QuantumRegister(self.register)
                    self.c = ClassicalRegister(self.register)
                    self.circ = QuantumCircuit(self.q, self.c)

                    for i in range (0, self.register):
                        self.column_occupied.append("1")

                    if self.verbose == 1:
                        print(self.column_occupied)

                    continue


                if self.register > 0:

                    if line.find("wire") != -1:
                        if self.verbose == 1:
                            print("wire")
                            print(self.column_occupied)

                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("x-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of x-gate")
                            print(self.column_occupied)

                        #
                        # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                        #       https://qiskit.org/documentation/release_notes.html#id379
                        #
                        #gate_name = self.circ.u3(pi, pi, 0, self.column_pointer)
                        gate_name = self.circ.u(pi, pi, 0, self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"
                        self.initial_degree_mask.append(pi)
                        self.initial_degree_mask.append(pi)
                        self.initial_degree_mask.append(0)

                    if line.find("h-gate") != -1:
                        if self.verbose == 1:
                            print("h-gate")
                            print(self.column_occupied)

                        self.circ.h(self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("A, B") != -1:
                        if self.verbose == 1:
                            print("inside A, B line: {}".format(line))
                            print(self.column_occupied)

                        controlers = (line.split(":")[1]).split(",")

                        if self.verbose == 1:
                            print("controlers[0]: {}".format(str(int(controlers[0]))))
                            print("controlers[1]: {}".format(str(int(controlers[1]))))

                        self.column_occupied[int(controlers[0])] = "0"
                        self.column_occupied[int(controlers[1])] = "0"

                        self.circ.cx(int(controlers[0]), int(controlers[1]))

                        if self.verbose == 1:
                            print("AB-0: {}".format(self.column_occupied[int(controlers[0])]))
                            print("AB-1: {}".format(self.column_occupied[int(controlers[1])]))

                    if line.find("B, A") != -1:
                        if self.verbose == 1:
                            print("inside B, A")
                            print(self.column_occupied)

                        controlers = (line.split(":")[1]).split(",")

                        if self.verbose == 1:
                            print("controlers[0]: {}".format(str(int(controlers[0]))))
                            print("controlers[1]: {}".format(str(int(controlers[1]))))

                        self.column_occupied[int(controlers[0])] = "0"
                        self.column_occupied[int(controlers[1])] = "0"

                        self.circ.cx(int(controlers[0]), int(controlers[1]))

                        if self.verbose == 1:
                            print("BA-0: {}".format(self.column_occupied[int(controlers[0])]))
                            print("BA-1: {}".format(self.column_occupied[int(controlers[1])]))
                    
                    if line.find("t-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of t-gate")
                            print(self.column_occupied)

                        #
                        # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                        #       https://qiskit.org/documentation/release_notes.html#id379
                        #
                        #gate_name = self.circ.u3(0, 0, pi/4, self.column_pointer)
                        gate_name = self.circ.u(0, 0, pi/4, self.column_pointer)                        
                        self.column_occupied[self.column_pointer] = "0"
                        self.initial_degree_mask.append(0)
                        self.initial_degree_mask.append(0)
                        self.initial_degree_mask.append(pi/4)

                    if line.find("s-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of s-gate")
                            print(self.column_occupied)

                        #
                        # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                        #       https://qiskit.org/documentation/release_notes.html#id379
                        #
                        #gate_name = self.circ.u3(0, 0, pi/2, self.column_pointer)
                        gate_name = self.circ.u(0, 0, pi/2, self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"
                        self.initial_degree_mask.append(0)
                        self.initial_degree_mask.append(0)
                        self.initial_degree_mask.append(pi/2)
                    
                    if line.find("tdg-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of tdg-gate")
                            print(self.column_occupied)

                        #
                        # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                        #       https://qiskit.org/documentation/release_notes.html#id379
                        #
                        #gate_name = self.circ.u3(0, 0, -pi/4, self.column_pointer)
                        gate_name = self.circ.u(0, 0, -pi/4, self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"
                        self.initial_degree_mask.append(0)
                        self.initial_degree_mask.append(0)
                        self.initial_degree_mask.append(-pi/2)

                    self.handleNextFreeSlot()

            if line.find(str("execution identifier: {}".format(self.identifier))) != -1:
                self.read_config = 1

            if ((self.read_config == 1) and line.find("end-of-descriptor") != -1) :
                self.read_config = 0
                break

        self.f.close()

        return self.circ
    

    def get_degree_mask(self):
        return self.initial_degree_mask


    def read_data_with_degree_mask(self, circ_id, degree_mask):
        self.f = open(self.filename, "r")
        self.identifier = circ_id
        self.register = 0
        self.depth = 0
        self.read_config = 0
        self.column_occupied = []
        self.column_pointer = 0

        self.mask_counter = 0

        self.q = None
        self.c = None
        self.circ = None

        self.verbose = 0

        for line in self.f:

            if self.read_config == 1:
                if self.verbose == 1:
                    print("line: {}".format(line))

                if line.find("registers") != -1:
                    a = line.split(",")
                    self.register = int((a[0].split(":"))[1])
                    self.depth = int((a[1].split(":"))[1])

                    if self.verbose == 1:
                        print("registers: {}".format(str(self.register)))
                        print("depth: {}".format(str(self.depth)))

                    self.q = QuantumRegister(self.register)
                    self.c = ClassicalRegister(self.register)
                    self.circ = QuantumCircuit(self.q, self.c)

                    for i in range (0, self.register):
                        self.column_occupied.append("1")

                    if self.verbose == 1:
                        print(self.column_occupied)

                    continue


                if self.register > 0:

                    if line.find("wire") != -1:
                        if self.verbose == 1:
                            print("wire")
                            print(self.column_occupied)

                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("x-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of x-gate")
                            print(self.column_occupied)

                        if (degree_mask[self.mask_counter] or degree_mask[self.mask_counter + 1] or degree_mask[self.mask_counter + 2]):
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                            gate_name = self.circ.u(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                        else:
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(pi, pi, 0, self.column_pointer)
                            gate_name = self.circ.u(pi, pi, 0, self.column_pointer)
                        self.mask_counter = self.mask_counter + 3
                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("h-gate") != -1:
                        if self.verbose == 1:
                            print("h-gate")
                            print(self.column_occupied)

                        self.circ.h(self.column_pointer)
                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("A, B") != -1:
                        if self.verbose == 1:
                            print("inside A, B line: {}".format(line))
                            print(self.column_occupied)

                        controlers = (line.split(":")[1]).split(",")

                        if self.verbose == 1:
                            print("controlers[0]: {}".format(str(int(controlers[0]))))
                            print("controlers[1]: {}".format(str(int(controlers[1]))))

                        self.column_occupied[int(controlers[0])] = "0"
                        self.column_occupied[int(controlers[1])] = "0"

                        self.circ.cx(int(controlers[0]), int(controlers[1]))

                        if self.verbose == 1:
                            print("AB-0: {}".format(self.column_occupied[int(controlers[0])]))
                            print("AB-1: {}".format(self.column_occupied[int(controlers[1])]))

                    if line.find("B, A") != -1:
                        if self.verbose == 1:
                            print("inside B, A")
                            print(self.column_occupied)

                        controlers = (line.split(":")[1]).split(",")

                        if self.verbose == 1:
                            print("controlers[0]: {}".format(str(int(controlers[0]))))
                            print("controlers[1]: {}".format(str(int(controlers[1]))))

                        self.column_occupied[int(controlers[0])] = "0"
                        self.column_occupied[int(controlers[1])] = "0"

                        self.circ.cx(int(controlers[0]), int(controlers[1]))

                        if self.verbose == 1:
                            print("BA-0: {}".format(self.column_occupied[int(controlers[0])]))
                            print("BA-1: {}".format(self.column_occupied[int(controlers[1])]))
                    
                    if line.find("t-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of t-gate")
                            print(self.column_occupied)

                        if (degree_mask[self.mask_counter] or degree_mask[self.mask_counter + 1] or degree_mask[self.mask_counter + 2]):
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                            gate_name = self.circ.u(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                        else:
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(0, 0, pi/4, self.column_pointer)
                            gate_name = self.circ.u(0, 0, pi/4, self.column_pointer)
                        self.mask_counter = self.mask_counter + 3
                        self.column_occupied[self.column_pointer] = "0"

                    if line.find("s-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of s-gate")
                            print(self.column_occupied)
                        
                        if (degree_mask[self.mask_counter] or degree_mask[self.mask_counter + 1] or degree_mask[self.mask_counter + 2]):
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                            gate_name = self.circ.u(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                        else:
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(0, 0, pi/2, self.column_pointer)
                            gate_name = self.circ.u(0, 0, pi/2, self.column_pointer)
                        self.mask_counter = self.mask_counter + 3
                        self.column_occupied[self.column_pointer] = "0"
                    
                    if line.find("tdg-gate") != -1:
                        if self.verbose == 1:
                            print("U3 gate will be applied instead of tdg-gate")
                            print(self.column_occupied)
                        if (degree_mask[self.mask_counter] or degree_mask[self.mask_counter + 1] or degree_mask[self.mask_counter + 2]):
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                            gate_name = self.circ.u(degree_mask[self.mask_counter], degree_mask[self.mask_counter + 1], degree_mask[self.mask_counter + 2], self.column_pointer)
                        else:
                            #
                            # Note: https://stackoverflow.com/questions/76939147/keep-receiving-error-attributeerror-quantumcircuit-object-has-no-attribute
                            #       https://qiskit.org/documentation/release_notes.html#id379
                            #
                            #gate_name = self.circ.u3(0, 0, -pi/4, self.column_pointer)
                            gate_name = self.circ.u(0, 0, -pi/4, self.column_pointer)
                        self.mask_counter = self.mask_counter + 3
                        self.column_occupied[self.column_pointer] = "0"

                    self.handleNextFreeSlot()

            if line.find(str("execution identifier: {}".format(self.identifier))) != -1:
                self.read_config = 1

            if ((self.read_config == 1) and line.find("end-of-descriptor") != -1) :
                self.read_config = 0
                break

        self.f.close()

        return self.circ

    #
    #  Expects a list/circ object
    #
    def insert_data(self, circ_id, circ_descriptor):

        f = open(self.filename, "a")
        f.write(str("execution identifier: {}".format(circ_id)))
        f.write(str("\n"))
        for x in circ_descriptor:
            f.write(str(x))
            f.write(str("\n"))
        
        f.close()


    def handleNextFreeSlot(self):

        while ((self.column_pointer < int(self.register)) and (self.column_occupied[self.column_pointer] == "0")):
            self.column_pointer = self.column_pointer + 1
            if self.verbose == 1:
                print("inside while column_pointer: {}".format(str(self.column_pointer)))

        if self.column_pointer == int(self.register):
            for i in range (0, int(self.register)):
                self.column_occupied[i] = "1"

            self.column_pointer = 0
            self.circ.barrier()

        if self.verbose == 1:
            print("column_pointer: {}".format(str(self.column_pointer)))


#
#  Should work with Result_Vector_Files, F-Metric, F'-Metric, etc., where the delimiter is ' ;;; '
#  Multiple instances will be used: one for RVF, one for F-M, one for F'-M, etc. In case of the file name changes object should be recreated(?)
#
class FileIOforIdDataKVPairs:
    def __init__(self, filename):
        self.filename = filename

    def create_data():
        pass

    def read_data(self, circ_id):
        f = open(self.filename, "r")
        identifier = circ_id
        for line in f:

            #
            #  The following guarantees that ids only from the beginning of the lines are accepted.
            #
            pos = line.find(str(identifier))
            if pos == 0:
                splitted_array = line.split(" ;;; ")
                result_list = (splitted_array[1]).split("; ")

                if len(result_list) > 1:
                    return result_list
                else:
                    return splitted_array[1]


    def insert_data(self, circ_id, assoc_value):
        f = open(self.filename, "a")
        f.write(str(circ_id))
        f.write(' ;;; ')

        #
        #  In case of 'list-like' types an explicit translator should be applied
        #
        if isinstance(assoc_value, list) or isinstance(assoc_value, tuple) or isinstance(assoc_value, set) or isinstance(assoc_value, numpy.ndarray):
            for value in assoc_value:
                f.write(str(value))
                f.write("; ")
        elif isinstance(assoc_value, dict):
            for key in assoc_value:
                f.write(str(key))
                f.write(": ")
                f.write(str(assoc_value[key]))
                f.write("; ")
        else:
            f.write(str(assoc_value))
            f.write("; ")

        f.write('\n')
        f.close()


#
#  Local test asset
#  A wrapper class is applied for module related test functions to avoid name collisions.
#
class TestWrapperSH:
    def __init__(self):
        pass

    def test_1_function():
        ficd = FileIOforCircDescriptor("../../../qiskit_statevector__20200401v01__d13.txt")
        variable = ficd.read_data("158577963908131")
        print("Variable: ", variable)

    def test_2_function():
        test_list = [ 1.76776695e-01+1.76776695e-01j,  1.76776695e-01-1.76776695e-01j, 
                     -8.32667268e-17-2.50000000e-01j, -2.50000000e-01+6.93889390e-17j, 
                     -1.76776695e-01+1.76776695e-01j,  1.76776695e-01+1.76776695e-01j,
                      2.50000000e-01-5.55111512e-17j, -1.11022302e-16-2.50000000e-01j,
                      1.76776695e-01+1.76776695e-01j,  1.76776695e-01-1.76776695e-01j,
                     -5.55111512e-17-2.50000000e-01j, -2.50000000e-01+5.55111512e-17j,
                     -1.76776695e-01+1.76776695e-01j,  1.76776695e-01+1.76776695e-01j,
                      2.50000000e-01-6.93889390e-17j, -6.93889390e-17-2.50000000e-01j]
        path_fidkv_rv= "../stored_results__local/03_result_vectors/rv_tests.txt"
        fidkv_rv = FileIOforIdDataKVPairs(path_fidkv_rv)
        fidkv_rv.insert_data("0000000000", "test_string")
        fidkv_rv.insert_data("0000000001", test_list)

    def test_3_function():
        path_fidkv_rv= "../stored_results__local/03_result_vectors/rv_tests.txt"
        fidkv_rv = FileIOforIdDataKVPairs(path_fidkv_rv)

        print(fidkv_rv.read_data("0000000000"))
        result_list = fidkv_rv.read_data("0000000001")
        print(result_list)
        print(complex(result_list[2]))

    def test_function():
        self.test_1_function()
        self.test_2_function()
        self.test_3_function()


if __name__ == '__main__':
    if test_mode:
        twSH = TestWrapperSH() 
        twSH.test_function()