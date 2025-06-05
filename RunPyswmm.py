import pyswmm
import pandas as pd
import networkx as nx
import swmmio
from IPython.display import HTML
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
from swmm.toolkit.shared_enum import SubcatchAttribute, NodeAttribute, LinkAttribute

# this runs the simulation I think
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/V19_cleaned_report.inp") as sim:
    node_object = Nodes(sim)
    link_object = Links(sim)
    subcatch_object = Subcatchments(sim)
    rain_garden = LidControls(sim)["RainGarden"]

    # node instantiation
    J253S = node_object["J253-S"]

    # Conduit instantiation
    C6 = link_object["C6"]

    # subcatchment instantiation
    SC1 = subcatch_object["S1"]

# output lets you access output without rerunning the file
from pyswmm import Output, SubcatchSeries, NodeSeries, LinkSeries, SystemSeries

with Output('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/V19_cleaned_report.out') as out:
    print(len(out.subcatchments))
    print(len(out.nodes))
    print(len(out.links))
    print(out.version)


    sub_ts = SubcatchSeries(out)['S1'].runoff_rate
    node_ts = NodeSeries(out)['J1'].invert_depth
    link_ts = LinkSeries(out)['C2'].flow_rate
    sys_ts = SystemSeries(out).rainfall

    print(sys_ts)


