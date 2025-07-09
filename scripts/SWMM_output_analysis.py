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
    max_depth_df['neighborhood'] = max_depth_df['node_id'].map(node_neighborhood) # TODO: rearrange order? order = ['col1', 'col2',...] df = df[order]

    # define new df showing relative change from base case
    # drop node names and neighborhoods for subtraction, then add back in
    relative_change_in_depth = max_depth_df.iloc[:, 1:7].copy() # TODO: fix hardcoding in the column indicies, changes w scenarios
    relative_change_in_depth = relative_change_in_depth.sub(max_depth_df['Base'], axis = 0)
    relative_change_in_depth['node_name'] = max_depth_df['node_name']
    relative_change_in_depth['node_id'] = max_depth_df['node_id']
    relative_change_in_depth['neighborhood'] = max_depth_df['neighborhood']

    max_depth_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_MaxDepth.csv')
    relative_change_in_depth.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_RelativeDepth.csv')
    return max_depth_df, relative_change_in_depth  # relative means relative to base case

def find_max_flow(processed_df, node_neighborhood):
    # find maxes for each node flowrate depth, each scenario
    grouped_df = processed_df.groupby(level=0).max()

    # select depth cols
    flow_cols = [col for col in grouped_df.columns if col.endswith('_flow')]
    max_flow_df = grouped_df[flow_cols]

    # make scenarios be column headers, keep node names
    max_flow_df = max_flow_df.reset_index()
    max_flow_df = max_flow_df.set_index('scenario').T
    max_flow_df = max_flow_df.reset_index().rename(columns={'index': 'node_name'})
    # assign neighborhoods to node name by extracting node name and mapping dict
    max_flow_df['node_id'] = max_flow_df['node_name'].str.extract(r'([^_]+)')[0]
    max_flow_df['neighborhood'] = max_flow_df['node_id'].map(node_neighborhood)

    # define new df showing relative change from base case
    # drop node names for subtraction, then add back in
    relative_change_in_flow = max_flow_df.iloc[:, 1:7].copy() #TODO fix harcoding in the column indicies, changes w scenarios
    relative_change_in_flow = relative_change_in_flow.sub(max_flow_df['Base'], axis = 0)
    relative_change_in_flow['node_name'] = max_flow_df['node_name']
    relative_change_in_flow['node_id'] = max_flow_df['node_id']
    relative_change_in_flow['neighborhood'] = max_flow_df['neighborhood']

    max_flow_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_MaxFlow.csv')
    relative_change_in_flow.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_RelativeFlow.csv')
    return max_flow_df, relative_change_in_flow  # relative means relative to base case

def time_above_curb(processed_df):
    threshold = 0.1524 # m (6 inches)
    node_columns = [col for col in processed_df.columns if col.endswith('_depth')]

    # Create a boolean df where True if above threshold
    above_threshold = processed_df[node_columns] > threshold

    #count number of cols, multiply by timestep set in data_processing.py (300sec = 5min) to get duration
    count_above = above_threshold.groupby(level='scenario').sum()
    total_time_above = count_above * 300 # seconds
    total_time_above = total_time_above / 60 # min
    total_time_above = total_time_above / 60  # hour

    # make scenarios be column headers
    depth_time_df= total_time_above.reset_index()
    depth_time_df = depth_time_df.set_index('scenario').T.reset_index(drop=True)

    #TODO: relative time above curb, neighborhoods

    depth_time_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_TimeDepth.csv')
    return depth_time_df

# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #load processed data
    processed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_simV19_AllNodes.csv', index_col=[0, 1])
    neighborhoods = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - '
                           'Research/01 - BSEC Project/SWMM models copy/Node_Neighborhoods.xlsx') # named based on https://livebaltimore.com/neighborhoods/

    #execute find max
    find_max_depth(processed_df, node_neighborhood)
    find_max_flow(processed_df, node_neighborhood)

    # execute above curb
    #time_above_curb(processed_df)




