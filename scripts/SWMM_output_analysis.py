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
    max_depth_df['node_id'] = max_depth_df['node_name'].str.extract(r'([^_]+)')[0]
    max_depth_df['neighborhood'] = max_depth_df['node_id'].map(lambda x: node_neighborhood[x][0])
    max_depth_df['historic_stream'] = max_depth_df['node_id'].map(lambda x: node_neighborhood[x][1])
    # TODO: rearrange order? order = ['col1', 'col2',...] df = df[order]

    # define new df showing relative change from base case
    # drop node names and neighborhoods for subtraction, then add back in
    relative_change_in_depth = max_depth_df.iloc[:, 1:7].copy() # TODO: fix hardcoding in the column indicies, changes w scenarios
    relative_change_in_depth = relative_change_in_depth.sub(max_depth_df['Base'], axis = 0)
    relative_change_in_depth['node_name'] = max_depth_df['node_name']
    relative_change_in_depth['node_id'] = max_depth_df['node_id']
    relative_change_in_depth['neighborhood'] = max_depth_df['neighborhood']
    relative_change_in_depth['historic_stream'] = max_depth_df['historic_stream']

    max_depth_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_2023_V20_AllNodes_MaxDepth.csv')
    relative_change_in_depth.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/nodes/processed/6_27_2023_V20_AllNodes_RelativeDepth.csv')
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
    max_flow_df['node_id'] = max_flow_df['node_name'].str.extract(r'([^_]+)')[0]
    max_flow_df['neighborhood'] = max_flow_df['node_id'].map(node_neighborhood_df)

    # define new df showing relative change from base case
    # drop node names for subtraction, then add back in
    relative_change_in_flow = max_flow_df.iloc[:, 1:7].copy() #TODO fix harcoding in the column indicies for subtraction, changes w scenarios
    relative_change_in_flow = relative_change_in_flow.sub(max_flow_df['Base'], axis = 0)
    relative_change_in_flow['node_name'] = max_flow_df['node_name']
    relative_change_in_flow['node_id'] = max_flow_df['node_id']
    relative_change_in_flow['neighborhood'] = max_flow_df['neighborhood']

    max_flow_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_2023_V20_AllNodes_MaxFlow.csv')
    relative_change_in_flow.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/nodes/processed/6_27_2023_V20_AllNodes_RelativeFlow.csv')
    return max_flow_df, relative_change_in_flow  # relative means relative to base case


def time_above_curb(processed_nodes_df):
    threshold = 0.1524  # m (6 inches)
    timestep_min = 5    # 5 minutes per step, as per SWMM model structure
    col_order = ['node', 'Base', 'BGN', 'BGNx3', 'G', 'I', 'G&I']
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


    duration_result.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_2023_V20_AllNodes_DurationOverCurb.csv')
    relative_duration.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_2023_V20_AllNodes_RelativeDurationOverCurb.csv')

    return relative_duration, duration_result


# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #load processed data
    processed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_2023_simV20_AllNodes.csv', index_col=[0, 1])
    neighborhoods = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - '
                           'Research/01 - BSEC Project/SWMM models copy/Node_Neighborhoods.xlsx') # named based on https://livebaltimore.com/neighborhoods/

    #execute find max
    find_max_depth(processed_df, node_neighborhood)
    find_max_flow(processed_df, node_neighborhood)

    # execute above curb
    time_above_curb(processed_df)




