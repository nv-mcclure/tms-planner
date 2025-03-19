#!/usr/bin/env python3
"""
Check for time issues in the TMS dataset
"""

import pandas as pd
from datetime import datetime, timedelta

# Load the data
df = pd.read_excel('data/TMS2025AI_Excel_02-21-2025.xlsx')

# Function to convert time string to datetime
def time_to_datetime(time_str):
    try:
        if isinstance(time_str, str):
            # Try standard format
            return datetime.strptime(time_str, '%H:%M:%S')
        elif hasattr(time_str, 'hour') and hasattr(time_str, 'minute'):
            return datetime(1900, 1, 1, time_str.hour, time_str.minute, 0)
        else:
            return None
    except Exception as e:
        print(f"Error parsing time {time_str}: {e}")
        return None

# Find extremely short sessions (less than 15 minutes)
short_sessions = []
for i in range(len(df)):
    # Parse times
    start_time = time_to_datetime(df.iloc[i].Start)
    end_time = time_to_datetime(df.iloc[i].End)
    
    if start_time and end_time:
        # Calculate duration
        duration = end_time - start_time
        
        # Check if duration is negative or very short
        if duration.total_seconds() < 900:  # Less than 15 minutes (900 seconds)
            short_sessions.append((i, duration))

# Report the issues
print(f"Found {len(short_sessions)} sessions shorter than 15 minutes out of {len(df)} sessions:")
print()

# Sort by duration
short_sessions.sort(key=lambda x: x[1])

# Show the shortest sessions
for i in range(min(20, len(short_sessions))):
    row_idx, duration = short_sessions[i]
    print(f"Row {row_idx}: Start={df.iloc[row_idx].Start}, End={df.iloc[row_idx].End}")
    print(f"Duration: {duration}")
    print(f"Title: {df.iloc[row_idx].Title}")
    print(f"Room: {df.iloc[row_idx].Location}")
    print(f"Symposium: {df.iloc[row_idx].Symposium}")
    print("-" * 80) 