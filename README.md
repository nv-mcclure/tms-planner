# TMS Conference Planner

A toolset for analyzing and personalizing your TMS 2025 conference schedule based on research interests.

## Features

- **Analyze TMS Schedule**: Get a comprehensive overview of sessions, speakers, and topics
- **Priority Session Details**: View detailed information on important sessions
- **Optimized Day-by-Day Schedule**: Generate chronological schedules with conflict detection
- **NVIDIA Business Justification**: Categorize sessions by NVIDIA product relevance
- **User-Customized Featurizer**: Create personalized schedules based on research interests
- **Calendar Visualization**: View your schedule in an easy-to-read calendar format

## Requirements

- Python 3.6+
- pandas
- numpy
- seaborn (for plots)
- matplotlib (for visualizations)

## Installation

1. Clone this repository or download the files:
   ```
   git clone https://github.com/yourusername/tms-planner.git
   cd tms-planner
   ```

2. Install required packages:
   ```
   pip3 install pandas numpy seaborn matplotlib
   ```

3. Data File Setup:
   - The planner expects the TMS conference data file (`TMS2025AI_Excel_02-21-2025.xlsx`) to be in the `data/` directory.
   - The file location will be auto-detected as long as it's in one of the following locations:
     - `data/TMS2025AI_Excel_02-21-2025.xlsx` (from repository root)
     - `./data/TMS2025AI_Excel_02-21-2025.xlsx` (relative to current directory)
     - `src/../data/TMS2025AI_Excel_02-21-2025.xlsx` (relative to the src directory)
   - You can also specify the file path explicitly using the `--file` option.

## Usage

### Command Line Interface

The `tms_planner.py` script provides a user-friendly command-line interface:

```bash
# List available research profiles
python3 src/tms_planner.py --list-profiles

# Generate a schedule using a pre-defined profile
python3 src/tms_planner.py --profile battery

# Use a custom interests file
python3 src/tms_planner.py --interests my_interests.json

# Specify a different conference data file
python3 src/tms_planner.py --profile ml --file /path/to/TMS2025_Updated.xlsx

# Adjust the minimum relevance score (default: 5)
python3 src/tms_planner.py --profile quantum --min-score 8

# Run from the src directory
cd src
python3 tms_planner.py --profile battery
```

### Known Issues

If you encounter a `command not found: python` error, make sure to use `python3` instead of `python` in all commands. This is especially common on macOS systems.

If the calendar visualization causes errors, you can disable it with the `--no-calendar` flag:

```bash
python3 src/tms_planner.py --profile battery --no-calendar
```

### Available Research Profiles

The planner comes with pre-defined research profiles to get you started quickly:

- **battery**: Battery materials, characterization, and manufacturing
- **ml**: Machine learning, data science, and materials informatics applications
- **am**: Additive manufacturing processes, materials, and characterization
- **quantum**: Quantum methods, DFT, and computational materials science
- **corrosion**: Corrosion phenomena, environments, and resistant materials

View all available profiles and their keywords:
```bash
python3 src/tms_planner.py --list-profiles
```

### Creating Custom Interest Profiles

To use your own research interests, create a JSON file with the following format:

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

Then use it with:
```bash
python3 src/tms_planner.py --interests my_interests.json
```

- **interests**: Dictionary mapping categories to lists of keywords
- **weights** (optional): Dictionary assigning importance weights to each category (default: 1.0)

#### Example: NVIDIA Custom Profile

A more comprehensive example is provided in the `nvidia_profile.json` file:

```json
{
  "interests": {
    "AI & Deep Learning": [
      "deep learning", "neural network", "AI", "machine learning", 
      "data mining", "artificial intelligence", "GPU", "tensor cores", "CUDA"
    ],
    "Digital Twins & Simulation": [
      "simulation", "modeling", "digital twin", "prediction", 
      "CAE", "computational", "omniverse", "physics-based"
    ],
    "Materials Science & Discovery": [
      "materials discovery", "high-throughput", "materials design", 
      "property prediction", "atomic scale", "computational materials"
    ]
  },
  "weights": {
    "AI & Deep Learning": 2.0,
    "Digital Twins & Simulation": 1.5,
    "Materials Science & Discovery": 1.7
  }
}
```

Using this model, you can create custom profiles tailored to any research interest. For more examples, check the [examples directory](examples/).

### Adjusting Schedule Relevance

You can control how many sessions appear in your personalized schedule by adjusting the minimum relevance score:

```bash
# More selective schedule (higher minimum score)
python3 src/tms_planner.py --profile battery --min-score 8

# More inclusive schedule (lower minimum score)
python3 src/tms_planner.py --profile battery --min-score 3
```

### Calendar Visualization

The planner includes a powerful calendar visualization feature that displays your personalized schedule in an easy-to-read format:

```bash
# Generate a schedule with default calendar visualization
python3 src/tms_planner.py --profile battery

# Disable calendar visualization 
python3 src/tms_planner.py --profile battery --no-calendar

# Save the visualization to a file
python3 src/tms_planner.py --profile battery --output my_schedule.png
```

#### Visualization Features

- **Day-by-Day View**: Each conference day is shown as a separate panel
- **Room Organization**: Sessions are arranged by room locations
- **Time Slots**: Sessions are placed according to their scheduled time
- **Color Coding**: Different research areas have distinct colors
- **Relevance Scores**: Each session displays its relevance score
- **Focus Areas**: Legend shows which research areas are represented

For an example visualization and more details, see the [examples directory](examples/).

## Interactive Calendar Visualization

The TMS Planner includes an interactive visualization that lets you explore your personalized schedule with advanced features:

```bash
python3 src/plotly_viz.py --profile battery --min-score 3 --open
```

Features:
- **Interactive Hover**: Hover over any session to see full details including abstract, speaker, and matching keywords
- **Clickable Legend**: Click on legend items to show/hide specific research areas
- **Time Filtering**: Use the buttons to quickly focus on morning or afternoon sessions
- **Color Coding**: Sessions are color-coded by research area for easy identification
- **Responsive Layout**: Adjusts to screen size for optimal viewing
- **Symposium View**: Group sessions by symposium for a clearer overview (`--symposium-view` flag)
- **CSV Export**: Generate a CSV file of all matched sessions (`--csv` flag)
- **Symposium Reports**: Generate a text report of top recommended symposiums (`--symposium` flag)

Options:
- `--profile NAME` or `--interests FILE`: Specify research interests (required)
- `--min-score N`: Minimum relevance score to include sessions (default: 3)
- `--output FILE`: Custom output HTML file path (default: auto-generated)
- `--title TEXT`: Custom title for the visualization
- `--open`: Automatically open in your web browser after generating
- `--symposium-view`: Group sessions by symposium instead of showing individual sessions
- `--csv`: Generate a CSV export of matched sessions
- `--symposium`: Generate a report of recommended symposiums
- `--areas AREA1 AREA2`: Filter to only show specific focus areas (space-separated)

Examples:
```bash
# Generate a standard view with CSV export
python3 src/plotly_viz.py --profile battery --min-score 5 --csv

# Generate a symposium view with symposium report
python3 src/plotly_viz.py --profile ml --min-score 4 --symposium-view --symposium

# Use a custom profile and filter to specific areas
python3 src/plotly_viz.py --interests nvidia_profile.json --min-score 5 --areas "AI & Deep Learning"

# Generate all outputs at once
python3 src/plotly_viz.py --profile am --min-score 3 --csv --symposium --output am_calendar.html
```

The visualization is saved as an HTML file that you can share, save for offline viewing, or open in any browser.

### Generate All Examples

To generate visualizations for all available profiles:

```bash
# Make the script executable
chmod +x src/generate_all_examples.sh

# Run the script
./src/generate_all_examples.sh
```

This will create HTML visualizations (both standard and symposium views), CSV exports, and symposium reports for all predefined profiles in the `examples/` directory.

## Requirements

To run the interactive visualization, you'll need to install Plotly:

```bash
pip3 install plotly
```

## Generating Calendar Visualizations

To generate a calendar visualization of your schedule as a PNG file:

```bash
python3 src/save_calendar.py --interests nvidia_profile.json --min-score 7 --output schedule.png --title "My TMS Schedule"
```

Options:
- `--interests FILE` or `--profile NAME`: Specify your research interests (required)
- `--min-score N`: Minimum relevance score to include sessions (default: 3)
- `--output FILE`: Output PNG file path (default: calendar.png)
- `--title TEXT`: Title for the visualization (default: "Conference Schedule")

The visualization will show sessions arranged by day and room, color-coded by research area, with relevance scores in parentheses.

## Troubleshooting

### Data File Not Found

If you encounter the error `Error: Could not find the Excel file`, you can:

1. Make sure the data file is in the expected location (`data/TMS2025AI_Excel_02-21-2025.xlsx`)
2. Specify the file path explicitly with:
   ```
   python3 src/tms_planner.py --profile battery --file /full/path/to/TMS2025AI_Excel_02-21-2025.xlsx
   ```
3. Create a symbolic link to the file in the expected location:
   ```
   ln -s /path/to/your/file.xlsx data/TMS2025AI_Excel_02-21-2025.xlsx
   ```

### Visualization Issues

If you encounter issues with the visualizations:

1. **Time Parsing Errors**: The planner automatically corrects time formatting issues in the data, ensuring that start times are always before end times. This fixes cases where AM/PM confusion might cause end times to appear before start times.

2. **Calendar Rendering Errors**: If the matplotlib calendar visualization causes errors, use the new interactive Plotly visualization instead:
   ```bash
   python3 src/plotly_viz.py --profile battery
   ```

3. **Memory Issues with Large Exports**: If generating visualizations for profiles with too many matches (like `am`), try increasing the minimum score to reduce the number of sessions:
   ```bash
   python3 src/plotly_viz.py --profile am --min-score 8
   ```

4. **Missing Modules**: If you get module not found errors, make sure you've installed all dependencies:
   ```bash
   pip3 install pandas numpy matplotlib seaborn plotly
   ```

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for improvements or bug fixes. 

## License

Licensed under the Apache License, Version 2.0. 