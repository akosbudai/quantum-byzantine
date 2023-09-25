"""
This code is used to estimate the number of quantum states to achieve a fixed failur probability threshhold
for a fixed error rate. 
"""
#%%
import numpy as np
import byzantine_code as eqc

#%%
mu = 0.272
l = 0.94

#define error rate
q = 1e-4

#%%
#define the quantum states for which pf is evaluated
ms = np.arange(400, 653, 1)
Pts = np.zeros(len(ms))

#%%
#evaluate pf for each m
for idx,m in enumerate(ms):

    print(m)

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

    #store the results
    Pts[idx] = P_total

    #print the results
    print(m, P_total, P_err)

#%%
#print the results and find the index of the minimum failure probability
print(Pts)
print(ms[np.argmin(Pts)], Pts[np.argmin(Pts)])