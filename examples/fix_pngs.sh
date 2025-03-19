#!/bin/bash
# Script to regenerate all PNG files in the examples directory

echo "Regenerating PNG files for all profiles..."

# Ensure kaleido is installed
pip3 install -U kaleido || {
    echo "Error: Failed to install kaleido. PNG export requires kaleido."
    exit 1
}

# Create examples directory if it doesn't exist
mkdir -p examples

# Define profiles 
profiles=("battery" "ml" "am" "quantum" "corrosion" "nvidia")

# Process profiles
for profile in "${profiles[@]}"
do
    echo
    echo "=== Regenerating PNG for ${profile} profile ==="
    
    if [[ "$profile" == "nvidia" ]]; then
        # Use interests file for NVIDIA
        python3 src/plotly_viz.py --interests ${profile}_profile.json --min-score 5 \
            --output examples/${profile}_calendar.html --export-png
    else
        # Use predefined profile
        python3 src/plotly_viz.py --profile ${profile} --min-score 5 \
            --output examples/${profile}_calendar.html --export-png
    fi
    
    # Also generate symposium view PNG
    if [[ "$profile" == "nvidia" ]]; then
        python3 src/plotly_viz.py --interests ${profile}_profile.json --min-score 5 \
            --output examples/${profile}_calendar_symposium.html --symposium-view --export-png
    else
        python3 src/plotly_viz.py --profile ${profile} --min-score 5 \
            --output examples/${profile}_calendar_symposium.html --symposium-view --export-png
    fi
done

echo
echo "All PNG files have been regenerated."
echo "Check the examples directory for the new PNG files."
ls -la examples/*.png 