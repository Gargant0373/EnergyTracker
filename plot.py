import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

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

def main(start_date, end_date, desired_group_interval_seconds=None, model="model"):
    # Load and filter the data
    df = pd.read_csv("./data/logs2.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    mask = (df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)
    df_filtered = df.loc[mask].copy()
    if df_filtered.empty:
        print("No data found in the given date range.")
        return

    # Determine total duration and the grouping interval
    total_seconds = (df_filtered['Timestamp'].max() - df_filtered['Timestamp'].min()).total_seconds()
    if desired_group_interval_seconds is None:
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
    total_duration = total_seconds / 3600  # Convert total duration to hours

    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)
    stats_df = pd.DataFrame({
        "Model": [model],
        "Avg Power (W)": [avg_power],
        "Min Power (W)": [min_power],
        "Max Power (W)": [max_power],
        "Total Energy (Wh)": [total_energy_wh],
        "Total Duration (h)": [total_duration]
    })
    stats_df.to_csv(os.path.join(output_folder, f"stats_{model}.csv"), index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped.index, df_grouped['Power (W)'], marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Average Power (W)')
    plt.title('Power Usage ' + model)
    plt.xticks(rotation=45)
    textstr = (f'Avg: {avg_power:.2f} W\n'
               f'Min: {min_power:.2f} W\n'
               f'Max: {max_power:.2f} W\n'
               f'Energy: {total_energy_wh:.2f} Wh\n'
               f'Duration: {total_duration:.2f} h')
    plt.gcf().text(0.15, 0.75, textstr, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_folder, f"plot_{model}.png"))
    
    plt.show()
    

if __name__ == '__main__':
    start_date = pd.to_datetime("2025-03-14 22:43:51")
    end_date = pd.to_datetime("2025-03-15 11:20:13")
    model = "Phi"
    desired_group_interval_seconds = 600

    main(start_date, end_date, desired_group_interval_seconds, model)
