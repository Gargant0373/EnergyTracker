# GPU Power Logger

This project provides a Python script that logs your NVIDIA GPU power consumption by invoking the `nvidia-smi` command. It aggregates power usage across all available GPUs and logs the total power draw every 10 seconds.

## Features

- **Automated Logging:** Records GPU power consumption every 10 seconds.
- **Aggregated Data:** Sums power draw from all detected NVIDIA GPUs.
- **Indexed Log Files:** Creates a `data` folder and indexes each log file (e.g., `gpu_power_log_1.csv`, `gpu_power_log_2.csv`).
- **CSV Output:** Logs are saved in CSV format with timestamps and power values.
- **Plotting:** Generates plots of power usage over time.
- **Analysis:** Analyzes energy consumption statistics.

## Prerequisites

- **Python:** Version 3.6 or later.
- **NVIDIA GPU:** With `nvidia-smi` installed (typically included with NVIDIA drivers).

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Gargant0373/EnergyTracker
   cd EnergyTracker
   ```

2. **Run the project**

   ```bash
   python energy.py
   ```

   Consider running it in a screen for background usage:
   ```bash
   screen -R energy
   ENTER
   python energy.py
   CTRL + A + D
   ```

## Plotting

To generate plots of the logged GPU power consumption data, use the `plot.py` script. You can specify the start and end dates for the data to be plotted, as well as the model name and the desired grouping interval in seconds.

Example usage:

```bash
python plot.py
```

## Analysis

To analyze the energy consumption statistics, use the `analyze.py` script. You can specify the path to the statistics file and the number of songs to calculate energy per song and related metrics.

Example usage:

```bash
python analyze.py
```