#
#  Module:  circuit_visualizer
#  Version: 0.0.1
#
#  Author:  Istvan Finta
#           https://tech.ronizongor.com
#
#  General note: this is an experimental code for experimental purposes. Refactoring required.
#
#  Description:
#           The goal of this module is to reconstruct a circuit from a (or later various) descriptor(s).
#
#
#   Outdated/obsoleted
#   REQUIRED: - Source File
#             - Execution Identifier
#             - Circuit Opening marker
#             - Circuit Closing marker
#             - Params (depth, qubits)
#
#   For plotting an image about the circuit
#   circ.draw(filename="") 
#   // There are several parameters, which can be found here: https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.draw.html
#


from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.visualization import *

test_mode = False

class CircuitVisualizer:
    def __init__(self):
        pass
    
    def set_path(self, path):
        self.path = path

    def circuit_drawer (self, circuit_id, circ):
        output = self.path + circuit_id + "_fig.png"
        circ.draw(output="mpl", filename=output)

#
#  Local test asset
#  A wrapper class is applied for module related test functions to avoid name collisions.
#
class TestWrapperCV:
    def __init__(self):
        pass

    def test_function():

        #
        #  Test purpose instances
        #
        q = QuantumRegister(2)
        c = ClassicalRegister(2)
        circ = QuantumCircuit(q, c)

        circ.x(0)
        circ.h(1)

        outputFile = "../stored_results__local/05_figures/test"

        cv = CircuitVisualizer()
        cv.set_path(outputFile)
        cv.circuit_drawer("158577963908131", circ)

if __name__ == '__main__':
    if test_mode:
        twCV = TestWrapperCV() 
        twCV.test_function()