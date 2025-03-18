# TMS Conference Planner

A toolset for analyzing and personalizing your TMS 2025 conference schedule based on research interests.

## Features

- **Analyze TMS Schedule**: Get a comprehensive overview of sessions, speakers, and topics
- **Priority Session Details**: View detailed information on important sessions
- **Optimized Day-by-Day Schedule**: Generate chronological schedules with conflict detection
- **NVIDIA Business Justification**: Categorize sessions by NVIDIA product relevance
- **User-Customized Featurizer**: Create personalized schedules based on research interests

## Requirements

- Python 3.6+
- pandas
- numpy
- seaborn (for plots)
- matplotlib (for visualizations)

## Installation

1. Clone this repository or download the files
2. Install required packages:
   ```
   pip install pandas numpy seaborn matplotlib
   ```
3. Make sure you have the TMS conference data file (`TMS2025AI_Excel_02-21-2025.xlsx` or similar)

## Usage

### Command Line Interface

The `tms_planner.py` script provides a user-friendly command-line interface:

```bash
# List available research profiles
python tms_planner.py --list-profiles

# Generate a schedule using a pre-defined profile
python tms_planner.py --profile battery

# Generate a template interests file to customize
python tms_planner.py --template my_interests.json

# Use a custom interests file
python tms_planner.py --interests my_interests.json

# Specify a different conference data file
python tms_planner.py --profile ml --file TMS2025_Updated.xlsx

# Adjust the minimum relevance score (default: 3)
python tms_planner.py --profile quantum --min-score 4
```

### Available Research Profiles

- **battery**: Battery materials, characterization, and manufacturing
- **ml**: Machine learning, data science, and materials informatics
- **am**: Additive manufacturing processes, materials, and characterization
- **quantum**: Quantum methods, DFT, and computational materials science
- **corrosion**: Corrosion phenomena, environments, and resistant materials

### Creating Custom Interest Profiles

Generate a template file:
```bash
python tms_planner.py --template my_interests.json
```

Edit the generated JSON file to match your research interests, then use it:
```bash
python tms_planner.py --interests my_interests.json
```

### Using the Full Analysis Script

For more detailed analysis, you can use the `analyze_tms.py` script directly:

```bash
python analyze_tms.py
```

This script provides additional analyses including:
- Detailed information about priority sessions
- Day-by-day optimized schedule
- NVIDIA-relevant sessions with business justifications

## Custom Interests File Format

The JSON format for custom interests:

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

- **interests**: Dictionary mapping categories to lists of keywords
- **weights** (optional): Dictionary assigning importance weights to each category

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for improvements or bug fixes. 