import os
import pandas as pd
import swmmio
import pyswmm
import datetime as dt
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from scripts.config import scenarios, model_path
from scripts.utils import clean_rpt_encoding

# DEFINITONS _______________________________________________________
def pyswmm_subcatchments(inp_path):
    with Simulation(inp_path) as sim:
        sim.step_advance(300)
        subcatchments = Subcatchments(sim)


        # launch inp_path simulation
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
    return df




pyswmm_subcatchments(model_path)