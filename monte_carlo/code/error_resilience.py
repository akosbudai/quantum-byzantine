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
q = 1e-5
#%%
#define the quantum states for which pf is evaluated
ms = np.arange(500,653, 1)
Pts = np.zeros(len(ms))

#%%
#evaluate pf for each m
for idx,m in enumerate(ms):

    #calculate pf
    pf = eqc.fprob_sfaulty(m = m, mu = mu, l = l)

    #calculate the probability of a leakage event
    P_err = 1-(1-q)**m
    P_err2 = m*q
    #calculate the total probability of failure
    P_total = (1 - P_err) * pf + P_err

    #store the results
    Pts[idx] = P_total

    #print the results
    print(m, P_total, P_err, P_err2)

#%%
#find the index of the minimum
print(ms[np.argmin(Pts)], Pts[np.argmin(Pts)])
# %%
