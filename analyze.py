import pandas as pd
import os

def analyze_stats(file_path, num_songs):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    df = pd.read_csv(file_path)
    print("Statistics Summary:")
    print(df.describe())

    # Divide total energy by number of songs to get energy per song.
    df['Energy per Song (Wh)'] = df['Total Energy (Wh)'] / num_songs

    # Calculate energy and cost for 1 million songs in kWh.
    df['Energy for 1M Songs (MWh)'] = df['Energy per Song (Wh)'] * 1_000_000 / 1_000_000
    # Calculate cost by converting kWh to MWh and multiplying by price
    df['Cost for 1M Songs (EUR)'] = (df['Energy for 1M Songs (MWh)'] * 87.8)

    # Calculate cost for 400 songs.
    df['Cost for 400 Songs (EUR)'] = (df['Energy per Song (Wh)'] * 400 / 1_000_000 * 87.8).round(2)

    # Calculate time per song and time for 1 million songs
    df['Time per Song (h)'] = df['Total Duration (h)'] / num_songs
    df['Time for 1M Songs (h)'] = df['Time per Song (h)'] * 1_000_000

    output_file_path = os.path.join(os.path.dirname(file_path), "updated_stats.csv")
    df.to_csv(output_file_path, index=False)
    print(f"Updated statistics saved to {output_file_path}")

    max_avg_power_model = df.loc[df['Avg Power (W)'].idxmax()]['Model']
    print(f"Model with the highest average power: {max_avg_power_model}")

if __name__ == '__main__':
    stats_file_path = "./output/stats.csv"
    num_songs = 400
    analyze_stats(stats_file_path, num_songs)
