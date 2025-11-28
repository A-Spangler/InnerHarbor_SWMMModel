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
def find_max_depth(processed_df, node_neighborhood, storm_name):
    # find maxes for each node depth across entire runtime, for each scenario
    grouped_df = processed_df.groupby(level=0).max()

    # select depth cols
    depth_cols = [col for col in grouped_df.columns if col.endswith('_depth')]
    max_depth_df = grouped_df[depth_cols]

    # make scenarios into column headers
    max_depth_df = max_depth_df.reset_index()
    max_depth_df = max_depth_df.set_index('scenario').T
    max_depth_df = max_depth_df.reset_index().rename(columns={'index': 'node_name'})
    max_depth_df = max_depth_df.reset_index(drop = True)
    # assign neighborhoods to node name by extracting node name and mapping dict
    max_depth_df['node_id'] = max_depth_df['node_name'].str.extract(r'([^_]+)')[0] # extract all ccharacters before the underscore (drop _depth)
    max_depth_df['neighborhood'] = max_depth_df['node_id'].map(lambda x: node_neighborhood[x][0])
    max_depth_df['historic_stream'] = max_depth_df['node_id'].map(lambda x: node_neighborhood[x][1])
    # TODO: rearrange order? order = ['col1', 'col2',...] df = df[order]

    #determine and print peak change in flood depth
    print("\nPeak Depths by Scenario:")
    for scenario in max_depth_df.columns[1:-3]:  # Skip node-related columns
        max_val = max_depth_df[scenario].max()
        max_node = max_depth_df.loc[max_depth_df[scenario].idxmax(), 'node_name']
        print(f"Scenario: {scenario}, Node: {max_node}, Peak Depth: {max_val:.3f} m")

    # determine and print avg change in flood depth
    print("\nAverage Depths by Scenario:")
    for scenario in max_depth_df.columns[1:-3]:
        avg_val = max_depth_df[scenario].mean()
        print(f"Scenario: {scenario}, Average Depth: {avg_val:.3f} m")

    # define new df showing relative change from base case
    # drop node names and neighborhoods for subtraction, then add back in
    relative_change_in_depth = max_depth_df.iloc[:, 1:5].copy() # TODO: fix hardcoding in the column indicies, changes 2 + number of scenarios processed
    relative_change_in_depth = relative_change_in_depth.sub(max_depth_df['Base'], axis = 0)
    relative_change_in_depth['node_name'] = max_depth_df['node_name']
    relative_change_in_depth['node_id'] = max_depth_df['node_id']
    relative_change_in_depth['neighborhood'] = max_depth_df['neighborhood']
    relative_change_in_depth['historic_stream'] = max_depth_df['historic_stream']

    #determine and print peak change in flood depth
    print("\nPeak Relative Change by Scenario:")
    for scenario in relative_change_in_depth.columns[0:-4]:
        # Find peak increase
        incr = relative_change_in_depth[scenario].min()
        incr_idx = relative_change_in_depth[scenario].idxmin()
        incr_node = relative_change_in_depth.loc[incr_idx, 'node_name']

        # Find base depth at that node for percentage calculation
        base_depth_incr = max_depth_df.loc[incr_idx, 'Base']
        pct_change_incr = (incr / base_depth_incr * 100) if base_depth_incr > 0 else float('inf')

        # Find peak absolute change
        abs_vals = relative_change_in_depth[scenario].abs()
        idx_abs_max = abs_vals.idxmax()
        max_val = relative_change_in_depth.loc[idx_abs_max, scenario]
        max_node = relative_change_in_depth.loc[idx_abs_max, 'node_name']

        # Find base depth for peak absolute change node
        base_depth_abs = max_depth_df.loc[idx_abs_max, 'Base']
        pct_change_abs = (max_val / base_depth_abs * 100) if base_depth_abs > 0 else float('inf')

        print(f"Scenario: {scenario}")
        print(f"  Peak Absolute Change: {max_val:.3f} m at {max_node} (Base: {base_depth_abs:.3f} m, Change: {pct_change_abs:.1f}%)")
        print(f"  Peak Increase: {incr:.3f} m at {incr_node} (Base: {base_depth_incr:.3f} m, Change: {pct_change_incr:.1f}%)")

# this line does nothing and can be calculated from the averages determined for each scenario above ( as %)
#    print("\nAverage Relative Change by Scenario (:")
#    for scenario in relative_change_in_depth.columns[0:-4]:
#        col_data = relative_change_in_depth[scenario].copy()
#        col_data[col_data > 0] = float('nan')
#        avg_neg = col_data.mean()
#        avg_signed_change = relative_change_in_depth[scenario].mean()
#        print(f"Scenario: {scenario}, avg: {avg_signed_change}, Average decrease (remove incr locations): {avg_neg:} m")

    savepath1 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_MaxDepth.csv'
    savepath2 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_RelativeDepth.csv'
    max_depth_df.to_csv(savepath1)
    relative_change_in_depth.to_csv(savepath2)
    return max_depth_df, relative_change_in_depth  # relative means relative to base case

def find_max_flow(processed_df, node_neighborhood_df, storm_name):
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

    savepath1 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_MaxFlow.csv'
    savepath2 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_RelativeFlow.csv'
    max_flow_df.to_csv(savepath1)
    relative_change_in_flow.to_csv(savepath2)
    return max_flow_df, relative_change_in_flow  # relative means relative to base case

def find_max_vol(processed_df, node_neighborhood_df, storm_name):
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

    savepath1 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_MaxVolume.csv'
    savepath2 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_RelativeVolume.csv'
    max_vol_df.to_csv(savepath1)
    relative_change_in_vol.to_csv(savepath2)
    return max_vol_df, relative_change_in_vol  # relative means relative to base case

def find_max_velocty(processed_links_df,link_neighborhood_df, storm_name):
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

    savepath1 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/{storm_name}_V22_AllNodes_MaxVelocity.csv'
    savepath2 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/{storm_name}_V22_AllNodes_RelativeVelocity.csv'
    max_veloc_df.to_csv(savepath1)
    relative_change_in_veloc.to_csv(savepath2)
    return max_veloc_df, relative_change_in_veloc  # relative means relative to base case


def time_above_curb(processed_nodes_df, storm_name):
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
    savepath1 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_DurationOverCurb.csv'
    savepath2 = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/{storm_name}_V22_AllNodes_RelativeDurationOverCurb.csv'
    duration_result.to_csv(savepath1)
    relative_duration.to_csv(savepath2)

    return relative_duration, duration_result


# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #load processed data
    processed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_23_simV22_AllNodes.csv', index_col=[0, 1])
    processed_links_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/6_27_23_simV22_AllLinks.csv', index_col=[0, 1])

    storm_name = '6_27_23'
    #execute find max fxns
    find_max_depth(processed_df, node_neighborhood, storm_name)
    find_max_flow(processed_df, node_neighborhood, storm_name)
    find_max_vol(processed_df, node_neighborhood, storm_name)
    find_max_velocty(processed_links_df, link_neighborhood, storm_name)

    # execute above curb fxn
    time_above_curb(processed_df, storm_name)


