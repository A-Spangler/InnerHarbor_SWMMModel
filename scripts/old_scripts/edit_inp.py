from IPython.display import HTML
import swmmio
import pyswmm
import pandas as pd
from swmmio import Model

# path to my SWMM model
model_path = '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.inp'

#test model
#model_path = 'https://raw.githubusercontent.com/USEPA/swmm-nrtestsuite/refs/heads/dev/public/examples/Example1.inp'
model = swmmio.Model(model_path)
model.summary
#print(model.summary)


# get the data related to links
nodes_df = model.nodes.dataframe
#nodes_df.columns = nodes_df.columns.str.strip()
nodes_df = nodes_df.reset_index()
node_names = nodes_df['Name'].tolist()
street_node_names = [k for k in node_names if '-S' in k]
print(street_node_names)

#model.inp.outfalls

#modify the dataframe
#model.inp.outfalls.loc['J4', 'OutfallType'] = 'FIXED'

#save
#model.inp.save('SWMMIO_Example1.inp')

#new model instance
#example_1 = swmmio.Model('../SWMMIO_Example1.inp')
#Nodes = example_1.nodes.dataframe
#print(Nodes)


