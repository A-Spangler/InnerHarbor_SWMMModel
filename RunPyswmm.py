import pyswmm
import pandas as pd
import swmmio
from IPython.display import HTML
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups
import numpy as np
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

cfs_to_cms = (12**3)*(2.3**3)*(1/100**3)
ft_to_m = 12*2.54*(1/100)


node_ids = ["J338-S", "J253-S", "J366-S",]

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
def run_pyswmm(inp_path, node_ids):
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
                output[node_id]['depth'].append(node.depth*ft_to_m)
                output[node_id]['flow'].append(node.total_inflow*cfs_to_cms)

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

# Optional: Combine all into a single DataFrame with multi-index
combined_df = pd.concat(scenario_results, names=['scenario', 'row'])

# print(scenario_results['BGN'].tail())

## rainfall data--------------------------------------------------------------------------------------------------------

df = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/Validation/2023June27.xlsx')

# combine date and time, convert to datetime
df['dt'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

#rainfall (inches *2.54 for plotting in cm)
df['rain_cm'] = df['rain_inches']*2.54
dt = df['dt']
rain_cm = df['rain_cm']

## Plotting------------------------------------------------------------------------------------------------------------

# plot flow (in CMS) across scenarios
fig, ax1 = plt.subplots(figsize=(10, 5))
for scenario in scenarios.keys():
    df = combined_df.loc[scenario]
    ax1.plot(df['timestamp'], df['J338-S_flow'], label=scenario)

ax2 = ax1.twinx()
ax2.plot(dt, rain_cm, color='b')
ax2.set_ylim(-0.05,5)
ax2.invert_yaxis()
ax2.set_ylabel('Precipitation (cm)', color='b')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.set_xlabel('Time of Day')
ax1.set_ylabel('Flow (cms)')
ax1.set_title('June 27, 2023: J338-S Flow Across Scenarios')
ax1.legend('center right')
ax1.grid(True)
plt.tight_layout()
plt.show()

'''
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