import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/pandas-dev/pandas/main/pandas/tests/io/data/csv/iris.csv')
print (df.head())
pd.plotting.parallel_coordinates(df, 'Name', color=('#556270', '#4ECDC4', '#C7F464'))
plt.show()