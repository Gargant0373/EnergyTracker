#!/usr/bin/env python3
import os
import subprocess
import time
from datetime import datetime
import glob

# Create a data folder if it doesn't exist
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Determine the next available index for the log file
existing_logs = glob.glob(os.path.join(DATA_DIR, "gpu_power_log_*.csv"))
indices = []
for log in existing_logs:
    # Filename pattern: gpu_power_log_{index}.csv
    basename = os.path.basename(log)
    try:
        index = int(basename.split('_')[2].split('.')[0])
        indices.append(index)
    except (IndexError, ValueError):
        continue
next_index = max(indices) + 1 if indices else 1

LOGFILE = os.path.join(DATA_DIR, f"gpu_power_log_{next_index}.csv")
INTERVAL = 10  # seconds

def get_gpu_power():
    """Retrieve the power draw (in Watts) for all GPUs using nvidia-smi and return the total."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=power.draw", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        lines = result.stdout.strip().splitlines()
        powers = [float(line.strip()) for line in lines if line.strip()]
        total_power = sum(powers)
        return total_power
    except Exception as e:
        print(f"Error retrieving GPU power: {e}")
        return None

def main():
    with open(LOGFILE, "w") as f:
        f.write("Timestamp,Power (W)\n")
    
    print(f"Logging GPU power consumption every {INTERVAL} seconds to {LOGFILE}. Press Ctrl+C to stop.")
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            power = get_gpu_power()
            if power is not None:
                log_line = f"{timestamp},{power:.1f}\n"
                with open(LOGFILE, "a") as f:
                    f.write(log_line)
                print(log_line.strip())
            else:
                print(f"{timestamp}: Error reading power consumption.")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nLogging stopped.")

if __name__ == "__main__":
    main()
