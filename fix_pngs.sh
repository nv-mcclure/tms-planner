#!/bin/bash
# Script to regenerate PNG files for TMS Planner visualizations
# with improved layout and higher resolution

echo "Regenerating PNG files for all profiles with improved layout..."

# Make sure kaleido is installed
pip3 install -U kaleido

# Create examples directory if it doesn't exist
mkdir -p examples

# Define profiles and minimum score
profiles=("battery" "ml" "am" "quantum" "corrosion")
min_score=5

# Process all profiles
for profile in "${profiles[@]}"; do
    echo -e "\n=== Regenerating PNG for ${profile} profile ==="
    # Standard view
    python3 src/plotly_viz.py --profile $profile --min-score $min_score --output examples/${profile}_calendar.html --export-png
    # Symposium view
    python3 src/plotly_viz.py --profile $profile --min-score $min_score --symposium-view --output examples/${profile}_calendar_symposium.html --export-png
done

# Process NVIDIA profile separately as it uses a custom interests file
echo -e "\n=== Regenerating PNG for nvidia profile ==="
# Standard view
python3 src/plotly_viz.py --interests nvidia_profile.json --min-score $min_score --output examples/nvidia_calendar.html --export-png
# Symposium view
python3 src/plotly_viz.py --interests nvidia_profile.json --min-score $min_score --symposium-view --output examples/nvidia_calendar_symposium.html --export-png

echo -e "\nAll PNG files have been regenerated with improved layout and larger fonts."
echo "Check the examples directory for the new PNG files."
ls -la examples/*_calendar.png 