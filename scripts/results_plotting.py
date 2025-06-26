# By: Ava Spangler
# Date: 6/26/2025
# Description: This code takes in processed and analyzed data and creates visualizations

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pyswmm
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import itertools
from pyswmm import Simulation, Nodes, Links, Subcatchments, LidControls, LidGroups


# DEFINITIONS ----------------------------------------------------------------------------------------------------------
def plot_flowrt_with_hyetograph(processed_df, rain_df, scenarios):
    # plot flowrate (in CMS) across scenarios
    fig, ax1 = plt.subplots(figsize=(10, 5))
    colors = itertools.cycle(['lightblue', 'cornflowerblue', 'royalblue', 'blue', 'darkblue', 'black'])

    for scenario in scenarios.keys():
        df_plot = processed_df.loc[scenario]
        current_color = next(colors)
        ax1.plot(df_plot['timestamp'], df_plot['J338-S_flow'], label=scenario, color=current_color)

    # plot rain on second axis as inverted. Should be bar chart but its not working
    ax2 = ax1.twinx()
    ax2.plot(rain_df['dt'], rain_df['rain_cm'], color='slategrey')
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
    plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/flwrt_with_hyetograph_J338S.svg')


def plot_flowrt_barchart(processed_df, scenarios):
    # bar chart showing max flowrate across scenarios
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
    plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/flwrt_barchart_J338S.svg')

# EXECUTION ------------------------------------------------------------------------------------------------------------
processed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_2023_simV19.csv'
                           , index_col=[0, 1])
# analyzed_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/analyzed/6_27_23_simV19_analyzed')
rain_df = pd.read_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_23_rain_df.csv')

scenarios = processed_df.loc('base', 'BGN', 'BGNx3', 'IC', 'GM', 'GM+IC')
plot_flowrt_with_hyetograph(processed_df, rain_df, scenarios)
# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------
