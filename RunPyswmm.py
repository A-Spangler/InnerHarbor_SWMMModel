import pyswmm
import pandas as pd
import networkx as nx
import swmmio
from IPython.display import HTML
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups

# Initialize Lists for storing data
time_stamps = []
J338S_depth = []
J253S_depth = []
J366S_depth = []

# run the simulation, instantiate BE nodes
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.inp") as sim:
    J338S = Nodes(sim)['J338-S']
    J253S = Nodes(sim)['J253-S']
    J366S = Nodes(sim)['J366-S']

#lets python access sim during run (i think)
    sim.step_advance(300)

# Launch a simulation
    for ind, step in enumerate(sim):
        time_stamps.append(sim.current_time)
        J338S_depth.append(J338S.depth)
        J253S_depth.append(J253S.depth)
        J366S_depth.append(J366S.depth)

## Plotting ------------------------------------------------------------------------------------------------------------

fig = plt.figure(figsize=(8,4), dpi=200) #Inches Width, Height
fig.suptitle("Broadway East Node Depths")
axis_1 = fig.add_subplot(1,1,1)

#plot from sim
axis_1.plot(time_stamps, J338S_depth, color = 'c', label = 'Chase St. and Rutland St.')
axis_1.plot(time_stamps, J253S_depth, color = 'm', label = 'Eager St. and Rutland St.')
axis_1.plot(time_stamps, J366S_depth, color = 'y', label = 'Barnes Street')

axis_1.set_ylabel("Depth(ft)")
#axis_1.get_xticklabels().set_visible(False) # turns off the labels
axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %Hh'))
axis_1.legend()

fig.autofmt_xdate()
plt.tight_layout()
plt.show()

