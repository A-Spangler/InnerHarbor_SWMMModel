import pyswmm
import pandas as pd
import networkx as nx
import swmmio
from IPython.display import HTML
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#first clear any unicode errors up
#UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb3 in position 5166: invalid start byte
input_file = '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/Inner_Harbor_Model_V19.inp'
output_file = '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/V19_cleaned_report.inp'

# Read binary content
with open(input_file, 'rb') as f:
    content = f.read()

# Replace problematic characters
clean_content = content.replace(b'\xb3', b'3')  # Replace superscript 3 with regular 3

# Write cleaned content
with open(output_file, 'wb') as f:
    f.write(clean_content)



# open model
model_path = '/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/SWMM models copy/V19_cleaned_report.inp'
#TEST model_path = 'https://raw.githubusercontent.com/USEPA/swmm-nrtestsuite/refs/heads/dev/public/examples/Example1.inp'
model = swmmio.Model(model_path)
G = swmmio.Model.network



# do stuff
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