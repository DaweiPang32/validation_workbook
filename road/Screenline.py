import pandas as pd

# Load the dataset
file_path = r"C:\Users\dpang\Desktop\trer.csv"
df = pd.read_csv(file_path)

df.dropna(subset=['Dir', 'A', 'B'], inplace=True)
df['A'] = df['A'].astype(int)
df['B'] = df['B'].astype(int)

# Define inbound and outbound directions
inbound_dirs = ['W', 'S']
outbound_dirs = ['E', 'N']

# Define screenline groups based on provided AB pairs
screenline_groups = {
    "Bay_Bridge": [(103803, 103783), (7973, 103784)],
    "San_Mateo": [(4229, 4230), (4539, 4224)],
    "Golden_Gate": [(103803, 103783), (7973, 103784)]
}

# Define time periods
time_periods = ['EA', 'AM', 'MD', 'PM', 'EV']

# Function to aggregate by time of day and screenline
def aggregate_by_time_and_screenline(df, screenline_name, ab_pairs, direction, direction_label):
    filtered_df = df[(df[['A', 'B']].apply(tuple, axis=1).isin(ab_pairs)) & (df['Dir'].isin(direction))]
    
    summary = {
        'TOD': time_periods + ['Total'],
        'Observed': [filtered_df[f'{period}_obs'].sum() for period in time_periods],
        'Modeled': [filtered_df[f'{period}_est'].sum() for period in time_periods],
    }
    summary['Diff'] = [m - o for o, m in zip(summary['Observed'], summary['Modeled'])]
    summary['Percent Diff'] = [d / o if o != 0 else None for o, d in zip(summary['Observed'], summary['Diff'])]
    
    total_observed = sum(summary['Observed'])
    total_modeled = sum(summary['Modeled'])
    total_diff = total_modeled - total_observed
    total_percent_diff = total_diff / total_observed if total_observed != 0 else None
    
    summary['Observed'].append(total_observed)
    summary['Modeled'].append(total_modeled)
    summary['Diff'].append(total_diff)
    summary['Percent Diff'].append(total_percent_diff)
    
    result_df = pd.DataFrame(summary)
    result_df.to_csv(f"{screenline_name}_{direction_label}.csv", index=False)
    result_df.drop(result_df.tail(1).index, inplace=True)  # Remove total row
    result_df.to_csv(f"{screenline_name}_{direction_label}_without_total.csv", index=False)
    
    return result_df

# Function to aggregate all screenlines together
def aggregate_all_screenlines(df, direction, direction_label):
    filtered_df = df[df['Dir'].isin(direction)]
    
    summary = {
        'TOD': time_periods + ['Total'],
        'Observed': [filtered_df[f'{period}_obs'].sum() for period in time_periods],
        'Modeled': [filtered_df[f'{period}_est'].sum() for period in time_periods],
    }
    summary['Diff'] = [m - o for o, m in zip(summary['Observed'], summary['Modeled'])]
    summary['Percent Diff'] = [d / o if o != 0 else None for o, d in zip(summary['Observed'], summary['Diff'])]
    
    total_observed = sum(summary['Observed'])
    total_modeled = sum(summary['Modeled'])
    total_diff = total_modeled - total_observed
    total_percent_diff = total_diff / total_observed if total_observed != 0 else None
    
    summary['Observed'].append(total_observed)
    summary['Modeled'].append(total_modeled)
    summary['Diff'].append(total_diff)
    summary['Percent Diff'].append(total_percent_diff)
    
    result_df = pd.DataFrame(summary)
    result_df.to_csv(f"All_Screenlines_{direction_label}.csv", index=False)
    result_df.drop(result_df.tail(1).index, inplace=True)  # Remove total row
    result_df.to_csv(f"All_Screenlines_{direction_label}_without_total.csv", index=False)
    
    return result_df

# Generate and save tables for each screenline and direction
for screenline, ab_pairs in screenline_groups.items():
    inbound_table = aggregate_by_time_and_screenline(df, screenline, ab_pairs, inbound_dirs, "inbound")
    outbound_table = aggregate_by_time_and_screenline(df, screenline, ab_pairs, outbound_dirs, "outbound")

# Generate and save aggregated tables for all screenlines
all_screenlines_inbound = aggregate_all_screenlines(df, inbound_dirs, "inbound")
all_screenlines_outbound = aggregate_all_screenlines(df, outbound_dirs, "outbound")
