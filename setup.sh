#!/bin/bash
# TMS Planner Setup Script

echo "Setting up TMS Planner..."

# Create necessary directories
mkdir -p data
mkdir -p examples

# Install required Python packages
echo "Installing required Python packages..."
pip3 install pandas numpy matplotlib seaborn plotly kaleido || {
    echo "Error installing packages with pip3. Trying with pip..."
    pip install pandas numpy matplotlib seaborn plotly kaleido || {
        echo "Failed to install packages. Please make sure pip is installed and try again."
        exit 1
    }
}

# Make scripts executable
echo "Making scripts executable..."
chmod +x src/tms_planner.py
chmod +x src/plotly_viz.py
chmod +x src/save_calendar.py
chmod +x src/generate_all_examples.sh

# Check for data file
if [ ! -f "data/TMS2025AI_Excel_02-21-2025.xlsx" ]; then
    echo "Data file not found in data directory."
    echo "Please place the TMS2025AI_Excel_02-21-2025.xlsx file in the data directory."
fi

echo "Setup complete!"
echo "To get started, try: python3 src/tms_planner.py --list-profiles"
echo "For more examples, see: examples/example_usage.md" 