from IPython.display import HTML
import swmmio
import pyswmm
import pandas as pd
from swmmio import Model

# path to a SWMM model
#model_path = 'https://raw.githubusercontent.com/USEPA/swmm-nrtestsuite/refs/heads/dev/public/examples/Example1.inp'
#model = swmmio.Model(model_path)
#model.summary
#print(model.summary)

#test model from swmmio
from swmmio.tests.data import MODEL_FULL_FEATURES_PATH

# instantiate a model object
model = swmmio.Model(MODEL_FULL_FEATURES_PATH)

# get the data related to links
links = model.links.dataframe

outfalls = model.inp.outfalls

#modify the dataframe
outfalls.loc['J4', 'OutfallType'] = 'FIXED'

#save
model.inp.save('SWMMIO_Example1.inp')

#new model instance
example_1 = swmmio.Model('SWMMIO_Example1.inp')
Nodes = example_1.nodes.dataframe
print(Nodes)