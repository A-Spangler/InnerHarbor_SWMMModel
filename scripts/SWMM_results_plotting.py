# By: Ava Spangler
# Date: 6/26/2025
# Description: This code takes in processed and analyzed data and creates visualizations

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pyswmm
import numpy as np
import pandas as pd
import seaborn as sns
import datetime as dt
from datetime import datetime
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colormaps
import itertools
from pandas.plotting import parallel_coordinates
from scripts.config import scenarios
import matplotlib.patches as mpatches

# DEFINITIONS ----------------------------------------------------------------------------------------------------------
# can use BE_nodes to plot a subset of locations. BE_nodes is sequential, upstream to downstream.
def plot_basedepth_with_hyetograph(processed_nodes_df, rain_df, BE_nodes, name):
    processed_nodes_df['timestamp'] = pd.to_datetime(processed_nodes_df['timestamp'])
    rain_df['dt'] = pd.to_datetime(rain_df['dt'])
    fig, ax1 = plt.subplots(figsize=(27, 5))
    df_plot = processed_nodes_df.loc['Base']

    cmap = matplotlib.colormaps['Blues']
    cmap = cmap.resampled(len(BE_nodes))
    colors = cmap(range(cmap.N))

    for i, node in enumerate(BE_nodes):
        #ax1.plot(df_plot['timestamp'], df_plot[node], color=colors[i], label=node, linewidth=2)
        ax1.plot(df_plot['timestamp'], df_plot[node], color=colors[i], linewidth=2)

    #plot just one node at a time
    #ax1.plot(df_plot['timestamp'], df_plot['J782-S_depth'], color='gold', linewidth=3)

    # plot rain on second axis as inverted. Limit range using xmin and xmax.
    #xmin = pd.Timestamp('2023-06-27 2:30:00')
    #xmax = pd.Timestamp('2023-06-27 5:00:00')
    ax2 = ax1.twinx()
    #ax2.set_xlim([xmin, xmax])
    ax2.bar(rain_df['dt'], rain_df['rain_cm'], color='cornflowerblue', width=0.002)
    ax2.set_ylim(-0.05, 4)
    ax2.invert_yaxis()
    ax2.set_ylabel('Precipitation (cm)', color='cornflowerblue')

    # set formatting and save
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Time of Day')
    ax1.set_ylim(-0.05, 0.4)
    ax1.set_ylabel('depth (m)', color = 'darkblue')
    ax1.set_title(f'{name} Storm: J329 Depth')
    #ax1.legend()
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_J329_BaseDepth.png'
    plt.savefig(save_path)

# plot flowrate over time for one node with inverted hyetograph, all scenarios (cms) (cms)
def plot_flowrt_with_hyetograph(processed_nodes_df, rain_df, scenarios, name):
    processed_nodes_df['timestamp'] = pd.to_datetime(processed_nodes_df['timestamp'])
    rain_df['dt'] = pd.to_datetime(rain_df['dt'])
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue'])

    for scenario in scenarios.keys():
        df_plot = processed_nodes_df.loc[scenario]
        current_color = next(colors)
        ax1.plot(df_plot['timestamp'], df_plot['J338-S_flow'], label=scenario, color=current_color)

    # plot rain on second axis, inverted
    ax2 = ax1.twinx()
    ax2.bar(rain_df['dt'], rain_df['rain_cm'], color='slategrey', width=0.002)
    ax2.set_ylim(-0.05, 5)
    ax2.invert_yaxis()
    ax2.set_ylabel('Precipitation (cm)', color='slategrey')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Time of Day')
    ax1.set_ylabel('Flow (cms)')
    ax1.set_title(f'{name} Storm: Broadway East Storm Flow')
    ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.show()
    save_path =  f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_flwrt_with_hyetograph_J338S.png'
    plt.savefig(save_path)


# plot depth over time for one node with inverted hyetograph, all scenarios (cms)
def plot_depth_with_hyetograph(processed_nodes_df, rain_df, scenarios, name):
    processed_nodes_df['timestamp'] = pd.to_datetime(processed_nodes_df['timestamp'])
    rain_df['dt'] = pd.to_datetime(rain_df['dt'])
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue'])
    for scenario in scenarios.keys():
        df_plot = processed_nodes_df.loc[scenario]
        current_color = next(colors)
        ax1.plot(df_plot['timestamp'], df_plot['J338-S_depth'], label=scenario, color=current_color)

    # plot rain on second axis as inverted.
    ax2 = ax1.twinx()
    ax2.bar(rain_df['dt'], rain_df['rain_cm'], color='slategrey', width=0.002)
    ax2.set_ylim(-0.05, 5)
    ax2.invert_yaxis()
    ax2.set_ylabel('Precipitation (cm)', color='slategrey')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Time of Day')
    ax1.set_ylabel('Flow (cms)')
    ax1.set_title(f'{name} Storm: Broadway East Flood Depth')
    ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_depth_with_hyetograph_J338S.png'
    plt.savefig(save_path)

# plot max depths for one node, all scenarios (m)
def plot_depth_barchart(processed_nodes_df, scenarios, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue'])
    # scenarios = ('base', 'BGN', 'BGNx3', 'V', 'I', 'V+I')
    for scenario in scenarios.keys():
        df_plot = processed_nodes_df.loc[scenario].max()
        current_color = next(colors)
        ax1.bar(scenario, df_plot['J338-S_depth'], label=scenario, color=current_color)

    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('Depth (m)')
    ax1.set_title(f'{name} Storm: Maximum Flood Depth in Broadway East')
    # ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_depth_barchart_J338S.png'
    plt.savefig(save_path)

# plot max flowrate for one node, all scenarios (cms)
def plot_flowrt_barchart(processed_nodes_df, scenarios, name):
    # bar chart showing max flowrate across scenarios
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue'])
    for scenario in scenarios.keys():
        df_plot = processed_nodes_df.loc[scenario].max()
        current_color = next(colors)
        ax1.bar(scenario, df_plot['J338-S_flow'], label=scenario, color=current_color)

    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('Flowrate (cms)')
    ax1.set_title(f'{name} Storm: Maximum Storm Flow in Broadway East')
    # ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_flwrt_barchart_J338S.png'
    plt.savefig(save_path)
def boxplot_max_depth(max_depth_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = max_depth_df['Base'], max_depth_df['V'], max_depth_df['I'], max_depth_df['V&I']
    labels = ['Base', 'V', 'I', 'V+I']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue']
    bplot = ax1.boxplot(x, patch_artist = True, tick_labels = labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Depth (m)')
    ax1.set_title(f'{name} Storm: Maximum Flood Depths Across Baltimore Harbor')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_depth_boxplot_allnodes.png'
    plt.savefig(save_path)

def boxplot_max_flow(max_flow_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = max_flow_df['Base'],  max_flow_df['V'], max_flow_df['I'], max_flow_df['V&I']
    labels = ['Base', 'V', 'I', 'V+I']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue']
    bplot = ax1.boxplot(x, patch_artist = True, tick_labels = labels)
    #bplot = ax1.violinplot(x)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Flow (cms)')
    ax1.set_title(f'{name} Storm: Maximum Flowrate Across Baltimore Harbor')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_flow_boxplot_allnodes.png'
    plt.savefig(save_path)

def boxplot_relative_depth(relative_depth_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = relative_depth_df['Base'],  relative_depth_df['V'], relative_depth_df['I'], relative_depth_df['V&I']
    labels = ['Base', 'V', 'I', 'V+I']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue']
    bplot = ax1.boxplot(x, patch_artist=True, tick_labels=labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Depth (m)')
    ax1.set_title(f'{name} Storm: Relative Change in Flood Depth')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_Boxplot_RelativeDepth.png'
    plt.savefig(save_path)

def boxplot_watersheds_relative_depth(relative_depth_df, name):
    #make df long
    value_vars = ['Base', 'V', 'I', 'V&I']
    long_df = relative_depth_df.melt(
        id_vars=['node_name', 'node_id', 'historic_stream'],
        value_vars=value_vars,
        var_name='scenario',
        value_name='relative_depth'
    )
    # arrange neighborhood order
    #neighborhood_order = ['Clifton Park', 'Broadway East', 'Eager Park', 'Dunbar-Broadway',
                          #'Washington Hill', 'Berea', 'Madison-Eastend', 'McElderry Park', 'Johnston Square', 'Patterson Park', 'Downtown', 'Canton',
                          #'Canton Industrial Area', 'Federal Hill', 'Fells Point', 'Upper Fells Point', 'Locust Point',
                          #'Orangeville', 'Baltimore Highlands', ]
    #long_df['neighborhood'] = pd.Categorical(
    #    long_df['neighborhood'],
    #    categories=neighborhood_order,
    #    ordered=True
    #)

    #plot
    plt.figure(figsize=(14, 5))
    sns.boxplot(
        data=long_df,
        x='historic_stream',
        y='relative_depth',
        hue='scenario',  # Each color = one neighborhood
        showfliers=False
    )
    plt.ylabel('Relative Depth (m)')
    plt.title(f'{name} Storm: Relative Change in Max Flood Depth')
    plt.legend(title='Neighborhood', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.grid(axis='y')
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_WatershedBoxplot_RelativeDepth.png'
    plt.savefig(save_path)


def boxplot_relative_flow(relative_flow_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = relative_flow_df['Base'], relative_flow_df['V'],  relative_flow_df['I'], relative_flow_df['V&I']
    labels = ['base', 'V', 'I', 'V+I']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue']
    bplot = ax1.boxplot(x, patch_artist=True, tick_labels=labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Flowrate (cms)')
    ax1.set_title(f'{name} Storm: Relative Change in Flowrate')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_Boxplot_RelativeFlow.png'
    plt.savefig(save_path)

def boxplot_relative_veloc(relative_veloc_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = relative_veloc_df['Base'], relative_veloc_df['V'],  relative_veloc_df['I'], relative_veloc_df['V&I']
    labels = ['base', 'V', 'I', 'V+I']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue']
    bplot = ax1.boxplot(x, patch_artist=True, tick_labels=labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Relative Velocity (m/s)')
    ax1.set_title(f'{name} Storm: Relative Change in Flow Velocity')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/links/{name}_Boxplot_RelativeVelocity.png'
    plt.savefig(save_path)


def boxplot_relative_duration_above_curb(relative_duration_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    labels = ['Base', 'V', 'I', 'V+I']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue']

    # Select only scenario columns (exclude 'node' column)
    scenario_cols = [col for col in relative_duration_df.columns if col != 'node']
    data_to_plot = [relative_duration_df[col].values for col in scenario_cols]
    bplot = ax1.boxplot(data_to_plot, tick_labels=labels, patch_artist=True)

     #fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Time (min)')
    ax1.set_xlabel('Scenario')
    ax1.set_title(f'{name} Storm: Duration of Flooding Above Curb')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_AboveCurb_allnodes.png'
    plt.savefig(save_path)

def depth_parallelcoord(relative_depth_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    # Columns to plot (first is the class column)
    plot_cols = ['neighborhood', 'Base', 'V', 'I', 'V&I']
    # Get unique neighborhoods sorted
    unique_neighborhoods = sorted(relative_depth_df['neighborhood'].unique())
    num_neigh = len(unique_neighborhoods)

    # plot only broadway east in color
    colors = ['mediumpurple' if n == 'Broadway East' or n == 'Dunbar-Broadway' or n == 'Eager Park' else 'lightgrey' for n in unique_neighborhoods]

    #color by nieghborhood
    #cmap = matplotlib.colormaps['tab20']
    #cmap = cmap.resampled(num_neigh)
    #colors = [cmap(i) for i in range(num_neigh)]
    # Create a mapping of neighborhood to color (optional, not required for parallel_coordinates itself)
    #color_map = {nb: colors[i] for i, nb in enumerate(unique_neighborhoods)}

    #plot
    pd.plotting.parallel_coordinates(relative_depth_df[plot_cols], 'neighborhood', color=colors, ax=ax1)
    ax1.set_ylabel('Depth (m)')
    ax1.set_title(f'{name} Storm: Relative Improvement of Depth of Flooding')
    ax1.set_ylim(-0.15,0.15)
    ax1.grid(axis='y')

    # legend
    patches = [mpatches.Patch(color=colors[i], label=unique_neighborhoods[i]) for i in range(num_neigh)]
    ax1.legend(handles=patches, title='Neighborhood', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    svg_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_Relative_ParallelPlot_Depth.svg'
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_Relative_ParallelPlot_Depth.png'
    plt.savefig(svg_path)
    plt.savefig(save_path)

def volume_parallelcoord(relative_volume_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    # Columns to plot (first is the class column)
    plot_cols = ['neighborhood', 'Base', 'V', 'I', 'V&I']
    # Get unique neighborhoods sorted
    unique_neighborhoods = sorted(relative_volume_df['neighborhood'].unique())
    num_neigh = len(unique_neighborhoods)

    # plot only broadway east as blue
    colors = ['yellowgreen' if n == 'Broadway East' or n == 'Dunbar-Broadway' or n == 'Eager Park' else 'lightgrey' for n in unique_neighborhoods]

    #color by nieghborhood
    #cmap = matplotlib.colormaps['tab20']
    #cmap = cmap.resampled(num_neigh)
    #colors = [cmap(i) for i in range(num_neigh)]
    # Create a mapping of neighborhood to color (optional, not required for parallel_coordinates itself)
    #color_map = {nb: colors[i] for i, nb in enumerate(unique_neighborhoods)}

    #plot
    pd.plotting.parallel_coordinates(relative_volume_df[plot_cols], 'neighborhood', color=colors, ax=ax1)
    ax1.set_ylabel('Flood volume (m\u00b3)')
    ax1.set_title(f'{name} Storm: Relative Improvement in Flood Volume')
    ax1.grid(axis='y')

    # legend
    patches = [mpatches.Patch(color=colors[i], label=unique_neighborhoods[i]) for i in range(num_neigh)]
    ax1.legend(handles=patches, title='Neighborhood', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_Relative_ParallelPlot_Volume.png'
    plt.savefig(save_path)

def veloc_parallelcoord(relative_veloc_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    # Columns to plot (first is the class column)
    plot_cols = ['neighborhood', 'Base', 'V', 'I', 'V&I']

    # plot only broadway east as blue
    neighborhood_order = relative_veloc_df['neighborhood'].unique()
    #blue for 'Broadway East', grey for others
    colors = ['blue' if n == 'Broadway East' or n == 'Eager Park' else 'grey' for n in neighborhood_order]

    # Get unique neighborhoods sorted
    #relative_veloc_df['neighborhood'] = relative_veloc_df['neighborhood'].astype(str)
    #unique_neighborhoods = sorted(relative_veloc_df['neighborhood'].unique())
    #num_neigh = len(unique_neighborhoods)

    #qualitative colormap
    #cmap = matplotlib.colormaps['tab20']
    #cmap = cmap.resampled(num_neigh)
    #colors = [cmap(i) for i in range(num_neigh)]
    # Create a mapping of neighborhood to color (optional, not required for parallel_coordinates itself)
    #color_map = {nb: colors[i] for i, nb in enumerate(unique_neighborhoods)}

    # plot
    pd.plotting.parallel_coordinates(relative_veloc_df[plot_cols], 'neighborhood', color=colors, ax=ax1)
    ax1.set_ylabel('Change in Velocity Relative to Base Scenario (m/s)')
    ax1.set_title(f'{name} Storm: Relative Change in Flood Velocity')
    ax1.grid(axis='y')

    ax1.legend(title='Neighborhood', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/links/SCS1a_V22 Relative_ParallelPlot_Veloc.png'
    plt.savefig(save_path)



# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # load dfs
    processed_nodes_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_simV22_AllNodes.csv', index_col=[0, 1])
    max_flow_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_V22_AllNodes_MaxFlow.csv')
    max_depth_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_V22_AllNodes_MaxDepth.csv')
    duration_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_V22_AllNodes_DurationOverCurb.csv')
    relative_depth_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_V22_AllNodes_RelativeDepth.csv').drop(['Unnamed: 0'],axis=1)
    relative_flow_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_V22_AllNodes_RelativeFlow.csv').drop(['Unnamed: 0'],axis=1)
    relative_duration_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_V22_AllNodes_RelativeDurationOverCurb.csv').drop(['Unnamed: 0'],axis=1)
    rain_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/rainfall/6_27_23_rain_df.csv')
    relative_veloc_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/links/1_9_2024_V22_AllNodes_RelativeVelocity.csv').drop(['Unnamed: 0'], axis=1)
    relative_volume_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/1_9_2024_V22_AllNodes_RelativeVolume.csv').drop(['Unnamed: 0'], axis=1)
    #BE_nodes = ['J329-S_depth']
    BE_nodes = ['J1-S_depth', 'J260-S_depth','J801-S_depth', 'J280-S_depth', 'J278-S_depth', 'J329-S_depth',
                'J338-S_depth', 'J253-S_depth', 'J366-S_depth', 'J361-S_depth', 'J637-S_depth']

    storm_name = 'January 9, 2024'
    #execute, note 'relative' functions means the result is relative to base case
    #plot_basedepth_with_hyetograph(processed_nodes_df, rain_df, BE_nodes)
    #plot_flowrt_with_hyetograph(processed_nodes_df, rain_df, scenarios)
    #plot_depth_with_hyetograph(processed_nodes_df, rain_df, scenarios)
    plot_flowrt_barchart(processed_nodes_df, scenarios, storm_name)
    plot_depth_barchart(processed_nodes_df, scenarios, storm_name)
    ##plot_duration_barchart(processed_nodes_df, scenarios, name) #TODO
    boxplot_max_depth(max_depth_df, storm_name)
    boxplot_max_flow(max_flow_df, storm_name)
    boxplot_relative_depth(relative_depth_df, storm_name)
    boxplot_relative_flow(relative_flow_df, storm_name)
    boxplot_relative_veloc(relative_veloc_df, storm_name)
    boxplot_watersheds_relative_depth(relative_depth_df, storm_name)
    boxplot_relative_duration_above_curb(relative_duration_df, storm_name)
    depth_parallelcoord(relative_depth_df, storm_name)
    veloc_parallelcoord(relative_veloc_df, storm_name)
    volume_parallelcoord(relative_volume_df, storm_name)

