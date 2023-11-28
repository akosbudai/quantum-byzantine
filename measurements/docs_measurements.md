# IBM Quantum experiments  
  
## Run experiments  
You can run experiments by running the [./ibm_quantum/circuitb/circuitb_run.ipynb](./ibm_quantum/circuitb/circuitb_run.ipynb) jupyter notebook from the IBM Quantum Lab.
After choosing the desired backend ```backend_name``` with the command 

```python
backend = service.get_backend(backend_name)
```

the experiment can be run using the command

```python
all_res = run_circuits(backend)
```

The experiment runs on each layout of the backend that achieves a 9 CNOT circuit.
The variable ```all_res``` is a list of SamplerResult objects.

## Save experiments to file

Experiments can be saved to file using the jupyter notebook [./ibm_quantum/circuitb/circuitb_save.ipynb](./ibm_quantum/circuitb/circuitb_save.ipynb).
An experiment with qiskit job id ```job_id``` can be saved using the command

```python
save_results(job_id, layout_num)
```

The structure of the data files is explained [here](#data-files).
  
## Calculate fidelities for experiments
Quantum fidelities can be calculated using the notebook [./ibm_quantum/circuitb/circuitb_evaluate.ipynb](./ibm_quantum/circuitb/circuitb_evaluate.ipynb).

Fidelities are calculated for the data from a file.
To calculate quantum fidelities, use

```python
calculate_QST_quantum_fidelity(filename)
```

This calculates the quantum fidelities for both the raw and mitigated results.  
Classical fidelities with or without readout error mitigation can also be calculated.

## Data files  

Data files are created using [./ibm_quantum/circuitb/circuitb_save.ipynb](./ibm_quantum/circuitb/circuitb_save.ipynb) and can be found under [./ibm_quantum/circuitb/data](./ibm_quantum/circuitb/data), named as ```{backend_name}_{layout_number}.txt```. 
The rows are as follows:  
1 - backend name  
2 - layout (list of qubits used)  
3 - experiment end date  
4 - measured distributions (ordered by basis from XXXX to ZZZZ)  

# IonQ experiments

The commented jupyter notebook for IonQ experiments can be found under [./ionq/circuitb_ionq.ipynb](./ionq/circuitb_ionq.ipynb).  
The data file can be accessed at [./ionq/counts.txt](./ionq/counts.txt).
