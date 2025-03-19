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

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for improvements or bug fixes. 

## License

Licensed under the Apache License, Version 2.0. 