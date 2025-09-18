import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from collections import defaultdict

# Import scenarios dict from your config module
from scripts.config import scenarios


def parse_inp_polygons(inp_path):
    polygons = defaultdict(list)
    reading = False

    with open(inp_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('[POLYGONS]'):
                reading = True
                continue
            if reading and line.startswith('['):  # end of [POLYGONS] section
                break
            if reading and not line.startswith(';') and line:
                parts = line.split()
                subcatch_id = parts[0]
                x, y = map(float, parts[1:3])
                polygons[subcatch_id].append((x, y))

    poly_ids = []
    geometries = []
    for subcatch_id, coords in polygons.items():
        poly_ids.append(subcatch_id)
        geometries.append(Polygon(coords))

    gdf = gpd.GeoDataFrame({'subcatchment': poly_ids, 'geometry': geometries}, crs='EPSG:32618')
    return gdf


def plot_subcatchment_metric(gdf_polygons, df_stats, metric, cmap="Blues"):
    gdf_plot = gdf_polygons.merge(df_stats, on='subcatchment', how='left')

    ax = gdf_plot.plot(column=metric, cmap=cmap, legend=True, edgecolor='black')
    plt.title(f"Subcatchment {metric.replace('_', ' ').title()}")
    plt.axis('off')

    for idx, row in gdf_plot.iterrows():
        centroid = row.geometry.centroid
        plt.text(centroid.x, centroid.y, row['subcatchment'], fontsize=7, ha='center')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Select the scenario you want to plot
    scenario_name = 'Base'
    inp_path = scenarios[scenario_name]

    results_dir = '/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/subcatchments/'

    gdf_polygons = parse_inp_polygons(inp_path)

    stats_csv_path = f"{results_dir}6_27_2023_simV22_stats.csv"
    df_stats_all = pd.read_csv(stats_csv_path)
    df_stats = df_stats_all[df_stats_all['scenario'] == scenario_name]

    metric_to_plot = 'total_runoff'  # change as needed

    plot_subcatchment_metric(gdf_polygons, df_stats, metric=metric_to_plot, cmap='YlOrRd')



