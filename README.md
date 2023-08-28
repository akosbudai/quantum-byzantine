# byzantion  
A repository for the source code of our paper on a quantum solution to the Byzantine agreement problem.  
  
## ibm_quantum folder   
  
### Run experiments:  
You can run experiments from the circuitb/circuitb_run.ipynb jupyter notebook.
After choosing the desired backend with the command 

```
backend = service.get_backend('ibmq_quito')
```

the experiment can be run using the command

```
all_res = run_circuits(backend)
```

The experiment runs on each layout of the backend that achieves a 9 CNOT circuit.
The variable ```all_res``` is a list of SamplerResult objects.

### Save experiments to file:

Experiments can be saved to file using the jupyter notebook circuitb/circuitb_save.ipynb.
An experiment with qiskit job id ```job_id``` can be saved using the command

```
save_results(job_id, layout_num)
```
  
### Calculate fidelities for experiments:
Quantum fidelities can be calculated using the notebook circuitb/circuitb_evaluate.ipynb.

Fidelities are calculated for the data from a file.
To calculate quantum fidelities, use

```
calculate_QST_quantum_fidelity(filename)
```

This calculates the quantum fidelities for both the raw and mitigated results.

### Data files:  

Data files are created using circuitb/circuitb_save.ipynb and can be found under circuitb/data, named as {backend_name}_{layout_number}.txt. 
The rows are as follows:  
1 - backend name  
2 - layout (list of qubits used)  
3 - experiment end date  
4 - measured distributions (ordered by basis from XXXX to ZZZZ)  
