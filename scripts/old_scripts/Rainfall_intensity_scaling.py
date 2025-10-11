#ava Spangler
#10/10/2025

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

real_storm = pd.read_excel("/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - RainfallData/ProcessedStorms/2023June27_onepulse_x1.xlsx")
print(real_storm)

#process real storm
rain_cum = real_storm['cumulative_rain'].to_numpy()
rain_cum_max = rain_cum.max()
real_storm["time_elapsed_minutes"] = pd.to_timedelta(real_storm["time_elapsed_minutes"])
real_time_elapsed = real_storm["time_elapsed_minutes"].dt.total_seconds() / 60  # minutes
real_time_elapsed = real_time_elapsed.to_numpy()
real_intensity = np.gradient(real_storm.cumulative_rain,real_time_elapsed)
peak_intensity = real_intensity.max()
average_intensity = real_intensity.mean()
print('real storm cumulative depth:', rain_cum_max,'in')
print("real storm average intensity:", average_intensity, "in/hr")
print("real storm peak intensity:", peak_intensity, "in/hr")


# interpolate cumulative distribution of half-duration storm
halving = 0.5
rain_cum = real_storm['cumulative_rain'].to_numpy()
x_halftime = np.linspace(0, real_time_elapsed[-1] * halving, int(len(real_time_elapsed)))
y_halftime_interp = np.interp(x_halftime / halving, real_time_elapsed, rain_cum) # interpolates rain by new time series
halftime_cum_max = y_halftime_interp.max()
halftime_intensity = np.gradient(y_halftime_interp,x_halftime) # finds gradient of new rain/time series
halftime_peak_intensity = halftime_intensity.max()
halftime_average_intensity = halftime_intensity.mean()
print('half duration cumulative depth:', halftime_cum_max,'in')
print("half duration average intensity:", halftime_average_intensity, "in/hr")
print("half duration peak intensity:", halftime_peak_intensity, "in/hr")

# interpolate cumulative distribution of double-duration storm
doubling = 2
rain_cum = real_storm['cumulative_rain'].to_numpy()
x_doubletime = np.linspace(0, real_time_elapsed[-1] * doubling, int(len(real_time_elapsed)))
y_doubletime_interp = np.interp(x_doubletime / doubling, real_time_elapsed, rain_cum)
doubletime_cum_max = y_doubletime_interp.max()
doubletime_intensity = np.gradient(y_doubletime_interp,x_doubletime)
doubletime_peak_intensity = doubletime_intensity.max()
doubletime_average_intensity = doubletime_intensity.mean()
print('doubleduration cumulative depth:', doubletime_cum_max,'in')
print("double duration average intensity:", doubletime_average_intensity, "in/hr")
print("double duration peak intensity:", doubletime_peak_intensity, "in/hr")


# plot
plt.plot(real_time_elapsed, rain_cum, label = '6/27/2023')
plt.plot(x_halftime, y_halftime_interp, label = 'More Intense 6/27/2023')
plt.plot(x_doubletime, y_doubletime_interp, label = 'Less Intense 6/27/2023')
plt.xlabel("Elapsed Time (minutes)")
plt.ylabel("Rainfall (inches)")
plt.legend()
plt.title("Cumulative Rainfall") 
plt.show()

plt.bar(real_time_elapsed, real_intensity, label = '6/27/2023')
plt.bar(x_halftime, halftime_intensity, label = 'More Intense 6/27/2023')
plt.bar(x_doubletime, doubletime_intensity, label = 'Less Intense 6/27/2023')
plt.xlabel("Elapsed Time (minutes)")
plt.ylabel("Rainfall intensity (inches / 5 min)")
plt.legend()
plt.title("Rainfall Hyetograph")
plt.show()

#create dfs and save, creating HH:MM formatting for SWMM
halftime_df = pd.DataFrame()
halftime_df = halftime_df.assign(time_elapsed_minutes=x_halftime, rain_cumulatives=y_halftime_interp)
hours = (halftime_df['time_elapsed_minutes'] // 60).astype(int)
minutes = (halftime_df['time_elapsed_minutes'] % 60).astype(int)
halftime_df['elapsed_time_HHMM'] = hours.astype(str).str.zfill(2) + ':' + minutes.astype(str).str.zfill(2)
halftime_df.to_excel(("/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - RainfallData/ProcessedStorms/2023June27_onepulse_x0.4time.xlsx"))

doubletime_df = pd.DataFrame()
doubletime_df = doubletime_df.assign(time_elapsed_minutes=x_doubletime, rain_inches=y_halftime_interp)
hours = (doubletime_df['time_elapsed_minutes'] // 60).astype(int)
minutes = (doubletime_df['time_elapsed_minutes'] % 60).astype(int)
doubletime_df['elapsed_time_HHMM'] = hours.astype(str).str.zfill(2) + ':' + minutes.astype(str).str.zfill(2)
doubletime_df.to_excel(("/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/04 - RainfallData/ProcessedStorms/2023June27_onepulse_x2.5time.xlsx"))
