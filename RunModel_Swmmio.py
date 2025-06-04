import pyswmm
import pandas as pd
import networkx
import swmmio
import matplotlib
import matplotlib.pyplot as plt

# access the model as a Networkx MutliDiGraph
#model_path = '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.inp'

model_path = 'https://raw.githubusercontent.com/USEPA/swmm-nrtestsuite/refs/heads/dev/public/examples/Example1.inp'
model = swmmio.Model(model_path)
G = model.network

link_flows = dict()

# Run simulation PySWMM
with pyswmm.Simulation(model.inp.path) as sim:
    # get link ids
    link_ids = model.inp.conduits.index

    for step in sim:
        # store each link's flow in a dictionary
        link_flows[sim.current_time] = {
            link_id: pyswmm.Links(sim)[link_id].flow
            for link_id in link_ids
        }

pd.DataFrame(link_flows).T.plot(title='Link Flows')
plt.show()