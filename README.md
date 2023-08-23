# byzantion
A repository for the source code of our paper on a quantum solution to the Byzantine agreement problem.

## ibm_quantum folder

### Run experiments:
circuitb_run.ipynb
usage:
backend = service.get_backend('ibmq_quito')
all_res = run_circuits(backend)

### Save experiments to file:
circuitb_save.ipynb
usage:
save_results(job_id, layout_num)

### Calculate fidelities for experiments:
circuitb_evaluate.ipynb
usage: 
calculate_QST_quantum_fidelity(filename)
