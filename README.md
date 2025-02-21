# GPU Power Logger

This project provides a Python script that logs your NVIDIA GPU power consumption by invoking the `nvidia-smi` command. It aggregates power usage across all available GPUs and logs the total power draw every 10 seconds.

## Features

- **Automated Logging:** Records GPU power consumption every 10 seconds.
- **Aggregated Data:** Sums power draw from all detected NVIDIA GPUs.
- **Indexed Log Files:** Creates a `data` folder and indexes each log file (e.g., `gpu_power_log_1.csv`, `gpu_power_log_2.csv`).
- **CSV Output:** Logs are saved in CSV format with timestamps and power values.

## Prerequisites

- **Python:** Version 3.6 or later.
- **NVIDIA GPU:** With `nvidia-smi` installed (typically included with NVIDIA drivers).

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
