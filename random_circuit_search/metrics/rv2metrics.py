#
#  Module:  rv2metrics - result vector to metrics computer module
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
import math

test_mode = False

class InputVector:
    def __init__(self, input_vector):
        self.input_vector = input_vector

    #
    #   Interface implementation to be compatible with VectorMetricsComputer -> computable.compute.
    #
    def compute(self, computer):
        computer.start_metric(self.input_vector)



class VectorMetricsComputer:                       # Conform to ObjectSerializer
    def compute(self, computable, c_metrics):
        computer = factory.get_metric(c_metrics)   #   Generate a specific type of object from the types of AharonovFidelityMetrics, AharonovFidelityApMetrics, ArbitraryMetrics. The selection based on the "c_metrics".
        computable.compute(computer)               #   The computable is an InputVector object, which implements the compute(computer) method. The selected computer is fed with the actual vector.
        return computer.compute_metrics()          #   The selected computer already contains the InputVector to be computed, that is the computation takes place. The result is a scalar measurement value.



class AharonovFidelityMetrics:
    #
    #                   0000 0001 0010 0011              0100 0101                  0110                  0111 1000 1001                 1010                   1011 1100                1101 1110 1111
    #
    desired_statevector = [0,   0,   0,   (1/math.sqrt(3)), 0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   (1/(math.sqrt(3))), 0,   0,   0]

    def __init__(self):
        self.statevector = None
    
    def start_metric(self, statevector):
        self.statevector = statevector

    def compute_metrics(self):

        return_value = 0

        j = 0
        for x in self.statevector:
            return_value = return_value + (abs(x) * self.desired_statevector[j])
            j = j+1

        return return_value


class AharonovFidelityApMetrics:

    #
    #                   0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111
    #
    desired_statevector = [0,   0,   0,   1,   0,   1,   1,   0,   0,   1,   1,   0,   1,   0,   0,   0]

    def __init__(self):
        self.statevector = None
    
    def start_metric(self, statevector):
        self.statevector = statevector

    def compute_metrics(self):

        number_of_useful_positions = 6

        return_value = 0
        section_ratio_multiplier = 0
        core_multiplier = 0

        j = 0
        for x in self.statevector:
            product = (abs(x)* abs(x) * self.desired_statevector[j])
            section_ratio_multiplier = section_ratio_multiplier + product
            if product > 0.01:
                core_multiplier = core_multiplier + (1/number_of_useful_positions)
            j = j+1

        return_value = section_ratio_multiplier * core_multiplier

        return return_value


class QMFidelityMetrics:

    #
    #                   0000 0001 0010 0011              0100 0101                  0110                  0111 1000 1001                 1010                   1011 1100                1101 1110 1111
    #
    desired_statevector = [0,   0,   0,   (1/math.sqrt(3)), 0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   (1/(math.sqrt(3))), 0,   0,   0]

    def __init__(self):
        self.statevector = None
    
    def start_metric(self, statevector):
        self.statevector = statevector

    def compute_metrics(self):

        return_value = 0

        j = 0
        for x in self.statevector:
            return_value = return_value + (x.conjugate() * self.desired_statevector[j])
            j = j+1

        return_value = abs(return_value)*abs(return_value)

        return return_value

class QMFidelityRMetrics:

    #
    #                   0000 0001 0010 0011              0100 0101                  0110                  0111 1000 1001                 1010                   1011 1100                1101 1110 1111
    #
    desired_statevector = [0,   0,   0,   (1/math.sqrt(3)), 0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   (1/(math.sqrt(3))), 0,   0,   0]

    def __init__(self):
        self.statevector = None
    
    def start_metric(self, statevector):
        self.statevector = statevector

    def compute_metrics(self):

        return_value = 0

        j = 0
        for x in self.statevector:
            return_value = return_value + (x.conjugate() * self.desired_statevector[j])
            j = j+1

        return return_value

class ArbitraryMetrics:

    def __init__(self):
        self.statevector = None
    
    def start_metric(self, statevector):
        self.statevector = statevector
    
    def compute_metrics(self):
        pass


class MetricsFactory:
    def __init__(self):
        self._computers = {}

    def register_metrics(self, c_metrics, converter):
        self._computers[c_metrics] = converter

    def get_metric(self, c_metrics):
        converter = self._computers.get(c_metrics)
        if not converter:
            return ValueError(c_metrics)
        return converter()

factory = MetricsFactory()
factory.register_metrics('AFMET', AharonovFidelityMetrics)
factory.register_metrics('AFAMET', AharonovFidelityApMetrics)
factory.register_metrics('QMMET', QMFidelityMetrics)


#
#  Local test asset
#  A wrapper class is applied for module related test functions to avoid name collisions.
#
class TestWrapperRVM:
    def __init__(self):
        pass

    def test_function():

        test_vector_1 = [0,   0,   0,   (1/math.sqrt(3)), 0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   0,   (1/(2*math.sqrt(3))), (1/(2*math.sqrt(3))), 0,   (1/(math.sqrt(3))), 0,   0,   0]
        test_vector_2 = [0,   0,   0,   (1/3),   0,   (1/3),   (1/3),   0,   0,   (1/3),   (1/3),   0,   (0.666633332),   0,   0,   0]
        test_vector_3 = [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
        test_vector_4 = [0.5-6.123234e-17j, 0,  0,  0, 0.5+6.123234e-17j,   0,  0,  0, 0.5-6.123234e-17j, 0,  0,  0, 0.5+6.123234e-17j,   0,  0,  0]
        test_vector_5 = [0.07322330470336302-0.07322330470336313j, 2.7755575615628907e-17-1.623039923343337e-18j, 4.4836342863982475e-18-4.4836342863982475e-18j, -0.42677669529663687-0.4267766952966367j, -1.0824450702943669e-17-2.7755575615628907e-17j, -0.17677669529663678+0.17677669529663684j, 0.17677669529663692+0.17677669529663678j, -1.0824450702943661e-17+1.0824450702943665e-17j, 2.1590353721026326e-18-1.7467120361444552e-17j, 1.5265566588595902e-16+0.24999999999999983j, 1.942890293094024e-16+0.24999999999999992j, 9.09773980601393e-33+1.5308084989341894e-17j, 2.220446049250313e-16+0.6035533905932735j, -1.7361307251140927e-18-8.076947141659499e-18j, 3.695698639522925e-17j, 1.1796119636642288e-16+0.1035533905932737j]

        computer = VectorMetricsComputer()

        iv = InputVector(test_vector_1)
        return_value = computer.compute(iv, 'AFMET')
        print("test_vector_1, AFMET, result: ", return_value)

        return_value = computer.compute(iv, 'AFAMET')
        print("test_vector_1, AFAMET, result: ", return_value)

        return_value = computer.compute(iv, 'QMMET')
        print("test_vector_1, QMMET, result: ", return_value)

        iv = None

        iv = InputVector(test_vector_2)
        return_value = computer.compute(iv, 'AFMET')
        print("test_vector_2, AFMET, result: ", return_value)

        return_value = computer.compute(iv, 'AFAMET')
        print("test_vector_2, AFAMET, result: ", return_value)

        return_value = computer.compute(iv, 'QMMET')
        print("test_vector_2, QMMET, result: ", return_value)

        iv = None

        iv = InputVector(test_vector_3)
        return_value = computer.compute(iv, 'AFMET')
        print("test_vector_3, AFMET, result: ", return_value)

        return_value = computer.compute(iv, 'AFAMET')
        print("test_vector_3, AFAMET, result: ", return_value)

        return_value = computer.compute(iv, 'QMMET')
        print("test_vector_3, QMMET, result: ", return_value)

        iv = None

        iv = InputVector(test_vector_4)
        return_value = computer.compute(iv, 'AFMET')
        print("test_vector_4, AFMET, result: ", return_value)

        return_value = computer.compute(iv, 'AFAMET')
        print("test_vector_4, AFAMET, result: ", return_value)

        return_value = computer.compute(iv, 'QMMET')
        print("test_vector_4, QMMET, result: ", return_value)

if __name__ == '__main__':
    if test_mode:
        twRVM = TestWrapperRVM() 
        twRVM.test_function()