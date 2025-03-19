# TMS Planner Example Profiles

This directory contains example interest profiles that can be used with the TMS Planner tool.

## Available Examples

- **example_profile.json**: A sample profile focused on battery materials research
  - Includes interests in battery materials, characterization techniques, and manufacturing processes
  - Uses weighted preferences to prioritize certain categories

## Using Example Profiles

You can use any example profile with the TMS Planner by running:

```bash
python src/tms_planner.py --interests examples/example_profile.json
```

## Creating Your Own Profiles

The easiest way to create your own profile is to use the interactive helper:

```bash
python src/create_interests.py
```

This will guide you through the process of defining research interests and will save the profile as a JSON file.

Alternatively, you can copy and modify any example profile to suit your needs.

# TMS Conference Planner Examples

This directory contains example scripts that demonstrate the functionality of the TMS Conference Planner.

## Demo Calendar Visualization

The `demo_calendar.py` script demonstrates the calendar visualization feature of the TMS Conference Planner. This script:

1. Attempts to load the real conference data file if available
2. If the real data is not found, it creates a sample dataset with randomly generated sessions
3. Generates and displays multiple calendar visualizations:
   - A full schedule view
   - A filtered view based on specified research areas and minimum score
   - Saves the visualization as a PNG file

### Running the Demo

```bash
# From the repository root
python3 examples/demo_calendar.py

# From the examples directory
cd examples
python3 demo_calendar.py
```

> **Note**: On macOS systems, you must use `python3` command rather than `python`.

> **Note**: If you encounter visualization errors, try using the text-based output only by editing the script to set `show_calendar = False`.

### Example Output

The script will generate calendar visualizations that show:

- Sessions organized by day and room
- Color-coded sessions based on research areas
- Score indicators for each session
- Filtered views based on relevance scores

The calendar visualization has the following features:

- **Day-by-Day View**: Each conference day is displayed as a separate subplot
- **Room Organization**: Sessions are grouped by room (horizontally)
- **Time Slots**: The vertical axis represents time, with sessions displayed at their scheduled times
- **Color Coding**: Different research areas are shown in different colors
- **Relevance Scores**: Sessions display their relevance score
- **Transparency**: Higher scoring sessions appear more opaque

## Troubleshooting

If you encounter errors related to the calendar visualization:

1. Make sure you're using Python 3.6+ with up-to-date matplotlib and pandas libraries:
   ```bash
   pip3 install --upgrade matplotlib pandas
   ```

2. Run the planner without visualization:
   ```bash
   python3 src/tms_planner.py --profile battery --no-calendar
   ```

3. For the demo script, edit the file and set `show_calendar = False` at the end of the `main()` function.

## Customizing the Visualization

You can modify the `demo_calendar.py` script to:

1. Change the sample dataset parameters
2. Adjust the research areas and keywords
3. Modify the minimum score threshold
4. Save visualizations with different filenames and resolution

## Interactive Use

When running the script, the visualizations will appear in interactive matplotlib windows that allow you to:

- Zoom in/out
- Pan around
- Save the visualization manually
- Adjust the figure layout 