# By: Ava Spangler
# Date: 8/12/2025
# Description: this code executes a run of SWMM using pyswmm, then processes and stores the results in a dataframe
# this code can be run with one or several scenarios

# IMPORTS --------------------------------------------------------------------------------------------------------------
import os
import pandas as pd
import swmmio
import pyswmm
import datetime as dt
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import scenarios
from scripts.utils import clean_rpt_encoding


# DEFINITIONS ----------------------------------------------------------------------------------------------------------
# Initialize dictionaries for storing data from each scenario, for each node, for each property
# function to run pyswmm and save outputs as dict
cfs_to_cms = (12**3)*(2.54**3)*(1/(100**3))
ft_to_m = 12*2.54*(1/100)
inchperhour_to_cmpersec = (2.54)*(1/3600)

def list_street_nodes(model): #separate out above ground storage nodes from below ground junctions
    nodes_df = model.nodes.dataframe
    nodes_df = nodes_df.reset_index()
    node_names = nodes_df['Name'].tolist()
    street_node_names = [k for k in node_names if '-S' in k]
    return street_node_names

def list_street_links(model): #separate out above ground storage nodes from below ground junctions
    link_df = model.links.dataframe
    link_df = link_df.reset_index()
    link_names = link_df['Name'].tolist()
    street_link_names = [q for q in link_names if '-S' in q]
    return street_link_names

# TODO: restructure so separate Dfs come out for depth and flow, not combined df
def run_pyswmm(inp_path, node_ids, link_ids):
    output_nodes = {node: {'depth': [], 'flow': []} for node in node_ids}
    output_links = {link: {'velocity': []} for link in link_ids}

# run inp_path simulation, instantiate BE nodes
    time_stamps = []
    with Simulation(inp_path) as sim:
        nodes = {node_id: Nodes(sim)[node_id] for node_id in node_ids} #dictionary with nodes
        links = {link_id: Links(sim)[link_id] for link_id in link_ids}
        sim.step_advance(300) #lets python access sim during run (300 sec = 5min inetervals)

        # Launch inp_path simulation
        for step in enumerate(sim):
            time_stamps.append(sim.current_time)
            for node_id, node in nodes.items(): # store node flow and depth data in node dictionary
                output_nodes[node_id]['depth'].append(node.depth*ft_to_m) # ft to m
                output_nodes[node_id]['flow'].append(node.total_inflow*cfs_to_cms) #m**3/s
            for link_id, link in links.items():  # store node flow and depth data in node dictionary
                output_links[link_id]['velocity'].append(link.flow * ft_to_m) #ft/s to meter/s

        # construct df
        node_data = {'timestamp': time_stamps} #dictionary of timestamps
        for node_id in node_ids:
            node_data[f'{node_id}_depth'] = output_nodes[node_id]['depth']
            node_data[f'{node_id}_flow'] = output_nodes[node_id]['flow']
        link_data = {'timestamp': time_stamps}  # dictionary of timestamps
        for link_id in link_ids:
            link_data[f'{link_id}_velocity'] = output_links[link_id]['velocity']

        df_node_data = pd.DataFrame(node_data).copy()
        df_link_data = pd.DataFrame(link_data).copy()
        return df_node_data, df_link_data

    # define node neighborhood tuple
node_neighborhood_df = pd.read_excel(
        '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05'
        ' - Research/01 - BSEC Project/SWMM models copy/Node_Neighborhoods.xlsx')
node_neighborhood = dict(zip(node_neighborhood_df['street_node_id'],zip(node_neighborhood_df['neighborhood'], node_neighborhood_df['historic_stream'])))

    # define node neighborhood tuple
link_neighborhood_df = pd.read_excel(
        '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05'
        ' - Research/01 - BSEC Project/SWMM models copy/Link_Neighborhoods.xlsx')
link_neighborhood = dict(zip(link_neighborhood_df['link_id'],(link_neighborhood_df['neighborhood'])))


# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #clean all rpt files
    for name, inp_path in scenarios.items():
        rpt_path = os.path.splitext(inp_path)[0] + '.rpt'
        if os.path.isfile(rpt_path):
            print(f"Cleaning report file: {rpt_path}")
            clean_rpt_encoding(rpt_path)

    #find street node names
    model_path = scenarios['Base']
    model = swmmio.Model(model_path)
    node_ids = list_street_nodes(model)
    node_ids.remove('J509-S')  # exclude unwanted (patterson park) node

    #find street link names
    model_path = scenarios['Base']
    model = swmmio.Model(model_path)
    link_ids = list_street_links(model)
    link_ids.remove('C509-S')
    link_ids.remove('C6-S')
    link_ids.remove('C797-S')

    # run simulations
    scenario_node_results = {}
    scenario_link_results = {}
    for scenario_name, inp_path in scenarios.items():
        print(f"Running scenario: {scenario_name}")
        df_nodes, df_links = run_pyswmm(inp_path, node_ids, link_ids)
        scenario_node_results[scenario_name] = df_nodes
        scenario_link_results[scenario_name] = df_links

    # SAVE AND EXPORT ------------------------------------------------------------------------------------------------------
    # combine and save nodes as a multiindex df
    processed_nodes_df = pd.concat(scenario_node_results, names=['scenario'])
    processed_nodes_df.index.set_names(['scenario', 'row'], inplace=True)
    processed_nodes_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_2023_simV20_AllNodes.csv')

    # combine and save links as a multiindex df
    processed_links_df = pd.concat(scenario_link_results, names=['scenario'])
    processed_links_df.index.set_names(['scenario', 'row'], inplace=True)
    processed_links_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/6_27_2023_simV20_AllLinks.csv')



# TODO: write a function to process subcatchments