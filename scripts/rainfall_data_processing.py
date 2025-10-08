# By: Ava Spangler
# Date:
# Description: This code does ...

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# EXECUTION ------------------------------------------------------------------------------------------------------------
# rainfall data--------------------------------------------------------------------------------------------------------
rain_df = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - RainfallData/ProcessedStorms/2023June27_formatted.xlsx')
scs2_df = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - '
                              'RainfallData/ProcessedStorms/SCS2_2.96in_24hour.xlsx')
scs1a_df = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - '
                              'RainfallData/ProcessedStorms/SCS1A_2.96in_24hour.xlsx')
#scs1_df = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - '
                              #'RainfallData/ProcessedStorms/SCS1_2.96in_12hour.xlsx')

#find intensity of the real storm using np.gradient
#convert minutes to hours
real_elapsed = rain_df.time_elapsed_minutes/60
real_intensity = np.gradient(rain_df.cumulative_rain,real_elapsed)
peak_intensity = real_intensity.max()
average_intensity = real_intensity.mean()
#cum_depth = rain_df.rain_inches.sum()
#print("real storm cumulative depth:", cum_depth)
print("real storm average intensity:", average_intensity, "in/hr")
print("real storm peak intensity:", peak_intensity, "in/hr")


#Find intensity of SCS storms
# convert to elapsed datetime
scs2_df.time = pd.to_timedelta(scs2_df['time'].astype(str))
scs2_df['time_no_days'] = scs2_df['time'] - pd.to_timedelta(scs2_df['time'].dt.days, unit='d')
scs2_df['elapsed_hours'] = scs2_df['time_no_days'].dt.total_seconds() / 3600
scs2_elapsed = scs2_df['elapsed_hours']
scs2_intensity = np.gradient(scs2_df['cum_rain_inches'],scs2_elapsed)
scs2_peak_intensity = scs2_intensity.max()
scs2_avg_intensity = scs2_intensity.mean()
print("SCS 2 average intensity:", scs2_avg_intensity, "in/hr")
print("SCS 2 peak intensity:", scs2_peak_intensity, "in/hr")

'''
scs1_df.time = pd.to_timedelta(scs1_df['time'].astype(str))
scs1_df['time_no_days'] = scs1_df['time'] - pd.to_timedelta(scs1_df['time'].dt.days, unit='d')
scs1_df['elapsed_hours'] = scs1_df['time_no_days'].dt.total_seconds() / 3600
scs1_elapsed = scs1_df['elapsed_hours']
scs1_intensity = np.gradient(scs1_df['cum_rain_inches'],scs1_elapsed)
scs1_peak_intensity = scs1_intensity.max()
scs1_avg_intensity = scs1_intensity.mean()
print("SCS 1 average intensity:", scs1_avg_intensity, "in/hr")
print("SCS 1 peak intensity:", scs1_peak_intensity, "in/hr")
'''

scs1a_df.time = pd.to_timedelta(scs1a_df['time'].astype(str))
scs1a_df['time_no_days'] = scs1a_df['time'] - pd.to_timedelta(scs1a_df['time'].dt.days, unit='d')
scs1a_df['elapsed_hours'] = scs1a_df['time_no_days'].dt.total_seconds() / 3600
scs1a_elapsed = scs1a_df['elapsed_hours']
scs1a_intensity = np.gradient(scs1a_df['cum_rain_inches'],scs1a_elapsed)
scs1a_peak_intensity = scs1a_intensity.max()
scs1a_avg_intensity = scs1a_intensity.mean()
print("SCS 1A average intensity:", scs1a_avg_intensity, "in/hr")
print("SCS 1A peak intensity:", scs1a_peak_intensity, "in/hr")

#plot
plt.plot(scs2_elapsed, scs2_df.cum_rain_inches, label = "scs2")
plt.ylabel("Cumulative depth (inches)")
plt.xlabel("Elapsed time (hours)")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/SCS2_24cum.svg')
plt.close()

#plt.plot(scs1_elapsed, scs1_df.cum_rain_inches, label = "scs1")
plt.plot(scs1a_elapsed, scs1a_df.cum_rain_inches, label = "scs1A")
plt.ylabel("Cumulative depth (inches)")
plt.xlabel("Elapsed time (hours)")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/SCS1A_24cum.svg')
plt.close()

plt.plot(real_elapsed, rain_df.cumulative_rain, label = "1/9/2024 storm")
plt.ylabel("Cumulative depth (inches)")
plt.xlabel("Elapsed time (hours)")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/6_27_2023_cum.svg')
plt.close()


plt.plot(scs2_elapsed, scs2_intensity, label = "scs2")
plt.ylabel("Cumulative depth (inches)")
plt.xlabel("Elapsed time (hours)")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/SCS2_24hyeto.svg')
plt.close()

plt.plot(scs1a_elapsed, scs1a_intensity, label = "scs1")
plt.ylabel("Cumulative depth (inches)")
plt.xlabel("Elapsed time (hours)")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/SCS1a_24hyeto.svg')
plt.close()

#plt.plot(scs1_elapsed, scs1_intensity, label = "scs1A")
plt.plot(real_elapsed, real_intensity, label = "1/9/2024 storm")
plt.ylabel("Cumulative depth (inches)")
plt.xlabel("Elapsed time (hours)")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/6_27_2023_hyeto.svg')
plt.close()


# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------

