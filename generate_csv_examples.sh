#!/bin/bash

# Script to generate CSV files and symposium reports for TMS Planner examples

echo "Generating CSV files and symposium reports for all profiles..."

# Create examples directories if they don't exist
mkdir -p examples

# Define profiles and minimum score
profiles=("battery" "ml" "am" "quantum" "corrosion")
min_score=5

# Process all profiles
for profile in "${profiles[@]}"; do
    echo -e "\n=== Generating reports for ${profile} profile ==="
    # Generate CSV and symposium report
    python3 src/plotly_viz.py --profile $profile --min-score $min_score --csv --symposium --output examples/${profile}_calendar.html
    # Move files to examples directory
    mv ${profile}_sessions.csv examples/${profile}_sessions.csv
    mv ${profile}_symposiums.txt examples/${profile}_symposiums.txt
done

# Process NVIDIA profile separately as it uses a custom interests file
echo -e "\n=== Generating reports for nvidia profile ==="
python3 src/plotly_viz.py --interests nvidia_profile.json --min-score $min_score --csv --symposium --output examples/nvidia_calendar.html
mv nvidia_profile_sessions.csv examples/nvidia_profile_sessions.csv
mv nvidia_profile_symposiums.txt examples/nvidia_profile_symposiums.txt

echo -e "\nAll CSV files and symposium reports have been generated."
echo "Check the examples directory for the new files:"
ls -la examples/*_sessions.csv examples/*_symposiums.txt 