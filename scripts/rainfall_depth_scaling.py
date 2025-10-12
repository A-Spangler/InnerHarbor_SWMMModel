#ava Spangler
#10/10/2025

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

real_storm = pd.read_excel("/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - RainfallData/ProcessedStorms/2023June27_onepulse_x1.xlsx")
print(real_storm)

#process real storm
rain_cum_max = real_storm['cumulative_rain'].max()
rain_cum = real_storm['cumulative_rain'].to_numpy()
real_storm["time_elapsed_minutes"] = pd.to_timedelta(real_storm["time_elapsed_minutes"])
real_time_elapsed = real_storm["time_elapsed_minutes"].dt.total_seconds() / 60  # minutes
real_intensity = np.gradient(real_storm.cumulative_rain,real_time_elapsed)
peak_intensity = real_intensity.max()
average_intensity = real_intensity.mean()
print('real storm cumulative depth:', rain_cum_max,'in')
print("real storm average intensity:", average_intensity, "in/hr")
print("real storm peak intensity:", peak_intensity, "in/hr")


# interpolate cumulative distribution of half-depth storm
decrease_factor = 0.5
decr_storm = pd.DataFrame()
decr_storm['cumulative_rain'] = real_storm['cumulative_rain'] * decrease_factor
decr_storm_rain = decr_storm['cumulative_rain'].to_numpy()
decr_storm_max = decr_storm['cumulative_rain'].max()
decr_storm['decr_time'] = real_time_elapsed * decrease_factor
decr_time = decr_storm['decr_time'].to_numpy()
#calculate new intensity
decr_intensity = np.gradient(decr_storm_rain, decr_time) # gradient(y,x)
decr_average_intensity = decr_intensity.mean()
decr_peak_intensity = decr_intensity.max()
print('decreased cumulative depth:', decr_storm_max,'in')
print("decreased average intensity:", decr_average_intensity, "in/hr")
print("decreased peak intensity:", decr_peak_intensity, "in/hr")


# interpolate cumulative distribution of double-duration storm
increase_factor = 2
incr_storm = pd.DataFrame()
incr_storm['cumulative_rain'] = real_storm['cumulative_rain'] * increase_factor
incr_storm_rain = incr_storm['cumulative_rain'].to_numpy()
incr_storm_max = incr_storm['cumulative_rain'].max()
incr_storm['incr_time'] = real_time_elapsed * increase_factor
incr_time = incr_storm['incr_time'].to_numpy()
#calculate new intensity
incr_intensity = np.gradient(incr_storm_rain, incr_time) # gradient(y,x)
incr_average_intensity = incr_intensity.mean()
incr_peak_intensity = incr_intensity.max()
print('increased cumulative depth:', incr_storm_max,'in')
print("increased depth average intensity:", incr_average_intensity, "in/hr")
print("increased depth peak intensity:", incr_peak_intensity, "in/hr")

# plot
plt.plot(real_time_elapsed, rain_cum, label = '6/27/2023')
plt.plot(decr_time, decr_storm_rain, label = 'Smaller 6/27/2023')
plt.plot(incr_time, incr_storm_rain, label = 'Larger 6/27/2023')
plt.xlabel("Elapsed Time (minutes)")
plt.ylabel("Rainfall (inches)")
plt.legend()
plt.title("Cumulative Rainfall")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/incrdecr_cumulative.svg')



plt.bar(real_time_elapsed, real_intensity, label = '6/27/2023')
plt.bar(decr_time, decr_intensity, label = 'Smaller 6/27/2023')
plt.bar(incr_time, incr_intensity, label = 'Larger 6/27/2023')
plt.xlabel("Elapsed Time (minutes)")
plt.ylabel("Rainfall intensity (inches / 5 min)")
plt.legend()
plt.title("Rainfall Hyetograph")
plt.savefig('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/plots/rainfall/incrdecr_hyeto.svg')

#create dfs and save, creating HH:MM formatting for SWMM
decr_df = pd.DataFrame()
decr_df = decr_df.assign(time_elapsed_minutes=decr_time, rain_cumulatives=decr_storm_rain)
hours = (decr_df['time_elapsed_minutes'] // 60).astype(int)
minutes = (decr_df['time_elapsed_minutes'] % 60).astype(int)
decr_df['elapsed_time_HHMM'] = hours.astype(str).str.zfill(2) + ':' + minutes.astype(str).str.zfill(2)
decr_df.to_excel(("/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - RainfallData/ProcessedStorms/2023June27_onepulse_depthx0.5.xlsx"))

incr_df = pd.DataFrame()
incr_df = incr_df.assign(time_elapsed_minutes=incr_time, rain_inches=incr_storm_rain)
hours = (incr_df['time_elapsed_minutes'] // 60).astype(int)
minutes = (incr_df['time_elapsed_minutes'] % 60).astype(int)
incr_df['elapsed_time_HHMM'] = hours.astype(str).str.zfill(2) + ':' + minutes.astype(str).str.zfill(2)
incr_df.to_excel(("/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - RainfallData/ProcessedStorms/2023June27_onepulse_depthx2.xlsx"))
