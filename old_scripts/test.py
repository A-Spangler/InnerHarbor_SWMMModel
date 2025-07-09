# IMPORTS --------------------------------------------------------------------------------------------------------------
import pandas as pd
import swmmio
import pyswmm
import datetime as dt
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import scenarios
from scripts.config import model_path

def nodes(model_path):
    nodes_df = model.nodes.dataframe
    print(nodes_df)
    return nodes_df

    model = swmmio.Model(model_path)
    node_ids = nodes(model_path)
    print(node_ids)