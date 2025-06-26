# By: Ava Spangler
# Date: 6/26/2025
# Description: this code executes a run of SWMM using pyswmm, then processes and stores the results in a dataframe
#              this code can be run with one or several scenarios

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import swmmio
import pyswmm
import datetime as dt
from IPython.display import HTML
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups


# DEFINITIONS ----------------------------------------------------------------------------------------------------------
# Initialize dictionaries for storing data from each scenario, for each node, for each property
# function to run pyswmm and save outputs as dict
cfs_to_cms = (12**3)*(2.3**3)*(1/100**3)
ft_to_m = 12*2.54*(1/100)

def run_pyswmm(inp_path, node_ids):
    output = {node: {'depth': [], 'flow': []} for node in node_ids}
    time_stamps = []
# run inp_path simulation, instantiate BE nodes
    with Simulation(inp_path) as sim:
        nodes = {node_id: Nodes(sim)[node_id] for node_id in node_ids}
        sim.step_advance(300) #lets python access sim during run (300 sec = 5min inetervals)

        # Launch inp_path simulation
        for step in enumerate(sim):
            time_stamps.append(sim.current_time)
            for node_id, node in nodes.items(): # store node data in dictionary
                output[node_id]['depth'].append(node.depth*ft_to_m)
                output[node_id]['flow'].append(node.total_inflow*cfs_to_cms)

        # construct df
        df_output = pd.DataFrame({'timestamp': time_stamps})
        for node_id in node_ids:
            df_output[f'{node_id}_depth'] = output[node_id]['depth']
            df_output[f'{node_id}_flow'] = output[node_id]['flow']

        return df_output


# EXECUTION ------------------------------------------------------------------------------------------------------------
# Run all scenarios and store results
node_ids = ["J338-S", "J253-S", "J366-S"]

scenarios = {
    'base': r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.inp",
    'BGN' : r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_BGN.inp",
    'BGNx3' : "/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_BGNx3.inp",
    'IC': r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_Inlets.inp",
    'GM': r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_greenmaxxing.inp",
    'GM+IC' : r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_greenmaxxing+inlets.inp"
}

scenario_results = {}
for scenario_name, inp_path in scenarios.items():
    print(f"Running scenario: {scenario_name}")
    scenario_results[scenario_name] = run_pyswmm(inp_path, node_ids)

# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------
# combine all into a single df
processed_df = pd.concat(scenario_results, names=['scenario', 'row'])
processed_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_simV19.csv', index=False)
print(isinstance(processed_df.index, pd.MultiIndex))