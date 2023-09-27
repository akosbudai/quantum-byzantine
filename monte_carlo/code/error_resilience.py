"""
This code is used to estimate the number of quantum states to achieve a fixed failur probability threshhold
for a fixed error rate. 
"""
#%%
import numpy as np
import multiprocessing
import byzantine_code as eqc

#%%
#define error function
def error_func(m):
    #define the parameters of the protocol
    mu = 0.272
    l = 0.94

    #define error rate
    q = 1e-4    

    #calculate the failure probability for all the scenarios
    pfno = eqc.fprob_nofaulty(m = m, mu = mu, l = l)
    pfs = eqc.fprob_sfaulty(m = m, mu = mu, l = l)
    pfr0 = eqc.fprob_r0faulty(m = m, mu = mu, l = l)

    #calculate the maximum of the failure probabilities
    pf = max([pfno, pfs, pfr0])

    #calculate the probability of a leakage event
    P_err = 1-(1-q)**m

    #calculate the total probability of failure
    P_total = (1 - P_err) * pf + P_err

    return P_total

#%%
#define the number of states for which pf is evaluated
ms = np.arange(400, 500, 1)

#%%
pool = multiprocessing.Pool(8)
results = pool.map(error_func, ms)

#%%
#find the optimal number of states
ind = np.argmin(results)
print(ms[ind], results[ind])
