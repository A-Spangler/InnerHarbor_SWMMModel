# By: Ava Spangler
# Date: 6/26/2025
# Description: this code executes a run of SWMM using pyswmm, then processes and stores the results in a dataframe
#              this code can be run with one or several scenarios

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pandas as pd
import swmmio
import pyswmm
import datetime as dt
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import scenarios
from scripts.config import model_path

# DEFINITIONS ----------------------------------------------------------------------------------------------------------
# Initialize dictionaries for storing data from each scenario, for each node, for each property
# function to run pyswmm and save outputs as dict
cfs_to_cms = (12**3)*(2.3**3)*(1/100**3)
ft_to_m = 12*2.54*(1/100)
model = swmmio.Model(model_path)

def list_street_nodes(model_path):
    nodes_df = model.nodes.dataframe
    nodes_df = nodes_df.reset_index()
    node_names = nodes_df['Name'].tolist()
    street_node_names = [k for k in node_names if '-S' in k]
    return street_node_names

def run_pyswmm(inp_path, node_ids):
    output = {node: {'depth': [], 'flow': []} for node in node_ids}
    time_stamps = []
# run inp_path simulation, instantiate BE nodes
    with Simulation(inp_path) as sim:
        nodes = {node_id: Nodes(sim)[node_id] for node_id in node_ids} #dictionary with nodes
        sim.step_advance(300) #lets python access sim during run (300 sec = 5min inetervals)

        # Launch inp_path simulation
        for step in enumerate(sim):
            time_stamps.append(sim.current_time)
            for node_id, node in nodes.items(): # store node flow and depth data in node dictionary
                output[node_id]['depth'].append(node.depth*ft_to_m)
                output[node_id]['flow'].append(node.total_inflow*cfs_to_cms)

        # construct df
        node_data = {'timestamp': time_stamps} #dictionary of timestamps
        for node_id in node_ids:
            node_data[f'{node_id}_depth'] = output[node_id]['depth']
            node_data[f'{node_id}_flow'] = output[node_id]['flow']

        df_node_data = pd.DataFrame(node_data).copy()
        return df_node_data


# EXECUTION ------------------------------------------------------------------------------------------------------------

# only rerun this code when SWMM_dataprocessing.py is run
if __name__ == "__main__":
    # find street node names
    model = swmmio.Model(model_path)
    node_ids = list_street_nodes(model_path)

    #run each scenario in pyswmm
    scenario_results = {}
    for scenario_name, inp_path in scenarios.items():
        print(f"Running scenario: {scenario_name}")
        scenario_results[scenario_name] = run_pyswmm(inp_path, node_ids)

# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------
    # combine and save as a multiindex df
    processed_df = pd.concat(scenario_results, names=['scenario'])
    processed_df.index.set_names(['scenario', 'row'], inplace=True)

    processed_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_simV19_AllNodes.csv')
