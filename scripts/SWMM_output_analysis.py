# By: Ava Spangler
# Date: 6/26/2025
# Description: This code takes in pre-processed SWMM data and analyzes it

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pandas as pd
import datetime as dt
import swmmio
import pyswmm
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import scenarios
from scripts.config import model_path
from SWMM_data_processing import list_street_nodes

# DEFINITIONS ----------------------------------------------------------------------------------------------------------
def find_max(processed_df):
    # find maxes for each node flowrate depth, each scenario
    grouped_df = processed_df.groupby(level=0).max()

    # select depth cols
    depth_cols = [col for col in grouped_df.columns if col.endswith('_depth')]
    depth_df = grouped_df[depth_cols]
    depth_long = depth_df.melt()

    # select flow cols
    flow_cols = [col for col in grouped_df.columns if col.endswith('_flow')]
    flow_df = grouped_df[flow_cols]
    flow_long = depth_df.melt()

    # combine and save as a df, NOT multiindex since melted
    max_df = pd.concat([depth_long, flow_long], names=['scenario'])
    max_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_max.csv')
    return max_df

# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #load processed data
    processed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_simV19_AllNodes.csv', index_col=[0, 1])
    rain_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_23_rain_df.csv')

    #execute find max
    find_max(processed_df)



# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------

