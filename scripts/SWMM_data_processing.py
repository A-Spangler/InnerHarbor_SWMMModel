# By: Ava Spangler
# Date: 6/26/2025
# Description: this code executes a run of SWMM using pyswmm, then processes and stores the results in a dataframe
#              this code can be run with one or several scenarios

# IMPORTS --------------------------------------------------------------------------------------------------------------
import os
import pandas as pd
import swmmio
import pyswmm
import datetime as dt
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import scenarios
from scripts.config import scenarios
from scripts.utils import clean_rpt_encoding


# DEFINITIONS ----------------------------------------------------------------------------------------------------------
# Initialize dictionaries for storing data from each scenario, for each node, for each property
# function to run pyswmm and save outputs as dict
cfs_to_cms = (12**3)*(2.54**3)*(1/100**3)
ft_to_m = 12*2.54*(1/100)
inchperhour_to_cmpersec  = (2.54)*(1/3600)

def list_street_nodes(model): #separate out above ground storage nodes from below ground junctions
    nodes_df = model.nodes.dataframe
    nodes_df = nodes_df.reset_index()
    node_names = nodes_df['Name'].tolist()
    street_node_names = [k for k in node_names if '-S' in k]
    return street_node_names

def pyswmm_nodes(inp_path, node_ids):
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
                output[node_id]['flow'].append(node.total_inflow*cfs_to_cms) #cubmic meters per sec

        # construct df
        node_data = {'timestamp': time_stamps} #dictionary of timestamps
        for node_id in node_ids:
            node_data[f'{node_id}_depth'] = output[node_id]['depth']
            node_data[f'{node_id}_flow'] = output[node_id]['flow']

        df_node_data = pd.DataFrame(node_data).copy()
        return df_node_data

    # define node neighborhood tuple
node_neighborhood_df = pd.read_excel(
        '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05'
        ' - Research/01 - BSEC Project/SWMM models copy/Node_Neighborhoods.xlsx')
node_neighborhood = dict(zip(node_neighborhood_df['street_node_id'],zip(node_neighborhood_df['neighborhood'], node_neighborhood_df['historic_stream'])))
print(node_neighborhood)

def pyswmm_subcatchments(inp_path):
    runoff_data = {}
    infilt_data = {}
    time_stamps = []

    with Simulation(inp_path) as sim:
        sim.step_advance(300)  # 5 min steps

        subcatchments = Subcatchments(sim)
        subcatch_ids = [sc.subcatchmentid for sc in subcatchments]

        for sc_id in subcatch_ids:
            runoff_data[sc_id] = []
            infilt_data[sc_id] = []

        for _ in sim:
            time_stamps.append(sim.current_time)
            for sc in subcatchments:
                sc_id = sc.subcatchmentid
                runoff = sc.runoff * cfs_to_cms
                infilt = sc.infiltration_loss * inchperhour_to_cmpersec
                runoff_data[sc_id].append(runoff)
                infilt_data[sc_id].append(infilt)
                # Debug print
                print(f"{sim.current_time} | {sc_id}: runoff={runoff:.6f}, infilt={infilt:.6f}")

        # Final statistics must be inside the `with` block
        stats_dict = {
            'subcatchment': [],
            'area': [],
            'total_runoff': [],
            'total_infiltration': [],
            'precipitation': []
        }

        for sc in subcatchments:
            stat = sc.statistics
            stats_dict['subcatchment'].append(sc.subcatchmentid)
            stats_dict['area'].append(stat['Area'])
            stats_dict['total_runoff'].append(stat['Runoff'])
            stats_dict['total_infiltration'].append(stat['Infiltration'])
            stats_dict['precipitation'].append(stat['Precipitation'])

    df_runoff = pd.DataFrame(runoff_data)
    df_runoff.insert(0, 'timestamp', time_stamps)

    df_infilt = pd.DataFrame(infilt_data)
    df_infilt.insert(0, 'timestamp', time_stamps)

    df_stats = pd.DataFrame(stats_dict)

    return df_runoff, df_infilt, df_stats



# EXECUTION ------------------------------------------------------------------------------------------------------------
# only rerun this code when SWMM_dataprocessing.py is run
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
    node_ids.remove('J509-S')  # exclude unwanted node

    # run node simulations pyswmm_nodes
    scenario_node_results = {}
    for scenario_name, inp_path in scenarios.items():
        print(f"Running nodes for scenario: {scenario_name}")
        #scenario_node_results[scenario_name] = pyswmm_nodes(inp_path, node_ids)

    #TODO: run subcatchment simulations pyswmm_subcatch
    scenario_subcatch_results = {}
    for scenario_name, inp_path in scenarios.items():
        print(f"Running subcatchments for scenario: {scenario_name}")
        #df_runoff, df_infilt, df_stats = pyswmm_subcatchments(inp_path)
        scenario_subcatch_results[scenario_name] = {
            'runoff': df_runoff,
            'infilt': df_infilt,
            'stats': df_stats
        }

    # Process and combine subcatchment results
    runoff_dfs = []
    infilt_dfs = []
    stats_dfs = []

    for scenario_name, results in scenario_subcatch_results.items():
        df_runoff = results['runoff'].copy()
        df_runoff['scenario'] = scenario_name
        runoff_dfs.append(df_runoff)

        df_infilt = results['infilt'].copy()
        df_infilt['scenario'] = scenario_name
        infilt_dfs.append(df_infilt)

        df_stats = results['stats'].copy()
        df_stats['scenario'] = scenario_name
        stats_dfs.append(df_stats)

# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------
    # combine and save nodes as a multiindex df
    processed_nodes_df = pd.concat(scenario_node_results, names=['scenario'])
    processed_nodes_df.index.set_names(['scenario', 'row'], inplace=True)
    processed_nodes_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_2023_simV20_AllNodes.csv')

    # combine and save subcatchs as a multiindex df
    combined_runoff = pd.concat(runoff_dfs, ignore_index=True)
    combined_infilt = pd.concat(infilt_dfs, ignore_index=True)
    combined_stats = pd.concat(stats_dfs, ignore_index=True)

    combined_runoff.set_index(['scenario', 'timestamp'], inplace=True)
    combined_infilt.set_index(['scenario', 'timestamp'], inplace=True)

    combined_runoff.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/subcatchments/6_27_2023_simV20_runoff.csv')
    combined_infilt.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/subcatchments/6_27_2023_simV20_infilt.csv')
    combined_stats.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/subcatchments/6_27_2023_simV20_stats.csv')

