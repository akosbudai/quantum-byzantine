"""
This code is used to estimate m_min for a fixed set of parameters and failure probability threshhold.
"""
import numpy as np
import byzantine_code as eqc

#%%
mu = 0.272
l = 0.94

fprob_threshhold = 0.05
#%%
ms = np.arange(100,150,1)
for m in ms:
    p = eqc.fprob_nofaulty(m = m, mu = mu, l = l)
    if p < fprob_threshhold:
        print(m, p)
    
#%%
ms = np.arange(200,260,1)
for m in ms:
    p = eqc.fprob_sfaulty(m = m, mu = mu, l = l)
    if p < fprob_threshhold:
        print(m, p)
        
#%%
ms = np.arange(260,290,1)
for m in ms:
    p = eqc.fprob_r0faulty(m = m, mu = mu, l = l)
    if p < fprob_threshhold:
        print(m, p)