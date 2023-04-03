"""
This code is used to generate the data for the 2d grids revealing the m_min values for the 0.05 treshhold failure probability.
"""

import numpy as np
import byzantine_code as eqc

#%%
#first generate the data needed for the upper panel 
ms = np.array([290,300])

mus = np.linspace(0.23,0.30,10)
ls = np.linspace(0.9,0.98,10)

#obtain the mmin points
points = eqc.optimalizator(ms = ms, mus = mus, ls = ls)

#save the data
np.savetxt(fname = "upperpanel_data.txt", X = points)

#%%
#and then generate the data for the lower panel
ms = np.array([i for i in range(270,301)])

mus = np.linspace(0.262,0.282,10)
ls = np.linspace(0.93,0.952,10)

points = eqc.optimalizator(ms = ms, mus = mus, ls = ls)

np.savetxt(fname = "lowerpanel_data.txt", X = points)

#%% 
#lets see a thin slice along the mu axis
ms = np.array([i for i in range(270,301)])

mus = np.linspace(0.27,0.274,50)
ls = np.linspace(0.94,0.945,2)

points = eqc.optimalizator(ms = ms, mus = mus, ls = ls)

np.savetxt(fname = "thinslice_data.txt", X = points)