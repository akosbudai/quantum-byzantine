"""
This code is used to obtain the data from the Monte-Carlo simulations
"""
import numpy as np
import byzantine_code as eqc
import matplotlib.pyplot as plt

#%%

#set the parameters of the simulation

#possible values of m
ms = np.arange(20,401,10)

#number of trials for each m
N = 10000

#parameters of the protocol
mu = 0.272
l = 0.94

#%%
#no faulty configuration
faulty = 0

#carry out the simulation
data = eqc.total_stats(N = N, ms = ms, faulty = faulty, mu = mu, l = l)

#plot the data
fig = plt.figure()
plt.scatter(ms,data[:])
plt.show()

#save the data
#np.savetxt(fname = "../data/simdata_faulty0_mu0272_lambda094.txt", X = data)

#%%
#faulty configuration
faulty = 1

#carry out the simulation
data = eqc.total_stats(N = N, ms = ms, faulty = faulty, mu = mu, l = l)

#plot the data
fig = plt.figure()
plt.scatter(ms,data[:])
plt.show()

#save the data
#np.savetxt(fname = "../data/simdata_faulty1_mu0272_lambda094.txt", X = data)

#%%
#faulty configuration
faulty = 2

#carry out the simulation
data = eqc.total_stats(N = N, ms = ms, faulty = faulty, mu = mu, l = l)

#plot the data
fig = plt.figure()
plt.scatter(ms,data[:])
plt.show()

#save the data
#np.savetxt(fname = "../data/simdata_faulty2_mu0272_lambda094.txt", X = data)