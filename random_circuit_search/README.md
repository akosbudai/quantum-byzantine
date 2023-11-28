# Motivation

This is an experimental package to generate quantum circuits in a predefined manner. Intentionally it was created to discover if the quantum mechanical singlet (Aharonov/Cabello) state can be produced from less than 15 c-not gates, which was the best iterative theoretical achievement at that time (early 2020). The achievement of singlet state is essential to implement the Quantum Byzantine Agreement. Byzantine Agreement has importance in the field of distributed computing, including fault tolerance, blockchain etc., to reach consensus among the participants.

The significance of this package is that with the help of this such a quantum circuit could be generated, which had only 5 c-not gates instead of 15. From noise, stability and applicability point of view this result is impressive. Moreover, it shows that there is room for further improvment in the field of theoretical circuit design (VQA).


# Installation and high level usage

To execute this code python3 has to be installed. Additionally IBM qiskit package is also required.

You can install the required IBM qiskit packages with:
```bash
$pip install qiskit,
$pip install qiskit-aer
```
comamnds.

If it's all set, based on your preferences you can choose between the single- or the multiprocessor execution:
```bash
$python3 execution_manager.py
$python3 execution_multiprocessor_scheduler.py
```

The 'execution_manager' is a single thread realization and will start immediately with the pre-defined settings.
'execution_multiprocessor_scheduler' is a multiprocessor implementation. According to the base configuration it runs 6 parallel threads.


# Block level description and usage

To be able to achieve the desired singlet state the circuit search problem were divided into three main parts, so do the program.
In the following you will find the block level description of the program. Parallel the block level configuration possibilites are also introduced.

## Part I. Definitions

### I.a. Quantum mechanical related definitions - define the fidelity metrics and the allowed quantum gate types

The allowed gate types were selected based on their stable implementation. The only required exception is the above mentioned c-not gate, which is very sensitive, still needed.

The allowed gates are available and can be modified in the 'randomized_quantum_circuit.py' module, 'RandomizedQuantumCircuit' class. Currently available gates are: 
- i-gate (wire),
- x-gate,
- h-gate (hadamard),
- t-gate,
- s-gate,
- cnot-gate.

Objective quality metrics  are also had to be defined, based on which it can be decided if a generated circuit is worth the effort for further investigation.
Following fidelity metrics are implemented for threshold value based selection procedure:
- Cabello/Aharonov state fidelity (also referred as AFMET in the code),
- Cabello/Aharonov subspace fidelity (also referred as AFAMET in the code),
- Quantum Mechanical Fidelity (also referred as QMMET in the code).

The quality/fidelity metrics are available and can be modified in the 'rv2metrics.py' module. The different metrics are implemented in different classes (AFMET, AFAMET, QMMET).


### I.b. Execution related definitions - register size, start and stop circuit depth, number of generated circuits on a given depth, parellelism, storage, etc.

Based on the theoretical results an ambitious experimental goal had been set. To this end the depth of the circuit had been limited to a reasonable range (4-12). This is an externally configurable parameter, and available via the 'execution_manager.py' module  'execution_function()' parameter. The number of generated circuits on a given depth is also an externally configurable parameter of the 'execution_function()'.
Other, storage related parameters can only be directly edited in the 'execution_manager.py' module.

The selected circuits, which passed the fidelity check, were stored in different directories, based on the execution time and the purpose of the saving:
- the formal circuit descriptor,
- the result vector,
- fidelity metrics related results,
- visual representation of the circuit.

Empty directories are still created even if none of the generated circuit pass the fidelity check.

To speed up the experiments, execution in multiprocessor environment also had been implemented. This is available via the 'execution_multiprocessor_scheduler.py'. Here you can parallel start several properly configured 'execution_function()'.


## Part II. Further / equivalent transformations to U/U3 gates, optimization process over the free parameters

None of the previously generated circuits could produce the 100 percent from quantum mechanical fidelity point of view. However, there were good candidates among them.
As a further step two of them had been selected, to perform 'equivalent' transformations over them. The goal was to reduce and replace the specific gate types in the model with the more generic U gates. U gates are the real, physical implementations of the allowed gates. However, U gates has free parameters to play with. 
After some manual tweeking the desired circuit could be achieved. It still contained dedicated gates, however, as we'll see later I created such instance methods, which replace the dedicted gates by properly set U3 gates.

Therefore three approaches had been selected for optimization purposes:
- dimension analysis,
- nearest neigbour search,
- gradient search.

During the executions, after the first round the gradient search approach were dropped out due to it's high time complexity in case of 15 free parameters. Finally, the nearest neigbour approach yielded a very good fidelity: over 99 percent could be achieved. Moreover, by further resolution increasing this value can get arbitrary close to 100 percent with only 5 c-not gates.

To be able to execute numerical optimization methods the already stored and transformed circuits had to be reloaded. Therefore the optimization related files are:
- storage_handlers.py
- rv2metrics.py
- circuit_vector_converter.py
- optimizers.py

In the storage_handlers's FileIOforCircDescriptor class the 'read_data_with_circ_id' and the 'read_data_with_degree_mask' methods are implemented, which performs the gate replacements.


## Part III. Executions

Finally, the circuit was tested on the IBM's real quantum computers. For this purpose this module was used:
- existing_circ_handler.py.


GPU based optimization approaches were also implemented, but those are still in really early stage. The baseline for these executions was the tensor product of the different gates, considered as a final system matrix.

If you new to quantum computing you can find a summary about the quantum phenomena [here](https://tech.ronizongor.com/post/quantum-computing-part-01-intro).
The basics of the quantum circuit model is described [here](https://tech.ronizongor.com/post/quantum-computing-part-02-math).


## License

[GPL3](https://choosealicense.com/licenses/gpl-3.0/)



