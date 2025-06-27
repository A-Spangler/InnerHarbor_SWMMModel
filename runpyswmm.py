# By: Ava Spangler
# Date: 6/10/2025

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
import itertools
from scripts.config import scenarios
from scripts.config import model_path

cfs_to_cms = (12**3)*(2.3**3)*(1/100**3)
ft_to_m = 12*2.54*(1/100)

def list_street_nodes(model_path):
    nodes_df = model.nodes.dataframe
    nodes_df = nodes_df.reset_index()
    node_names = nodes_df['Name'].tolist()
    street_node_names = [k for k in node_names if '-S' in k]
    return street_node_names


#model_path = '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.inp'
model = swmmio.Model(model_path)
node_ids = list_street_nodes(model_path)


## run all scenarios ------------------------------------------------------------------------------------------------------------
# Initialize dictionaries for storing data from each scenario, for each node, for each property
# function to run pyswmm and save outputs as dict
def run_pyswmm(inp_path, node_ids):
    output = {node: {'depth': [], 'flow': []} for node in node_ids}
    time_stamps = []
# run inp_path simulation, instantiate BE nodes
    with Simulation(inp_path) as sim:
        nodes = {node_id: Nodes(sim)[node_id] for node_id in node_ids} #dictionary with nodes
        sim.step_advance(300) #lets python access sim during run (300 sec = 5min inetervals)

        # Launch inp_path simulation
        for step in enumerate(sim):
            time_stamps.append(sim.current_time)
            for node_id, node in nodes.items(): # store node flow and depth data in node dictionary
                output[node_id]['depth'].append(node.depth*ft_to_m)
                output[node_id]['flow'].append(node.total_inflow*cfs_to_cms)

        # construct df
        node_data = {'timestamp': time_stamps} #dictionary of timestamps
        for node_id in node_ids:
            node_data[f'{node_id}_depth'] = output[node_id]['depth']
            node_data[f'{node_id}_flow'] = output[node_id]['flow']

        df_node_data = pd.DataFrame(node_data).copy()
        return df_node_data

scenario_results = {}
for scenario_name, inp_path in scenarios.items():
    print(f"Running scenario: {scenario_name}")
    scenario_results[scenario_name] = run_pyswmm(inp_path, node_ids)

# Combine into a single multiindex df
processed_df = pd.concat(scenario_results, names=['scenario'])
processed_df.index.set_names(['scenario', 'row'], inplace=True)

processed_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_simV19_test.csv', index=False)


# analysis -------------------------------------------------------------------------------------------------------------
# find maximums from each column in the multiindex df
max_df = processed_df.groupby(level=0).max()

#group each column based on if it is depth or flowrate



## rainfall data--------------------------------------------------------------------------------------------------------
df_rain = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/Validation/2023June27.xlsx')

# combine date and time, convert to datetime
df_rain['dt'] = pd.to_datetime(df_rain['date'].astype(str) + ' ' + df_rain['time'].astype(str))

#rainfall (inches *2.54 for plotting in cm)
df_rain['rain_cm'] = df_rain['rain_inches']*2.54


## Plotting------------------------------------------------------------------------------------------------------------

# plot peak depth for all nodes in inner harbor as boxplots
''''
fig, ax1 = plt.subplots(figsize=(10, 5))
colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])
# scenarios = ('base', 'BGN', 'BGNx3', 'IC', 'GM', 'GM+IC')
for scenario in scenarios.keys():
    df_plot = max_df.loc[scenario]
    current_color = next(colors)
   # ax1.boxplot(scenario, df_plot['J338-S_depth'], label=scenario, color=current_color)

ax1.set_xlabel('Scenario')
ax1.set_ylabel('Depth (m)')
ax1.set_title('June 27, 2023: Maximum Flood Depth in Broadway East')
# ax1.legend(loc='center left')
ax1.grid(axis='y')
plt.tight_layout()
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/flwrt_barchart_J338S.svg')
'''
'''
# plot flow (in CMS) across scenarios
fig, ax1 = plt.subplots(figsize=(10, 5))
colors = itertools.cycle(['lightblue','cornflowerblue','royalblue', 'blue', 'darkblue', 'black'])

for scenario in scenarios.keys():
    df_plot = processed_df.loc[scenario]
    current_color = next(colors)
    ax1.plot(df_plot['timestamp'], df_plot['J338-S_flow'], label=scenario, color=current_color)

#plot rain as inverted. Should be bar chart but its not working
ax2 = ax1.twinx()
ax2.plot(df_rain['dt'], df_rain['rain_cm'], color='slategrey')
ax2.set_ylim(-0.05,5)
ax2.invert_yaxis()
ax2.set_ylabel('Precipitation (cm)', color='slategrey')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.set_xlabel('Time of Day')
ax1.set_ylabel('Flow (cms)')
ax1.set_title('June 27, 2023: Broadway East Storm Flow')
ax1.legend(loc='center left')
ax1.grid(axis='y')
plt.tight_layout()
plt.show()
'''

# Plot water depths for 1 B.E. node across scenarios
fig, ax1 = plt.subplots(figsize=(10, 5))
colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])

for scenario in scenarios.keys():
    df_plot = combined_df.loc[scenario]
    current_color = next(colors)
    ax1.plot(df_plot['timestamp'], df_plot['J338-S_depth'], label=scenario, color = current_color)

#uncomment to zoom to 1 hour before and after max depth
#max_index = combined_df['J338S_flow'].max
#max_time = combined_df['J338S_flow'].max
#start_time = max_time - dt.timedelta(hours=1)
#end_time = max_time + dt.timedelta(hours=1)
#ax.set_ylim(3.5,6.5)
#ax.set_xlim([start_time, end_time])
#plot rain as inverted. Should be bar chart
#plot rain as inverted. Should be bar chart but its not working

ax2 = ax1.twinx()
ax2.plot(df_rain['dt'], df_rain['rain_cm'], color='slategrey')
ax2.set_ylim(-0.05,3)
ax2.invert_yaxis()
ax2.set_ylabel('Precipitation (cm)', color='slategrey')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.set_xlabel('Time of Day')
ax1.set_ylabel('Depth (m)')
ax1.set_title('June 27, 2023: Broadway East Flood Depth')
ax1.legend(loc = 'center left')
ax1.grid(axis='y')
plt.tight_layout()
plt.show()


'''
# Plot time above 6inch threshold for each scenario
fig, ax1 = plt.subplots(figsize=(10, 5))
for scenario in scenarios.keys():
    df_plot = combined_df.loc[scenario]
    ax1.plot(df_plot['timestamp'], df_plot['J338-S_depth'], label=scenario)

# bar chart showing max flowrate across scenarios
fig, ax1 = plt.subplots(figsize=(10, 5))
colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])
#scenarios = ('base', 'BGN', 'BGNx3', 'IC', 'GM', 'GM+IC')
for scenario in scenarios.keys():
    df_plot = combined_df.loc[scenario].max()
    current_color = next(colors)
    ax1.bar(scenario, df_plot['J338-S_depth'], label=scenario, color = current_color)

ax1.set_xlabel('Scenario')
ax1.set_ylabel('Depth (m)')
ax1.set_title('June 27, 2023: Maximum Flood Depth in Broadway East')
#ax1.legend(loc='center left')
ax1.grid(axis='y')
plt.tight_layout()
plt.show()

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