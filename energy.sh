#!/bin/bash
LOGFILE="power_log.csv"

echo "Timestamp,Power (W)" > "$LOGFILE"

INTERVAL=5

echo "Logging power usage every $INTERVAL seconds. Press Ctrl+C to stop."

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # Sum all initial energy values from all sensors
    T0_total=$(sudo cat /sys/class/powercap/*/energy_uj | awk '{sum+=$1} END {print sum}')
    
    # Wait for the defined interval
    sleep $INTERVAL

    # Sum all energy values after the interval
    T1_total=$(sudo cat /sys/class/powercap/*/energy_uj | awk '{sum+=$1} END {print sum}')
    
    # Calculate the total energy difference
    diff=$(( T1_total - T0_total ))
    
    # Convert energy difference (microjoules) to power (Watts)
    # Using awk to perform floating-point arithmetic
    power=$(awk -v diff="$diff" -v interval="$INTERVAL" 'BEGIN { printf "%.1f", diff/interval/1000000 }')
    
    # Append the timestamp and consolidated power reading to the log file
    echo "$TIMESTAMP,$power" >> "$LOGFILE"
done

