# By: Ava Spangler
# Date:
# Description: This code does ...

# IMPORTS --------------------------------------------------------------------------------------------------------------
import pandas as pd

# EXECUTION ------------------------------------------------------------------------------------------------------------
# rainfall data--------------------------------------------------------------------------------------------------------
rain_df = pd.read_excel('/Users/aas6791/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/05 - Research/01 - BSEC Project/Validation/2023June27.xlsx')

# combine date and time, convert to datetime
rain_df['dt'] = pd.to_datetime(rain_df['date'].astype(str) + ' ' + rain_df['time'].astype(str))

# rainfall (inches *2.54 for plotting in cm)
rain_df['rain_cm'] = rain_df['rain_inches'] * 2.54

# SAVE AND EXPORT ------------------------------------------------------------------------------------------------------
rain_df.to_csv('/Users/aas6791/PycharmProject/InnerHarborSWMM_experiment/processed/6_27_23_rain_df.csv', index=False)
