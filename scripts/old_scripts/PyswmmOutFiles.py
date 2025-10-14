import pyswmm
import pandas as pd
import networkx as nx
import swmmio
from IPython.display import HTML
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Output lets you access output without rerunning the file
from pyswmm import Output, NodeSeries

#access .out file
#with Output('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.out') as out:

    # access hydraulic head time series for nodes
    #J338S_head_ts = NodeSeries(out)['J338-S'].hydraulic_head

    # convert to pandas Series
    #J338S_head_series = pd.Series(J338S_head_ts.items())