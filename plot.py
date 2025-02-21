#!/usr/bin/env python3
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DATA_DIR = "data"
PLOTS_DIR = "plots"

if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

log_files = glob.glob(os.path.join(DATA_DIR, "gpu_power_log_*.csv"))

if not log_files:
    print("No log files found in the 'data' folder.")
    exit(1)

latest_log = max(log_files, key=os.path.getmtime)
print(f"Plotting data from: {latest_log}")

df = pd.read_csv(latest_log, parse_dates=["Timestamp"])

plt.figure(figsize=(12, 6))
plt.plot(df["Timestamp"], df["Power (W)"], marker='o', linestyle='-', label="GPU Power (W)")
plt.xlabel("Timestamp")
plt.ylabel("Power (W)")
plt.title("GPU Power Consumption Over Time")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

plot_filename = os.path.join(PLOTS_DIR, f"gpu_power_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

plt.savefig(plot_filename)
print(f"Plot saved to: {plot_filename}")

plt.show()
