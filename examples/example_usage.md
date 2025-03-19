# TMS Planner Usage Examples

This document provides examples of how to use the TMS Planner for various tasks.

## Example Visualizations by Profile

The examples directory is organized by research profile with the following structure:

- `/battery` - Battery materials research
- `/ml` - Machine learning and AI
- `/am` - Additive manufacturing
- `/quantum` - Quantum computing and DFT
- `/corrosion` - Corrosion science
- `/nvidia` - NVIDIA-related research (custom profile)

Each profile directory contains:
- Interactive HTML visualizations (standard and symposium views)
- Static PNG visualizations for inclusion in documents
- CSV exports of relevant sessions
- Symposium recommendation reports

## Basic Usage

List available research profiles:
```bash
python3 src/tms_planner.py --list-profiles
```

Generate a schedule using a pre-defined profile:
```bash
python3 src/tms_planner.py --profile battery
```

Use a custom interests file:
```bash
python3 src/tms_planner.py --interests nvidia_profile.json
```

## Creating Custom Interest Profiles

Create a custom interests template:
```bash
python3 src/tms_planner.py --template my_template.json --profile battery
```

This generates a template based on the battery profile that you can customize.

The structure of a custom profile JSON file is:

```json
{
  "interests": {
    "Category 1": ["keyword1", "keyword2", "keyword3"],
    "Category 2": ["keyword4", "keyword5", "keyword6"]
  },
  "weights": {
    "Category 1": 2.0,
    "Category 2": 1.5
  }
}
```

## Interactive Visualizations

### Standard Session View

Generate an interactive visualization for the ML profile:
```bash
python3 src/plotly_viz.py --profile ml --min-score 5 --output ml_calendar.html
```

Generate a calendar with additional exports:
```bash
python3 src/plotly_viz.py --profile battery --min-score 5 --csv --symposium
```

### Symposium View

Generate a symposium-grouped view for easier navigation:
```bash
python3 src/plotly_viz.py --profile quantum --min-score 3 --symposium-view
```

### Custom Profile Visualization

Use the NVIDIA profile to generate an interactive visualization:
```bash
python3 src/plotly_viz.py --interests nvidia_profile.json --min-score 5
```

### Export to PNG

Generate a static PNG visualization for inclusion in documents:
```bash
python3 src/plotly_viz.py --profile battery --min-score 5 --output battery_calendar.html --export-png
```

This will create both an interactive HTML file and a static PNG file.

### Filtering by Focus Area

Show only sessions related to specific focus areas:
```bash
python3 src/plotly_viz.py --profile am --areas "Process Optimization" "Materials Development"
```

## Data Exports

### Generate CSV Export

Export relevant sessions to a CSV file:
```bash
python3 src/plotly_viz.py --profile battery --min-score 5 --csv
```

This creates a file named `battery_sessions.csv` containing all sessions that match the battery profile with a score of 5 or higher.

### Generate Symposium Report

Generate a report of recommended symposiums:
```bash
python3 src/plotly_viz.py --profile battery --min-score 5 --symposium
```

This creates a file named `battery_symposiums.txt` with a ranked list of symposiums most relevant to your interests.

## Generating All Examples

To regenerate all example outputs for all profiles:

```bash
# Move to the project root
cd /path/to/tms-planner

# Regenerate all PNG files
./fix_pngs.sh

# Generate CSV and symposium reports
./generate_csv_examples.sh
```

## Advanced Options

### Adjusting Minimum Score

The minimum score controls how selective the visualization is:

```bash
# More selective (fewer sessions)
python3 src/plotly_viz.py --profile battery --min-score 8

# Less selective (more sessions)
python3 src/plotly_viz.py --profile battery --min-score 3
```

### Opening the Visualization Automatically

To open the visualization in a browser after generation:

```bash
python3 src/plotly_viz.py --profile ml --min-score 5 --open
```

### Custom Output Path

Specify a custom output file path:

```bash
python3 src/plotly_viz.py --profile battery --output /path/to/my_visualization.html
```

## Troubleshooting Examples

If you encounter errors with the PNG visualization:
```bash
# Ensure kaleido is installed
pip3 install -U kaleido

# Regenerate all PNGs
./fix_pngs.sh
```

If you need to specify the data file location:
```bash
python3 src/tms_planner.py --profile ml --file /path/to/TMS2025AI_Excel_02-21-2025.xlsx
```

If HTML files don't display properly on GitHub, try:
1. Clone the repository and open locally
2. Use GitHub Pages to host the files
3. Use a service like htmlpreview.github.io:
   ```
   https://htmlpreview.github.io/?https://github.com/yourusername/tms-planner/blob/main/examples/battery/battery_calendar.html
   ``` 