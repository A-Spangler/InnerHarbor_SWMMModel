import pyswmm
import pandas as pd
import networkx
import swmmio
import matplotlib

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
import matplotlib.pyplot as plt
import networkx as nx
# Draw the graph
pos = nx.spring_layout(G, k=30)

plt.figure(figsize=(5, 2))
nx.draw(G, node_size=10, node_color='blue', with_labels=False)
plt.show()