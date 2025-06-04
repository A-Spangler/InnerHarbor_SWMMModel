import pyswmm
import pandas as pd
import networkx as nx
import swmmio
from IPython.display import HTML
import matplotlib.pyplot as plt

from pyswmm import Simulation, Nodes, Links, Subcatchments
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/V19_cleaned_report.inp") as sim:
    node_object = Nodes(sim)
    link_object = Links(sim)
    subcatch_object = Subcatchments(sim)

    # get info about nodes
    J253S = node_object["J253-S"]
    print(J253S.invert_elevation)
    print(J253S.is_junction())

    # get info about conduits
    C6 = link_object["C6"]
    print(C6.depth)
    print(C6.is_conduit())

    # SC1 subcatchment instantiation
    SC1 = subcatch_object["S1"]
    print(SC1.area)

   # Step through a simulation
    #for step in sim:
