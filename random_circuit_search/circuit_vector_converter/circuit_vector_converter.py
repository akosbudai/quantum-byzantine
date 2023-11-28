#
#  Module:  circuit_vector_converter
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
#           This module is responsible of the computation of the different metrics related to result vectors.
#           As an input it receives a result vector of a quantum circuit and computes the given fidelity.
#           All the already implemented fidelities are scalar value, however this is not a requirement.
#           You are free to implement any fidelity or non fidelity metrics.
#

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

test_mode = False

class RandomCircuit:
    def __init__(self, circ_instance, shots):
        self.circ_instance = circ_instance
        self.shots = shots

    #   Interface implementation to be compatible with CircuitVectorConverter -> convertable.convert()
    def convert(self, converter):
        converter.start_circuit(self.circ_instance)
        converter.add_property('shots', self.shots)



class CircuitVectorConverter:                       #   Conforms to ObjectSerializer
    def convert(self, convertable, c_method):
        converter = factory.get_converter(c_method) #   Generate a specific type of object from the types of ComputationConverter, SimulationConverter, ExecutionConverter. The selection based on the "c_method".
        convertable.convert(converter)              #   The convertable is a RandomCircuit object, which implements the convert(converter) method. The selected converter is fed with the actual circuit.
        return converter.convert_to_vector()        #   The selected converter already contains the RandomCircuit to be converted, that is the conversion takes place. The result is a ResultVector.



class ComputationConverter:
    def __init__(self):
        self._current_circ = None
    
    def start_circuit(self, circ_instance):
        self._current_circ = {
            'circ_instance': circ_instance
        }
    
    def add_property(self, name, value):
        self._current_circ[name] = value
    
    def convert_to_vector(self):

        #   Select the StatevectorSimulator from the Aer provider
        simulator = Aer.get_backend('statevector_simulator')
    
        #   Execute and get counts
        result = execute(self._current_circ['circ_instance'], simulator).result()
        result_vector = result.get_statevector(self._current_circ['circ_instance'])
        
        return result_vector


class SimulationConverter:
    def __init__(self):
        self._current_circ = None
    
    def start_circuit(self, circ_instance):
        self._current_circ = {
            'circ_instance': circ_instance
        }
    
    def add_property(self, name, value):
        self._current_circ[name] = value
    
    def convert_to_vector(self):
        simulator = Aer.get_backend('qasm_simulator')
    
        #   Execute the circuit on the simulator with given times.
        job_sim = execute(self._current_circ['circ_instance'], backend = simulator, shots = self._current_circ['shots'])
    
        result_vector = job_sim.result().get_counts(self._current_circ['circ_instance'])
    
        return result_vector


class ExecutionConverter:
    def __init__(self):
        self._current_circ = None
    
    def start_circuit(self, circ_instance):
        self._current_circ = {
            'circ_instance': circ_instance
        }
    
    def add_property(self, name, value):
        self._current_circ[name] = value
    
    def convert_to_vector(self):

        return result_vector


class ConverterFactory:
    def __init__(self):
        self._converters = {}

    def register_converter(self, c_method, converter):
        self._converters[c_method] = converter

    def get_converter(self, c_method):
        converter = self._converters.get(c_method)
        if not converter:
            return ValueError(c_method)
        return converter()

factory = ConverterFactory()
factory.register_converter('COMP', ComputationConverter)
factory.register_converter('SIMU', SimulationConverter)
factory.register_converter('EXEC', ExecutionConverter)


#
#  Local test asset
#  A wrapper class is applied for module related test functions to avoid name collisions.
#
class TestWrapperCVC:
    def __init__(self):
        pass

    def test_function():

        #   Test instances
        q = QuantumRegister(2)
        c = ClassicalRegister(2)
        circ = QuantumCircuit(q, c)

        circ.x(0)
        circ.h(1)
        circ.barrier()
        circ.cx(0, 1)
        circ.barrier()
        circ.h(0)
        circ.x(1)

        rc = RandomCircuit(circ, 1024)
        converter = CircuitVectorConverter()
        converter.convert(rc, 'COMP')

if __name__ == '__main__':
    if test_mode:
        twCVC = TestWrapperCVC() 
        twCVC.test_function()