import pandas as pd

combined_df = pd.read_csv('6_27_2023_simV19.csv')
combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])

#duration over threshold
# pull out time above 6 inch (=.1524m) threshold using a filter
threshold=.1524 #meters
duration_above_threshold = []

for scenario in scenarios.keys():
    df_thresh = combined_df.loc[scenario]
    df_thresh = df_thresh.sort_values('timestamp').reset_index(drop=True)
    df_thresh['above_threshold'] = df_thresh['J338-S_depth'] > threshold
    # check if value in ['above threshold'] is not equal to previous, sum
    df_thresh['group'] = (df_thresh['above_threshold'] != df_thresh['above_threshold'].shift()).cumsum()
    # filter for only above-threshold groups
    above_df = df_thresh[df_thresh['above_threshold']]
    # group by segment and get start and end times
    above_df = above_df.groupby('group').agg(start=('timestamp', 'first'),
                                             end=('timestamp', 'last'))
    # compute duration
    above_df['duration_periods'] = above_df['end'] - above_df['start']
    above_df['total_duration'] = above_df['duration_periods'].sum()

print(above_df.head())
