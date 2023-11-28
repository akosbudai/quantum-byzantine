
#
#  Module:  randomized_quantum_circuit
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
#           This is the main class of the random circuit generator model. It implements the randomized circuit generation with the predefined gate types.
#           As an input parameter it receives the register_size and the "depth" of the circuit to be generated.
#           This means that the code files all the raster points with one of the allowed gate type.
#

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

import random

test_mode = False

class RandomizedQuantumCircuit():

    #
    #  Class level varibles
    #
    gates = ["empty", "x-gate", "h-gate", "cnot", "t-gate", "s-gate"]
    administered_cnot_reserved_points = ["start"]
    linearized_coordinate_associated_circuit = ["circuit"]

    def __del__(self):
        pass

    def __init__(self, registers, depth):

        self.registers = registers
        self.depth = depth
        self.q = QuantumRegister(registers, 'q0')
        self.c = ClassicalRegister(registers, 'c0')
        self.circ = QuantumCircuit(self.q, self.c)
        self.verbose = "off"
        self.linearized_coordinate_associated_circuit.insert(1, "registers: {}, depth: {}, ".format(self.registers, self.depth))

    def setVerboseOn(self):
        self.verbose = "on"

    def setVerboseOff(self):
        self.verbose = "off"


    def constructCircuit(self):
        for y in range(self.depth):
            if y > 0:
                if self.verbose == "on":
                    print("draw a bar")
                self.circ.barrier()

            #
            #  This is required to maintain the list of the already reserved places for cnot
            #
            self.administered_cnot_reserved_points.clear()
            for x in range(self.registers):
                self.administered_cnot_reserved_points.append("empty")

            for x in range(self.registers):
                gate = random.randrange(0, len(self.gates))
                if self.verbose == "on":
                    print("Gate {}".format(gate))
                self.gate_assoc (x, gate, self.registers)
        
        self.linearized_coordinate_associated_circuit.append("end-of-descriptor")
    
    def gate_assoc (self, pos, gate, q_register):

        if gate == 0:
            if (self.administered_cnot_reserved_points[pos] == "empty"):
                if self.verbose == "on":
                    print("Nothing to add, this is a wire")
                self.linearized_coordinate_associated_circuit.append("wire")
            else:
                if self.verbose == "on":
                    print("The point is already reserved by other gates. Skip.")

        elif gate == 1:
            if (self.administered_cnot_reserved_points[pos] == "empty"):
                if self.verbose == "on":
                    print("Add a {gate} gate".format(gate = self.gates[1]))
                self.circ.x(self.q[pos])
                self.linearized_coordinate_associated_circuit.append(self.gates[1])
            else:
                if self.verbose == "on":
                    print("The point is already reserved by other gates. Skip.")

        elif gate == 2:
            if (self.administered_cnot_reserved_points[pos] == "empty"):
                if self.verbose == "on":
                    print("Add a {gate} gate".format(gate = self.gates[2]))
                self.circ.h(self.q[pos])
                self.linearized_coordinate_associated_circuit.append(self.gates[2])
            else:
                if self.verbose == "on":
                    print("The point is already reserved by other gates. Skip.")

        elif gate == 3:
            if (self.administered_cnot_reserved_points[pos] == "empty"):
                if self.verbose == "on":
                    print("Add a {gate} gate".format(gate = self.gates[3]))
                self.cnot_handler (pos, gate, q_register)
            else:
                if self.verbose == "on":
                    print("The point is already reserved by other gates. Skip.")
        
        elif gate == 4:
            if (self.administered_cnot_reserved_points[pos] == "empty"):
                if self.verbose == "on":
                    print("Add a {gate} gate".format(gate = self.gates[4]))
                self.circ.t(self.q[pos])
                self.linearized_coordinate_associated_circuit.append(self.gates[4])
            else:
                if self.verbose == "on":
                    print("The point is already reserved by other gates. Skip.")
        
        elif gate == 5:
            if (self.administered_cnot_reserved_points[pos] == "empty"):
                if self.verbose == "on":
                    print("Add a {gate} gate".format(gate = self.gates[5]))
                self.circ.s(self.q[pos])
                self.linearized_coordinate_associated_circuit.append(self.gates[5])
            else:
                if self.verbose == "on":
                    print("The point is already reserved by other gates. Skip.")

        else:
            if self.verbose == "on":
                print("No gate has been selected")


    def cnot_handler (self, pos, gate, q_register):
        cnot_pair_available = 0

        #
        #  Check if is there any possibility to find pair.
        #
        if self.verbose == "on":
            print("cnot_handler pos+1: {}".format((pos + 1)))
            print("cnot_handler q_register: {}".format((q_register)))
        for x in range(pos + 1, q_register):
            if self.verbose == "on":
                print("cnot_handler")
            if (self.administered_cnot_reserved_points[x] == "empty"):
                cnot_pair_available = 1
                break

        if cnot_pair_available:       

            #
            #  Keep the loop until it find a pair.
            #
            while (cnot_pair_available):
                cnot_pair = random.randrange((pos + 1), q_register)

                #
                #  Administering the cnot_pair to avoid redraw.
                #
                if self.administered_cnot_reserved_points[cnot_pair] == "empty":
                    self.administered_cnot_reserved_points[cnot_pair] = "reserved"
                    if self.verbose == "on":
                        print("Selected pair is: {}".format(cnot_pair))
                    control_direction = random.randrange(0, 2)
                    if control_direction == 0:
                        if self.verbose == "on":
                            print("A controls B")
                        self.circ.cx(pos, cnot_pair)
                        self.linearized_coordinate_associated_circuit.append("A, B: {}, {}".format(str(pos), str(cnot_pair)))
                    else:
                        if self.verbose == "on":
                            print("B controls A")
                        self.circ.cx(cnot_pair, pos)
                        self.linearized_coordinate_associated_circuit.append("B, A: {}, {}".format(str(cnot_pair), str(pos)))
                    break

        #
        #  Originally we should bring the cnot to the next column, however, according to this implementation we simply select another gate from the left {wire, x-gate, h-gate}
        #
        else:
            if self.verbose == "on":
                print("No free pair to control")
            gate = random.randrange(0, 3) #FIXME -> because it takes into account only for cnot
            self.gate_assoc (pos, gate, q_register)
    
    def getConstructedRandomCircuit(self):
        return self.circ

    def getConstRandCirRepresentation(self):
        return self.linearized_coordinate_associated_circuit
    
    def clearConstRandCirRepresentation(self):
        self.linearized_coordinate_associated_circuit.clear()

#
#  Local test asset
#  A wrapper class is applied for module related test functions to avoid name collisions.
#
class TestWrapperRQC:
    def __init__(self):
        pass

    def test_function():

        rqc = RandomizedQuantumCircuit(4,5)
        rqc.setVerboseOn()
        rqc.constructCircuit()

if __name__ == '__main__':
    if test_mode:
        twRQC = TestWrapperRQC() 
        twRQC.test_function()