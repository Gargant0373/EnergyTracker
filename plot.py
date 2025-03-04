import datetime
import pandas as pd
import matplotlib.pyplot as plt

def get_date_from_input(prompt_label="start"):
    now = datetime.datetime.now()
    default_dt = now - datetime.timedelta(days=3) if prompt_label == "start" else now
    year = input(f"Enter {prompt_label} year (default {default_dt.year}): ").strip() or str(default_dt.year)
    month = input(f"Enter {prompt_label} month (default {default_dt.month}): ").strip() or str(default_dt.month)
    day = input(f"Enter {prompt_label} day (default {default_dt.day}): ").strip() or str(default_dt.day)
    hour = input(f"Enter {prompt_label} hour (default {default_dt.hour}): ").strip() or str(default_dt.hour)
    minute = input(f"Enter {prompt_label} minute (default {default_dt.minute}): ").strip() or str(default_dt.minute)
    second = input(f"Enter {prompt_label} second (default {default_dt.second}): ").strip() or str(default_dt.second)
    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)} {hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}"
    try:
        dt = pd.to_datetime(date_str, format="%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        exit(1)
    return dt

def main(start_date, end_date, desired_group_interval_seconds=None):
    # Load and filter the data
    df = pd.read_csv("./data/gpu_power_log_1.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    mask = (df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)
    df_filtered = df.loc[mask].copy()
    if df_filtered.empty:
        print("No data found in the given date range.")
        return

    # Determine total duration and the grouping interval
    total_seconds = (df_filtered['Timestamp'].max() - df_filtered['Timestamp'].min()).total_seconds()
    if desired_group_interval_seconds is None:
        # Default to 5 minutes (300 seconds) if duration is less than a day;
        # otherwise, compute a dynamic interval aiming for ~200 groups
        if total_seconds < 24 * 3600:
            group_duration_seconds = 300
        else:
            group_duration_seconds = total_seconds / 200
    else:
        group_duration_seconds = desired_group_interval_seconds

    group_interval = pd.Timedelta(seconds=group_duration_seconds)

    # Sort by Timestamp and set it as index for resampling
    df_filtered = df_filtered.sort_values('Timestamp').set_index('Timestamp')

    # Calculate the time differences between measurements (in seconds)
    # and compute energy consumption per measurement in Joules.
    df_filtered['TimeDelta'] = df_filtered.index.to_series().diff().dt.total_seconds().fillna(0)
    df_filtered['Energy_J'] = df_filtered['Power (W)'] * df_filtered['TimeDelta']

    # Resample the data over the dynamic grouping interval:
    # - Average the power values for the group.
    # - Sum the energy consumption (Joules) for the group.
    df_grouped = df_filtered.resample(group_interval).agg({
        'Power (W)': 'mean',
        'Energy_J': 'sum'
    })
    # Convert energy from Joules to Watt-hours (1 Wh = 3600 J)
    df_grouped['Energy_Wh'] = df_grouped['Energy_J'] / 3600

    # Compute overall statistics from the grouped data for display.
    avg_power = df_grouped['Power (W)'].mean()
    min_power = df_grouped['Power (W)'].min()
    max_power = df_grouped['Power (W)'].max()
    total_energy_wh = df_grouped['Energy_Wh'].sum()

    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped.index, df_grouped['Power (W)'], marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Average Power (W)')
    plt.title('Power Usage (Grouped)')
    plt.xticks(rotation=45)
    textstr = (f'Avg: {avg_power:.2f} W\n'
               f'Min: {min_power:.2f} W\n'
               f'Max: {max_power:.2f} W\n'
               f'Energy: {total_energy_wh:.2f} Wh')
    plt.gcf().text(0.15, 0.75, textstr, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    plt.tight_layout()
    
    plt.savefig("./plots/plot.png")
    
    plt.show()
    

if __name__ == '__main__':
    print("Enter start date and time:")
    start_date = get_date_from_input("start")
    print("\nEnter end date and time:")
    end_date = get_date_from_input("end")
    group_input = input("Enter grouping interval in minutes (default dynamic, 5 minutes if duration < 1 day): ").strip()
    if group_input:
        desired_group_interval_seconds = int(float(group_input) * 60)
    else:
        desired_group_interval_seconds = None

    main(start_date, end_date, desired_group_interval_seconds)
