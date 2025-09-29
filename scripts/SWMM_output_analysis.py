# By: Ava Spangler
# Date: 6/26/2025
# Description: This code takes in pre-processed SWMM data and analyzes it

# IMPORTS --------------------------------------------------------------------------------------------------------------
import csv
import pandas as pd
import datetime as dt
import swmmio
import pyswmm
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import model_path
from SWMM_data_processing import list_street_nodes
from SWMM_data_processing import node_neighborhood
from SWMM_data_processing import link_neighborhood


# DEFINITIONS ----------------------------------------------------------------------------------------------------------
def find_max_depth(processed_df, node_neighborhood):
    # find maxes for each node depth, each scenario
    grouped_df = processed_df.groupby(level=0).max()

    # select depth cols
    depth_cols = [col for col in grouped_df.columns if col.endswith('_depth')]
    max_depth_df = grouped_df[depth_cols]

    # make scenarios to column headers
    max_depth_df = max_depth_df.reset_index()
    max_depth_df = max_depth_df.set_index('scenario').T
    max_depth_df = max_depth_df.reset_index().rename(columns={'index': 'node_name'})
    max_depth_df = max_depth_df.reset_index(drop = True)
    # assign neighborhoods to node name by extracting node name and mapping dict
    max_depth_df['node_id'] = max_depth_df['node_name'].str.extract(r'([^_]+)')[0] # extract all ccharacters before the underscore (drop _depth)
    max_depth_df['neighborhood'] = max_depth_df['node_id'].map(lambda x: node_neighborhood[x][0])
    max_depth_df['historic_stream'] = max_depth_df['node_id'].map(lambda x: node_neighborhood[x][1])
    # TODO: rearrange order? order = ['col1', 'col2',...] df = df[order]

    # define new df showing relative change from base case
    # drop node names and neighborhoods for subtraction, then add back in
    relative_change_in_depth = max_depth_df.iloc[:, 1:5].copy() # TODO: fix hardcoding in the column indicies, changes 2 + number of scenarios processed
    relative_change_in_depth = relative_change_in_depth.sub(max_depth_df['Base'], axis = 0)
    relative_change_in_depth['node_name'] = max_depth_df['node_name']
    relative_change_in_depth['node_id'] = max_depth_df['node_id']
    relative_change_in_depth['neighborhood'] = max_depth_df['neighborhood']
    relative_change_in_depth['historic_stream'] = max_depth_df['historic_stream']

    max_depth_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_MaxDepth.csv')
    relative_change_in_depth.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_RelativeDepth.csv')
    return max_depth_df, relative_change_in_depth  # relative means relative to base case

def find_max_flow(processed_df, node_neighborhood_df):
    # find maxes for each node flowrate depth, each scenario
    grouped_df = processed_df.groupby(level=0).max()

    # select flow cols
    flow_cols = [col for col in grouped_df.columns if col.endswith('_flow')]
    max_flow_df = grouped_df[flow_cols]

    # make scenarios be column headers, keep node names
    max_flow_df = max_flow_df.reset_index()
    max_flow_df = max_flow_df.set_index('scenario').T
    max_flow_df = max_flow_df.reset_index().rename(columns={'index': 'node_name'})
    # assign neighborhoods to node name by extracting node name and mapping dict
    max_flow_df['node_id'] = max_flow_df['node_name'].str.extract(r'([^_]+)')[0] # extract all characters before the underscore to drop _flow
    max_flow_df['neighborhood'] = max_flow_df['node_id'].map(lambda x: node_neighborhood[x][0])
    max_flow_df['historic_stream'] = max_flow_df['node_id'].map(lambda x: node_neighborhood[x][1])

    # define new df showing relative change from base case
    # drop node names for subtraction, then add back in
    relative_change_in_flow = max_flow_df.iloc[:, 1:5].copy() #TODO fix harcoding in the column indicies for subtraction, changes w scenarios
    relative_change_in_flow = relative_change_in_flow.sub(max_flow_df['Base'], axis = 0)
    relative_change_in_flow['node_name'] = max_flow_df['node_name']
    relative_change_in_flow['node_id'] = max_flow_df['node_id']
    relative_change_in_flow['neighborhood'] = max_flow_df['neighborhood']

    max_flow_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_MaxFlow.csv')
    relative_change_in_flow.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_RelativeFlow.csv')
    return max_flow_df, relative_change_in_flow  # relative means relative to base case

def find_max_vol(processed_df, node_neighborhood_df):
    # find maxes for each node flowrate depth, each scenario
    grouped_df = processed_df.groupby(level=0).max()

    # select flow cols
    vol_cols = [col for col in grouped_df.columns if col.endswith('_volume')]
    max_vol_df = grouped_df[vol_cols]

    # make scenarios be column headers, keep node names
    max_vol_df = max_vol_df.reset_index()
    max_vol_df = max_vol_df.set_index('scenario').T
    max_vol_df = max_vol_df.reset_index().rename(columns={'index': 'node_name'})
    # assign neighborhoods to node name by extracting node name and mapping dict
    max_vol_df['node_id'] = max_vol_df['node_name'].str.extract(r'([^_]+)')[0] # extract all characters before the underscore drop _vol
    max_vol_df['neighborhood'] = max_vol_df['node_id'].map(lambda x: node_neighborhood[x][0])
    max_vol_df['historic_stream'] = max_vol_df['node_id'].map(lambda x: node_neighborhood[x][1])

    # define new df showing relative change from base case
    # drop node names for subtraction, then add back in
    relative_change_in_vol = max_vol_df.iloc[:, 1:5].copy() #TODO fix harcoding in the column indicies for subtraction, changes w scenarios
    relative_change_in_vol = relative_change_in_vol.sub(max_vol_df['Base'], axis = 0)
    relative_change_in_vol['node_name'] = max_vol_df['node_name']
    relative_change_in_vol['node_id'] = max_vol_df['node_id']
    relative_change_in_vol['neighborhood'] = max_vol_df['neighborhood']

    max_vol_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_MaxVolume.csv')
    relative_change_in_vol.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_RelativeVolume.csv')
    return max_vol_df, relative_change_in_vol  # relative means relative to base case

def find_max_velocty(processed_links_df,link_neighborhood_df):
    # find max velocity for each link
    max_veloc_df = processed_links_df.groupby(level=0).max()

    # make scenarios be column headers, keep node names
    max_veloc_df = max_veloc_df.reset_index()
    max_veloc_df = max_veloc_df.set_index('scenario').T
    max_veloc_df = max_veloc_df.reset_index().rename(columns={'index': 'link_name'})
    # assign neighborhoods to node name by extracting node name and mapping dict
    max_veloc_df['link_id'] = max_veloc_df['link_name'].str.extract(r'([^_]+)')[0] # extract all ccharacters before the underscore
    max_veloc_df['neighborhood'] = max_veloc_df['link_id'].map(link_neighborhood_df)

    # define new df showing relative change from base case
    # drop node names for subtraction, then add back in
    relative_change_in_veloc = max_veloc_df.iloc[:, 1:8].copy() #TODO fix harcoding in the column indicies for subtraction, changes w scenarios
    # ensure all are numeric
    relative_change_in_veloc = relative_change_in_veloc.apply(pd.to_numeric, errors='coerce')
    max_veloc_df['Base'] = pd.to_numeric(max_veloc_df['Base'], errors='coerce')
    # subtract base values
    relative_change_in_veloc = relative_change_in_veloc.sub(max_veloc_df['Base'], axis = 0)
    relative_change_in_veloc['link_name'] = max_veloc_df['link_name']
    relative_change_in_veloc['link_id'] = max_veloc_df['link_id']
    relative_change_in_veloc['neighborhood'] = max_veloc_df['neighborhood']

    max_veloc_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/SCS3_V22_AllNodes_MaxVelocity.csv')
    relative_change_in_veloc.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/SCS3_V22_AllNodes_RelativeVelocity.csv')
    return max_veloc_df, relative_change_in_veloc  # relative means relative to base case


def time_above_curb(processed_nodes_df):
    threshold = 0.1524  # m (6 inches)
    timestep_min = 5    # 5 minutes per step, as per SWMM model structure
    col_order = ['node', 'Base', 'V', 'I', 'V+I']
    node_columns = [col for col in processed_nodes_df.columns if col.endswith('_depth')]

    # Boolean DataFrame where True means above threshold, by scenario
    processed_nodes_df = processed_nodes_df.reset_index()
    above_thresh = processed_nodes_df[node_columns] > threshold
    above_thresh['scenario'] = processed_nodes_df['scenario']

    # count above-threshold per node per scenario
    duration_result = above_thresh.groupby('scenario')[node_columns].sum().T

    #convert to DataFrame with columns for node, scneario, and count above threshold
    duration_result.reset_index(inplace=True)
    duration_result = duration_result.melt(id_vars='index', var_name='scenario', value_name='count')
    duration_result.rename(columns={'index': 'node'}, inplace=True)
    duration_result['time_above'] = duration_result['count'] * timestep_min # time in min


    #subtract Base from all scenarios, reorganize cols
    relative_duration = duration_result.pivot(index='node', columns='scenario', values='time_above')
    relative_duration = relative_duration.sub(relative_duration['Base'], axis=0)
    relative_duration = relative_duration.reset_index()
    relative_duration = relative_duration.reindex(columns=col_order)

    #save
    duration_result.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_DurationOverCurb.csv')
    relative_duration.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_V22_AllNodes_RelativeDurationOverCurb.csv')

    return relative_duration, duration_result


# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #load processed data
    processed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/SCS3_simV22_AllNodes.csv', index_col=[0, 1])
    processed_links_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/SCS3_simV22_AllLinks.csv', index_col=[0, 1])

    #execute find max fxns
    find_max_depth(processed_df, node_neighborhood)
    find_max_flow(processed_df, node_neighborhood)
    find_max_vol(processed_df, node_neighborhood)
    find_max_velocty(processed_links_df, link_neighborhood)

    # execute above curb fxn
    time_above_curb(processed_df)




