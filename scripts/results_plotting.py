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
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colormaps
import itertools
from pandas.plotting import parallel_coordinates
from scripts.config import scenarios

# DEFINITIONS ----------------------------------------------------------------------------------------------------------
# can use BE_nodes to plot a subset of locations. BE_nodes is sequential, upstream to downstream.
def plot_basedepth_with_hyetograph(processed_df, rain_df, BE_nodes):
    processed_df['timestamp'] = pd.to_datetime(processed_df['timestamp'])
    rain_df['dt'] = pd.to_datetime(rain_df['dt'])
    fig, ax1 = plt.subplots(figsize=(8, 5))
    df_plot = processed_df.loc['Base']

    # If plotting several nodes at a time (e.g., using BE_nodes), create a colormap and get N colors (N = number of nodes)
    cmap = cm.get_cmap('Oranges', len(BE_nodes))
    colors = cmap(np.linspace(0, 1, len(BE_nodes)))

    for i, node in enumerate(BE_nodes):
        ax1.plot(df_plot['timestamp'], df_plot[node], color=colors[i], label=node, linewidth=2)

    #plot just one node at a time
    #ax1.plot(df_plot['timestamp'], df_plot['J782-S_depth'], color='gold', linewidth=3)

    # plot rain on second axis as inverted. Limit range using xmin and xmax.
    xmin = pd.Timestamp('2023-06-27 2:30:00')
    xmax = pd.Timestamp('2023-06-27 5:00:00')
    ax2 = ax1.twinx()
    ax2.set_xlim([xmin, xmax])
    ax2.bar(rain_df['dt'], rain_df['rain_cm'], color='cornflowerblue', width=0.002)
    ax2.set_ylim(-0.05, 4)
    ax2.invert_yaxis()
    ax2.set_ylabel('Precipitation (cm)', color='cornflowerblue')

    # set formatting and save
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Time of Day')
    ax1.set_ylim(-0.05, 0.4)
    ax1.set_ylabel('depth (m)', color = 'orange')
    ax1.set_title('June 27, 2023: Broadway East Flood Depths')
    ax1.legend()
    ax1.grid(axis='y')
    plt.tight_layout()
    plt.show()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/BE_SequentialNodes_depth_firstburst.svg')

# plot flowrate over time for one node with inverted hyetograph, all scenarios (cms) (cms)
def plot_flowrt_with_hyetograph(processed_df, rain_df, scenarios):
    processed_df['timestamp'] = pd.to_datetime(processed_df['timestamp'])
    rain_df['dt'] = pd.to_datetime(rain_df['dt'])
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])

    for scenario in scenarios.keys():
        df_plot = processed_df.loc[scenario]
        current_color = next(colors)
        ax1.plot(df_plot['timestamp'], df_plot['J338-S_flow'], label=scenario, color=current_color)

    # plot rain on second axis as inverted.
    ax2 = ax1.twinx()
    ax2.depth(rain_df['dt'], rain_df['rain_cm'], color='slategrey', width=0.002)
    ax2.set_ylim(-0.05, 5)
    ax2.invert_yaxis()
    ax2.set_ylabel('Precipitation (cm)', color='slategrey')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Time of Day')
    ax1.set_ylabel('Flow (cms)')
    ax1.set_title('June 27, 2023: Broadway East Storm Flow')
    ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/flwrt_with_hyetograph_J338S.svg')


# plot depth over time for one node with inverted hyetograph, all scenarios (cms)
def plot_depth_with_hyetograph(processed_df, rain_df, scenarios):
    processed_df['timestamp'] = pd.to_datetime(processed_df['timestamp'])
    rain_df['dt'] = pd.to_datetime(rain_df['dt'])
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])
    for scenario in scenarios.keys():
        df_plot = processed_df.loc[scenario]
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
    ax1.set_title('June 27, 2023: Broadway East Flood Depth')
    ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    plt.show()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/depth_with_hyetograph_J338S.svg')


# plot max depths for one node, all scenarios (m)
def plot_depth_barchart(processed_df, scenarios):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])
    # scenarios = ('base', 'BGN', 'BGNx3', 'IC', 'GM', 'GM+IC')
    for scenario in scenarios.keys():
        df_plot = processed_df.loc[scenario].max()
        current_color = next(colors)
        ax1.bar(scenario, df_plot['J338-S_depth'], label=scenario, color=current_color)

    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('Depth (m)')
    ax1.set_title('June 27, 2023: Maximum Flood Depth in Broadway East')
    # ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/depth_barchart_J338S.svg')


# plot max flowrate for one node, all scenarios (cms)
def plot_flowrt_barchart(processed_df, scenarios):
    # bar chart showing max flowrate across scenarios
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])
    for scenario in scenarios.keys():
        df_plot = processed_df.loc[scenario].max()
        current_color = next(colors)
        ax1.bar(scenario, df_plot['J338-S_flow'], label=scenario, color=current_color)

    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('Depth (m)')
    ax1.set_title('June 27, 2023: Maximum Storm Flow in Broadway East')
    # ax1.legend(loc='center left')
    ax1.grid(axis='y')
    plt.tight_layout()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/flwrt_barchart_J338S.svg')

def boxplot_max_depth(max_depth_df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = max_depth_df['Base'], max_depth_df['BGN'], max_depth_df['BGNx3'], max_depth_df['GM'], max_depth_df['IC'], max_depth_df['GM+IC']
    labels = ['Base', 'BGN', 'BGNx3', 'GM', 'IC', 'GM+IC']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black']
    bplot = ax1.boxplot(x, patch_artist = True, tick_labels = labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Depth (m)')
    ax1.set_title('June 27, 2023: Maximum Flood Depths Across Baltimore Harbor')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/depth_boxplot_allnodes.svg')

def boxplot_max_flow(max_flow_df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = max_flow_df['Base'], max_flow_df['BGN'], max_flow_df['BGNx3'], max_flow_df['GM'], max_flow_df['IC'], max_flow_df['GM+IC']
    labels = ['Base', 'BGN', 'BGNx3', 'GM', 'IC', 'GM+IC']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black']
    bplot = ax1.boxplot(x, patch_artist = True, tick_labels = labels)
    #bplot = ax1.violinplot(x)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Flow (cms)')
    ax1.set_title('June 27, 2023: Maximum Flowrate Across Baltimore Harbor')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/flow_boxplot_allnodes.svg')

def boxplot_relative_depth(relative_depth_df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = relative_depth_df['Base'], relative_depth_df['BGN'], relative_depth_df['BGNx3'], relative_depth_df['GM'], relative_depth_df['IC'], relative_depth_df['GM+IC']
    labels = ['Base', 'BGN', 'BGNx3', 'GM', 'IC', 'GM+IC']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black']
    bplot = ax1.boxplot(x, patch_artist=True, tick_labels=labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Depth (m)')
    ax1.set_title('June 27, 2023: Relative Change in Flood Depth')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/Boxplot_RelativeDepth.svg')

def boxplot_watersheds_relative_depth(relative_depth_df):
    #make df long
    value_vars = ['Base', 'BGN', 'BGNx3', 'GM', 'IC', 'GM+IC']
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
    plt.title('Relative Change in Max Flood Depth')
    plt.legend(title='Neighborhood', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/Boxplot_RelativeDepth.svg')


def boxplot_relative_flow(relative_flow_df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = relative_flow_df['Base'], relative_flow_df['BGN'], relative_flow_df['BGNx3'], relative_flow_df['GM'], relative_flow_df['IC'], relative_flow_df['GM+IC']
    labels = ['Base', 'BGN', 'BGNx3', 'GM', 'IC', 'GM+IC']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black']
    bplot = ax1.boxplot(x, patch_artist=True, tick_labels=labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Flowrate (cms)')
    ax1.set_title('June 27, 2023: Relative Change in Flowrate')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/Boxplot_RelativeFlow.svg')


def boxplot_above_curb(depth_time_df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = depth_time_df['Base'], depth_time_df['BGN'], depth_time_df['BGNx3'], depth_time_df['GM'], depth_time_df['IC'], depth_time_df['GM+IC']
    labels = ['Base', 'BGN', 'BGNx3', 'GM', 'IC', 'GM+IC']
    colors = ['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black']
    bplot = ax1.boxplot(x, patch_artist = True, tick_labels = labels)

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    ax1.set_ylabel('Time (hour)')
    ax1.set_title('June 27, 2023: Duration of Flooding Above Curb')
    plt.tight_layout()
    ax1.grid(axis='y')
    plt.show()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/AboveCurb_allnodes.svg')

def depth_parallelcoord(relative_depth_df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    unwanted = ['Northside, Drains to Harbor', 'Southside, Drains to Harbor', 'Armistead Creek']
    plot_df = relative_depth_df[~relative_depth_df['historic_stream'].isin(unwanted)]
    plot_cols = ['historic_stream', 'Base', 'BGN', 'BGNx3', 'GM', 'IC', 'GM+IC']
    colors = ['lightskyblue', 'blue']
    pd.plotting.parallel_coordinates(plot_df[plot_cols], 'historic_stream', color = colors)

    ax1.set_ylabel('Depth (m)')
    ax1.set_title('June 27, 2023: Relative Improvement of Depth of Flooding')
    ax1.get_legend()
    ax1.legend(loc = 'center left')
    plt.tight_layout()
    ax1.grid(axis='y')
    #plt.show()
    plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/Relative_ParallelPlot_Depth.svg')

def flow_parallelcoord(relative_flow_df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    pd.plotting.parallel_coordinates(relative_flow_df, 'neighborhood',  colormap = 'jet')

    ax1.set_ylabel('Flowrate (cfs)')
    ax1.set_title('June 27, 2023: Flowrate')
    ax1.get_legend(loc = 'center left')
    plt.tight_layout()
    ax1.grid(axis='y')
    plt.show()
    #plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/ParallelPlot_Flow.svg')


# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # load dfs
    processed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_simV19_AllNodes.csv', index_col=[0, 1])
    max_flow_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_MaxFlow.csv')
    max_depth_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_MaxDepth.csv')
    relative_depth_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_RelativeDepth.csv').drop(['Unnamed: 0'],axis=1)
    relative_flow_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_RelativeFlow.csv').drop(['Unnamed: 0'],axis=1)
    depth_time_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_V19_AllNodes_TimeDepth.csv')
    rain_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_23_rain_df.csv')
    BE_nodes = ['J1-S_depth', 'J260-S_depth','J801-S_depth', 'J280-S_depth', 'J278-S_depth', 'J329-S_depth',
                'J338-S_depth', 'J253-S_depth', 'J366-S_depth', 'J361-S_depth', 'J637-S_depth']


    # execute
    # relative means relative to base case
    plot_basedepth_with_hyetograph(processed_df, rain_df, BE_nodes)
    #plot_flowrt_with_hyetograph(processed_df, rain_df, scenarios) #problems with yaxis
    #plot_depth_with_hyetograph(processed_df, rain_df, scenarios)
    #plot_flowrt_barchart(processed_df, scenarios)
    #plot_depth_barchart(processed_df, scenarios)
    #boxplot_max_depth(max_depth_df)
    #boxplot_max_flow(max_flow_df)
    #boxplot_relative_depth(relative_depth_df)
    #boxplot_relative_flow(relative_flow_df)
    #boxplot_watersheds_relative_depth(relative_depth_df)
    #boxplot_above_curb(depth_time_df)
    #depth_parallelcoord(relative_depth_df)
    #flow_parallelcoord(relative_flow_df)


