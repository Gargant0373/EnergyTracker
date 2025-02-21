#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime

LOGFILE = "gpu_power_log.csv"
INTERVAL = 10  # seconds

def get_gpu_power():
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
    
    print(f"Logging GPU power consumption every {INTERVAL} seconds. Press Ctrl+C to stop.")
    
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

