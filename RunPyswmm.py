import pyswmm
import pandas as pd
import networkx as nx
import swmmio
from IPython.display import HTML
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups

cfs_to_cms = (12**3)*(2.3**3)*(1/100**3)
ft_to_m = 12*2.54*(1/100)


node_ids = ["J338S", "J253S", "J366S"]
scenarios = {
    'base': r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.inp",
    'BGN' : r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_BGN.inp",
    'BGNx3' : "/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_BGNx3.inp",
    'inlets': r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_Inlets.inp",
    'GM': r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_greenmaxxing.inp",
    'GMI' : r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_greenmaxxing+inlets.inp"
}

## BASE v19 SIM ------------------------------------------------------------------------------------------------------------
# Initialize dictionaries for storing data from each scenario, for each node, for each property
# function to run pyswmm and save outputs as dict
def run_pyswmm(inp_path):
    output = {node: {'depth': [], 'flow': []} for node in node_ids}
    time_stamps = []
# run the BASE simulation, instantiate BE nodes
    with Simulation(inp_path) as sim:
        nodes = {node_id: Nodes(sim)[node_id] for node_id in node_ids}
        sim.step_advance(300) #lets python access sim during run (300 sec = 5min inetervals)

        # Launch BASE simulation
        for step in enumerate(sim):
            time_stamps.append(sim.current_time)
            for node_id, node in nodes.items(): # store node data in dictionary
                output[node]['depth'].append(node.depth*ft_to_m)
                output[node]['flowrate'].append(node.total_inflow*cfs_to_cms)

        # Construct DataFrame
        df = pd.DataFrame({'timestamp': time_stamps})
        for node_id in node_ids:
            df[f'{node_id}_depth'] = output[node_id]['depth']
            df[f'{node_id}_flow'] = output[node_id]['flow']

        return df

    # Run all scenarios and store results
    scenario_results = {}
    for scenario_name, inp_path in scenarios.items():
        print(f"Running scenario: {scenario_name}")
        scenario_results[scenario_name] = run_pyswmm(inp_path, node_ids)

#combined_df = pd.concat(scenarios, names=['scenario', 'row'])
#print(combined_df.head())
'''
## BGN v19 SIM ---------------------------------------------------------------------------------------------------------
# Initialize Lists for storing data
time_stamps_BGN = []
J338S_depth_BGN = []
J253S_depth_BGN = []
J366S_depth_BGN = []
J338S_flwrt_BGN = []
J253S_flwrt_BGN = []
J366S_flwrt_BGN = []

#run the simulation, instantiate BE nodes
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_BGN.inp") as sim:
    J338S_BGN = Nodes(sim)['J338-S']
    J253S_BGN = Nodes(sim)['J253-S']
    J366S_BGN = Nodes(sim)['J366-S']

#lets python access sim during run (i think)
    sim.step_advance(300)

# Launch simulation
    for ind, step in enumerate(sim):
        time_stamps_BGN.append(sim.current_time)
        J338S_depth_BGN.append(J338S_BGN.depth)
        J253S_depth_BGN.append(J253S_BGN.depth)
        J366S_depth_BGN.append(J366S_BGN.depth)
        J338S_flwrt_BGN.append(J338S_BGN.total_inflow * cfs_to_cms)
        J253S_flwrt_BGN.append(J253S_BGN.total_inflow * cfs_to_cms)
        J366S_flwrt_BGN.append(J366S_BGN.total_inflow * cfs_to_cms)

## Inlets v19 SIM ------------------------------------------------------------------------------------------------------
# Initialize Lists for storing data
time_stamps_inlets = []
J338S_depth_inlets = []
J253S_depth_inlets = []
J366S_depth_inlets = []
J338S_flwrt_inlets = []
J253S_flwrt_inlets = []
J366S_flwrt_inlets = []

# run the simulation, instantiate BE nodes
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_Inlets.inp") as sim:
    J338S_inlet = Nodes(sim)['J338-S']
    J253S_inlet = Nodes(sim)['J253-S']
    J366S_inlet = Nodes(sim)['J366-S']

#lets python access sim during run (i think)
    sim.step_advance(300)

# Launch simulation
    for ind, step in enumerate(sim):
        time_stamps_inlets.append(sim.current_time)
        J338S_depth_inlets.append(J338S_inlet.depth)
        J253S_depth_inlets.append(J253S_inlet.depth)
        J366S_depth_inlets.append(J366S_inlet.depth)
        J338S_flwrt_inlets.append(J338S_inlet.total_inflow * cfs_to_cms)
        J253S_flwrt_inlets.append(J253S_inlet.total_inflow * cfs_to_cms)
        J366S_flwrt_inlets.append(J366S_inlet.total_inflow * cfs_to_cms)

## 3BGN v19 SIM ---------------------------------------------------------------------------------------------------------
# Initialize Lists for storing data
time_stamps_3BGN = []
J338S_depth_3BGN = []
J253S_depth_3BGN = []
J366S_depth_3BGN = []
J338S_flwrt_3BGN = []
J253S_flwrt_3BGN = []
J366S_flwrt_3BGN = []

#run the simulation, instantiate BE nodes
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_BGNx3.inp") as sim:
    J338S_3BGN = Nodes(sim)['J338-S']
    J253S_3BGN = Nodes(sim)['J253-S']
    J366S_3BGN = Nodes(sim)['J366-S']

#lets python access sim during run (i think)
    sim.step_advance(300)

# Launch simulation
    for ind, step in enumerate(sim):
        time_stamps_3BGN.append(sim.current_time)
        J338S_depth_3BGN.append(J338S_3BGN.depth)
        J253S_depth_3BGN.append(J253S_3BGN.depth)
        J366S_depth_3BGN.append(J366S_3BGN.depth)
        J338S_flwrt_3BGN.append(J338S_3BGN.total_inflow * cfs_to_cms)
        J253S_flwrt_3BGN.append(J253S_3BGN.total_inflow * cfs_to_cms)
        J366S_flwrt_3BGN.append(J366S_3BGN.total_inflow * cfs_to_cms)

## GreenMaxxing v19 SIM ---------------------------------------------------------------------------------------------------------
# Initialize Lists for storing data
time_stamps_GM = []
J338S_depth_GM = []
J253S_depth_GM = []
J366S_depth_GM = []
J338S_flwrt_GM = []
J253S_flwrt_GM = []
J366S_flwrt_GM = []

#run the simulation, instantiate BE nodes
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_greenmaxxing.inp") as sim:
    J338S_GM = Nodes(sim)['J338-S']
    J253S_GM = Nodes(sim)['J253-S']
    J366S_GM = Nodes(sim)['J366-S']

#lets python access sim during run (i think)
    sim.step_advance(300)

# Launch simulation
    for ind, step in enumerate(sim):
        time_stamps_GM.append(sim.current_time)
        J338S_depth_GM.append(J338S_GM.depth)
        J253S_depth_GM.append(J253S_GM.depth)
        J366S_depth_GM.append(J366S_GM.depth)
        J338S_flwrt_GM.append(J338S_GM.total_inflow * cfs_to_cms)
        J253S_flwrt_GM.append(J253S_GM.total_inflow * cfs_to_cms)
        J366S_flwrt_GM.append(J366S_GM.total_inflow * cfs_to_cms)

## GreenMaxxing + inlets v19 SIM ---------------------------------------------------------------------------------------------------------
# Initialize Lists for storing data
time_stamps_GMI = []
J338S_depth_GMI = []
J253S_depth_GMI = []
J366S_depth_GMI = []
J338S_flwrt_GMI = []
J253S_flwrt_GMI = []
J366S_flwrt_GMI = []

#run the simulation, instantiate BE nodes
with Simulation(r"/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19_greenmaxxing+inlets.inp") as sim:
    J338S_GMI = Nodes(sim)['J338-S']
    J253S_GMI = Nodes(sim)['J253-S']
    J366S_GMI = Nodes(sim)['J366-S']

#lets python access sim during run (i think)
    sim.step_advance(300)

# Launch simulation
    for ind, step in enumerate(sim):
        time_stamps_GMI.append(sim.current_time)
        J338S_depth_GMI.append(J338S_GMI.depth)
        J253S_depth_GMI.append(J253S_GMI.depth)
        J366S_depth_GMI.append(J366S_GMI.depth)
        J338S_flwrt_GMI.append(J338S_GMI.total_inflow * cfs_to_cms)
        J253S_flwrt_GMI.append(J253S_GMI.total_inflow * cfs_to_cms)
        J366S_flwrt_GMI.append(J366S_GMI.total_inflow * cfs_to_cms)


# Organize data into dictionaries for easier plotting
time_stamps_dict = {
    "Base": time_stamps,
    "BGN": time_stamps_BGN,
    "BGNx3": time_stamps_3BGN,
    "Inlets": time_stamps_inlets,
    "GreenMaxxed": time_stamps_GM,
    "GreenMaxxed_Inlets": time_stamps_GMI

}

depth_data = {
    "Base": {
        "J338S": J338S_depth,
        "J253S": J253S_depth,
        "J366S": J366S_depth
    },
    "BGN": {
        "J338S": J338S_depth_BGN,
        "J253S": J253S_depth_BGN,
        "J366S": J366S_depth_BGN
    },
    "BGNx3": {
        "J338S": J338S_depth_3BGN,
        "J253S": J253S_depth_3BGN,
        "J366S": J366S_depth_3BGN
    },
    "GM": {
        "J338S": J338S_depth_GM,
        "J253S": J253S_depth_GM,
        "J366S": J366S_depth_GM
    },
    "Inlets": {
        "J338S": J338S_depth_inlets,
        "J253S": J253S_depth_inlets,
        "J366S": J366S_depth_inlets
    },
    "GMI": {
        "J338S": J338S_depth_GMI,
        "J253S": J253S_depth_GMI,
        "J366S": J366S_depth_GMI
    }
}

#pull out max depths

max_depths = {}

for scenario, node_dict in depth_data.items():
    max_depths[scenario] = {node_id: max(depths) for node_id, depths in node_dict.items()}

# Calculate time below threshold (0.5 ft) for each scenario and node
threshold = 0.5  # ft
timestep_minutes = 5  # from your step_advance(300) = 300 seconds = 5 minutes

# Dictionary to store duration below threshold
duration_above_threshold = {}

for scenario, node_dict in depth_data.items():
    duration_above_threshold[scenario] = {}
    for node_id, depths in node_dict.items():
        count = sum(d >= threshold for d in depths)  # count timesteps below threshold
        duration_above_threshold[scenario][node_id] = count * timestep_minutes

# Prepare data for plotting
scenarios = list(duration_above_threshold.keys())
nodes = list(duration_above_threshold[scenarios[0]].keys())  # assuming all scenarios have same nodes

from itertools import cycle

colors = cycle(['lightsteelblue', 'cornflowerblue', 'royalblue', 'mediumblue', 'darkblue', 'black'])

# Create a bar plot for each node showing time below threshold by scenario
for node in nodes:
    plt.figure(figsize=(10, 6))

    # Get the time below threshold for this node across all scenarios
    times = [duration_above_threshold[scenario][node] for scenario in scenarios]

    # Create bars
    bars = plt.bar(scenarios, times, color=next(colors))

    # Customize the plot
    plt.title(f'Time above 6-Inch depth threshold at {node}')
    plt.ylabel('Time above threshold (mins)')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

## Plotting ------------------------------------------------------------------------------------------------------------

# Plot water depths for 3 B.E. nodes on one plot
fig = plt.figure(figsize=(8,4), dpi=200)
fig.suptitle("Broadway East Node Flowrate")
axis_1 = fig.add_subplot(1,1,1)

axis_1.plot(time_stamps, J338S_flwrt, color = 'c', label = 'Chase St. and Rutland St.')
axis_1.plot(time_stamps, J253S_flwrt, color = 'm', label = 'Eager St. and Rutland St.')
axis_1.plot(time_stamps, J366S_flwrt, color = 'y', label = 'Barnes Street')

axis_1.set_ylabel("Flowrate (cfs)")
axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %Hh'))
axis_1.legend()

fig.autofmt_xdate()
plt.tight_layout()
#plt.show()


# plot 3 scenarios on one graph
fig = plt.figure(figsize=(8,4), dpi=200)
fig.suptitle("Chase St. and Rutland St. Flowrate by Scenario")
axis_1 = fig.add_subplot(1,1,1)

axis_1.plot(time_stamps, J338S_flwrt, color = 'lightsteelblue', label = 'Base Model')
axis_1.plot(time_stamps_BGN, J338S_flwrt_BGN, color = 'cornflowerblue', label = 'BGN')
axis_1.plot(time_stamps_3BGN, J338S_flwrt_3BGN, color = 'royalblue', label = 'BGN x3')
axis_1.plot(time_stamps_GM, J338S_flwrt_GM, color = 'mediumblue', label = 'GreenMaxxed')
axis_1.plot(time_stamps_inlets, J338S_flwrt_inlets, color = 'darkblue', label = 'Inlets')
axis_1.plot(time_stamps_GMI, J338S_flwrt_GMI, color = 'black', label = 'GreenMaxxed + Inlets')

#uncomment to zoom to 1 hour before and after max depth
max_index = J338S_flwrt.index(max(J338S_flwrt))
max_time = time_stamps[max_index]
start_time = max_time - dt.timedelta(hours=1)
end_time = max_time + dt.timedelta(hours=1)
axis_1.set_ylim(3.5,6.5)
axis_1.set_xlim([start_time, end_time])

axis_1.set_ylabel("flowrate (cms)")
axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
axis_1.legend()

fig.autofmt_xdate()
plt.tight_layout()
plt.show()

#plot small multiples of 3 nodes, 3 scenarios
# plot 3 scenarios on one graph
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(8, 4), dpi=180, sharex=True, sharey=True)
fig.suptitle("Flooding Depth", fontsize=12)

# Color mapping for each scenario
scenario_colors = {
    "Base": "c",
    "BGN": "m",
    "Inlets": "y"
}

# Loop through nodes and scenarios
for row, scenario in enumerate(["Base", "BGN", "Inlets"]):
    for col, node_id in enumerate(["J338S", "J253S", "J366S"]):
        ax = axes[row, col]
        x = time_stamps_dict[scenario]
        y = depth_data[scenario][node_id]

        ax.plot(x, y, color=scenario_colors[scenario],)

        # labels
        if row == 0:
            ax.set_title(node_id, fontsize=10)
        if col == 0:
            ax.set_ylabel(f"{scenario}\nDepth (ft)", fontsize=10)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Hh'))
        ax.grid(True)
        ax.tick_params(labelsize=8)

fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.autofmt_xdate()
#plt.show()


# plot slope graph 
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 4), dpi=150, sharey=True)

# Plot Base → BGN
for node in node_ids:
    y_values = [max_depths["Base"][node], max_depths["BGN"][node]]
    ax.plot([0, 1], y_values, marker='o', color='m')
    ax.text(1.01, y_values[1], node, fontsize=8)

# Plot Base → Inlets
for node in node_ids:
    y_values = [max_depths["Base"][node], max_depths["Inlets"][node]]
    ax.plot([0, 1], y_values, marker='o', color='c')
    ax.text(1.01, y_values[1], node, fontsize=8)

# Final touches
ax.set_xticks([0, 1])
ax.set_xticklabels(["Base", "Infrastructure Scenario"])
ax.set_title("Infrastructure Scenario Improvements")

plt.tight_layout()
#plt.show()
'''