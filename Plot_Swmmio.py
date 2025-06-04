import pyswmm
import pandas as pd
import networkx as nx
import swmmio
import warnings
from IPython.display import HTML
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# access the model as a Networkx MutliDiGraph
model_path = 'https://raw.githubusercontent.com/USEPA/swmm-nrtestsuite/refs/heads/dev/public/examples/Example1.inp'
model = swmmio.Model(model_path)
G = model.network

# iterate through links
for u, v, key, data in model.network.edges(data=True, keys=True):
    # do stuff with the network
    print(u, v, key, data)
    break

# visualize the graph
# Draw the graph
pos = nx.spring_layout(G, k=30)

plt.figure(figsize=(5, 2))
nx.draw(G, node_size=10, node_color='blue', with_labels=False)
plt.show()

#
link_flows = dict()

# Run simulation PySWMM
with pyswmm.Simulation(model.inp.path) as sim:
    # get link ids
    link_ids = model.inp.conduits.index

    for step in sim:
        # store each link's flow in a dictionary
        link_flows[sim.current_time] = {
            link_id: pyswmm.Links(sim)[link_id].flow
            for link_id in link_ids
        }

pd.DataFrame(link_flows).T.plot(title='Link Flows')
plt.show()


# animate link flows
# Create a links geodataframe and join the flow data
links_gdf = model.links.geodataframe
links_gdf = links_gdf.join(pd.DataFrame(link_flows))

# create a figure and axis
fig, ax = plt.subplots()

# Function to update the plot for each frame
def update(frame):
    ax.clear()
    links_gdf.plot(linewidth=links_gdf[frame]+0.2, ax=ax, capstyle='round')
    ax.set_axis_off()
    ax.set_title(f'{frame}')

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=list(link_flows)[30:400][::5], repeat=True)
plt.show()
# Close the figure to prevent it from being displayed
#plt.close(fig)

# render the animation in the notebook
HTML(ani.to_jshtml(fps=30))
