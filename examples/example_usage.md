# TMS Planner Usage Examples

This document provides examples of how to use the TMS Planner for various tasks.

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

### Filtering by Focus Area

Show only sessions related to specific focus areas:
```bash
python3 src/plotly_viz.py --profile am --areas "Process Optimization" "Materials Development"
```

## Generating All Examples

Generate all example outputs for all profiles:
```bash
chmod +x src/generate_all_examples.sh
./src/generate_all_examples.sh
```

This creates:
- Interactive HTML visualizations (standard view)
- Interactive HTML visualizations (symposium view)
- CSV exports of relevant sessions
- Symposium reports

## Troubleshooting Examples

If you encounter errors with the matplotlib visualization:
```bash
python3 src/tms_planner.py --profile battery --no-calendar
```

If you need to specify the data file location:
```bash
python3 src/tms_planner.py --profile ml --file /path/to/TMS2025AI_Excel_02-21-2025.xlsx
```

If you want to generate calendar visualizations without Plotly:
```bash
python3 src/save_calendar.py --profile battery --output battery_calendar.png
``` 