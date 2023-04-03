"""
This code is used to obtain the numerical data figures in the paper.
"""
import numpy as np
import byzantine_code as eqc
import matplotlib.pyplot as plt

#%%
#define a set for the m values
ms = np.arange(20,401,10)

#set the parametervalues
mu = 0.272
l = 0.94

#%%
#Numerical evalution of the formulas for the no faulty configuration
#create a container for the failure probabilities
probs = []

for m in ms:
    probs.append(eqc.fprob_nofaulty(m = m, mu = mu, l = l))
    
np.savetxt(fname = "numdata_faulty0_mu0272_lambda094.txt", X = probs)

fig = plt.figure()
plt.scatter(ms, probs)
plt.show()

#%%
#s faulty configuration
probs = []

for m in ms:
    probs.append(eqc.fprob_sfaulty(m = m, mu = mu, l = l))
    
np.savetxt(fname = "numdata_faulty1_mu0272_lambda094.txt", X = probs)

fig = plt.figure()
plt.scatter(ms, probs)
plt.show()

#%%
#r0 faulty configuration
probs = []

for m in ms:
    probs.append(eqc.fprob_r0faulty(m = m, mu = mu, l = l))
    
np.savetxt(fname = "numdata_faulty2_mu0272_lambda094.txt", X = probs)

fig = plt.figure()
plt.scatter(ms, probs)
plt.show()