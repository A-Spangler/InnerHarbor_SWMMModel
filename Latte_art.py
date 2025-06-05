'''
PySWMM Latte Art Code
Author: Bryant McDonnell
Version: 1
Date: Nov 17, 2022
'''
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyswmm import Simulation, Nodes, Links, Output
from swmm.toolkit.shared_enum import SubcatchAttribute, NodeAttribute, LinkAttribute

## edited to plot node depth through time. Something is wrong because depth should never be negative
## but i can't figure it out yet

with Simulation(r'Example1.inp') as sim:
    Node21 = Nodes(sim)["21"]
    Link15 = Links(sim)['15']

    # Initialize Lists for storing data
    time_stamps = []
    node_head = []
    link_flow = []

    sim.step_advance(300)
    # Launch a simulation!
    for ind, step in enumerate(sim):
        time_stamps.append(sim.current_time)
        node_head.append(Node21.head)
        link_flow.append(Link15.flow)

with Output('Example1.out') as out:
    node_head_outfile = out.node_series('21', NodeAttribute.HYDRAULIC_HEAD)
    invert_depth_outfile = out.node_series('21', NodeAttribute.INVERT_DEPTH)
    link_flow_outfile = out.link_series('15', LinkAttribute.FLOW_RATE)

# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure
fig = plt.figure(figsize=(8,4), dpi=200) #Inches Width, Height
fig.suptitle("Node 21 Head and Link 15 Flow from simulation and output")
axis_1 = fig.add_subplot(2,1,1)
# Plot from the output file
x = node_head_outfile.keys()
y = [node_head_outfile[key] - invert_depth_outfile[key] for key in node_head_outfile.keys()]
axis_1.plot(x, y, ':b', label="Output File")
axis_1.set_ylabel("Head (ft)")
#axis_1.get_xticklabels().set_visible(False) # turns off the labels
axis_1.grid("xy")
axis_1.legend()
# Second Axis
axis_2 = fig.add_subplot(2,1,2, sharex=axis_1)
axis_2.plot(time_stamps, link_flow, ls='-', color = 'g')
x = link_flow_outfile.keys()
y = [link_flow_outfile[key] for key in link_flow_outfile.keys()]
axis_2.plot(x, y, ':b', label="Output File")
axis_2.set_ylabel("Flow (CFS)")
axis_2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %Hh'))
axis_2.grid("xy")

fig.autofmt_xdate()
plt.tight_layout()
plt.savefig("TEST.PNG")
plt.show()
