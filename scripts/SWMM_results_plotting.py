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
def depth_parallelcoord(max_depth_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 4))
    # Columns to plot (first is the class column)
    plot_cols = ['neighborhood', 'Base', 'I', 'V', 'V&I']
    # Get unique neighborhoods sorted
    unique_neighborhoods = sorted(max_depth_df['neighborhood'].unique())
    num_neigh = len(unique_neighborhoods)

    # plot only broadway east in color
    colors = ['mediumpurple' if n == 'Broadway East' or n == 'Eager Park' or n == 'Dunbar-Broadway' else 'lightgrey' for n in unique_neighborhoods]

    #plot
    pd.plotting.parallel_coordinates(max_depth_df[plot_cols], 'neighborhood', color=colors, ax=ax1)
    ax1.set_ylabel('Depth (m)')
    ax1.set_title(f'{name} Storm: Depth of Flooding')
    ax1.set_ylim(0,1.1)
    ax1.grid(axis='y')

    # legend
    patches = [mpatches.Patch(color=colors[i], label=unique_neighborhoods[i]) for i in range(num_neigh)]
    ax1.legend(handles=patches, title='Neighborhood', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    svg_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_absolute_ParallelPlot_Depth.svg'
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_absolute_ParallelPlot_Depth.png'
    plt.savefig(svg_path)
    plt.savefig(save_path)

def volume_parallelcoord(max_volume_df, name):
    fig, ax1 = plt.subplots(figsize=(10, 4))
    # Columns to plot (first is the class column)
    plot_cols = ['neighborhood', 'Base', 'I', 'V', 'V&I']
    # Get unique neighborhoods sorted
    unique_neighborhoods = sorted(max_volume_df['neighborhood'].unique())
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
    pd.plotting.parallel_coordinates(max_volume_df[plot_cols], 'neighborhood', color=colors, ax=ax1)
    ax1.set_ylabel('Flood volume (m\u00b3)')
    ax1.set_title(f'{name} Storm: Flood Volume')
    ax1.grid(axis='y')
    ax1.set_ylim(-30, 45)

    # legend
    patches = [mpatches.Patch(color=colors[i], label=unique_neighborhoods[i]) for i in range(num_neigh)]
    ax1.legend(handles=patches, title='Neighborhood', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    save_path = f'/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/nodes/{name}_Absolute_ParallelPlot_Volume.png'
    plt.savefig(save_path)

# EXECUTION ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # load dfs

    max_depth_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_23_V22_AllNodes_MaxDepth.csv')
    relative_depth_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_23_V22_AllNodes_RelativeDepth.csv').drop(['Unnamed: 0'],axis=1)
    relative_volume_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_23_V22_AllNodes_RelativeVolume.csv').drop(['Unnamed: 0'], axis=1)
    max_volume_df = pd.read_csv( '/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/nodes/6_27_23_V22_AllNodes_MaxVolume.csv').drop(['Unnamed: 0'], axis=1)

    storm_name = '6_27_23'
    #execute, note 'relative' functions means the result is relative to base case
    depth_parallelcoord(max_depth_df, storm_name)
    volume_parallelcoord(relative_volume_df, storm_name)

