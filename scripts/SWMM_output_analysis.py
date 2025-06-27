# By: Ava Spangler
# Date: 6/26/2025
# Description: This code takes processed SWMM data and analyzes in

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pandas as pd
import swmmio
import pyswmm
import datetime as dt
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import scenarios

# DEFINITIONS ----------------------------------------------------------------------------------------------------------

def find_max(node_ids):
    max_df = combined_df.groupby(level=0).max()
    return max_df


# EXECUTION ------------------------------------------------------------------------------------------------------------
find_max(node_ids)

# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------

