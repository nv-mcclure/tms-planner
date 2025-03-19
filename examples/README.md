# TMS Planner Examples

This directory contains example visualizations and data exports generated using the TMS Conference Planner. These examples demonstrate the different types of outputs the planner can generate for various research profiles.

## Available Examples

Each research profile has the following files:

- `*_calendar.html` - Interactive calendar visualization (standard view)
- `*_calendar_symposiums.html` - Interactive calendar visualization (symposium view)
- `*_calendar.png` - Static PNG version of the standard calendar view
- `*_calendar_symposium.png` - Static PNG version of the symposium view
- `*_sessions.csv` - CSV export of relevant sessions
- `*_symposiums.txt` - Text report of top recommended symposiums

## Static vs. Interactive Visualizations

This directory contains two types of visualizations:

1. **HTML Files** (Interactive): These provide the richest experience with interactive features like hovering for details, filtering by clicking legend items, and zooming controls.

2. **PNG Files** (Static): These are static image exports suitable for including in documents, presentations, or viewing without a web browser.

### Viewing HTML Files on GitHub

When viewing HTML files from this repository on GitHub:

1. Use the "Raw" button to view the file directly
2. Use a service like [htmlpreview.github.io](https://htmlpreview.github.io/) by prepending this URL:
   ```
   https://htmlpreview.github.io/?https://github.com/yourusername/tms-planner/blob/main/examples/battery_calendar.html
   ```
3. Clone the repository locally and open the HTML files in your browser

## Standard Profiles

The following standard research profiles are included:

- `battery` - Battery materials and characterization
- `ml` - Machine learning and AI in materials science
- `am` - Additive manufacturing
- `quantum` - Quantum computing and DFT simulations
- `corrosion` - Corrosion science and prevention

## Custom Profile Example

The `nvidia` example demonstrates how to create a custom profile. To create your own custom profile:

1. Create a JSON file similar to `nvidia_profile.json` in the root directory
2. Define your interests and weights in the JSON file
3. Run the planner with `--interests your_profile.json`

### NVIDIA Profile Structure

```json
{
  "interests": {
    "AI & Deep Learning": [
      "deep learning", 
      "neural network", 
      "AI", 
      "machine learning", 
      "data mining", 
      "artificial intelligence",
      "GPU", 
      "tensor cores", 
      "CUDA"
    ],
    "Digital Twins & Simulation": [
      "simulation", 
      "modeling", 
      "digital twin", 
      "prediction", 
      "CAE", 
      "computational",
      "omniverse",
      "physics-based"
    ],
    "Materials Science & Discovery": [
      "materials discovery", 
      "high-throughput", 
      "materials design", 
      "property prediction",
      "atomic scale",
      "computational materials"
    ]
  },
  "weights": {
    "AI & Deep Learning": 2.0,
    "Digital Twins & Simulation": 1.5,
    "Materials Science & Discovery": 1.7
  }
}
```

## Viewing Examples

To view the interactive visualizations, open any of the HTML files in a web browser. The visualizations allow you to:

- Filter sessions by clicking on legend items
- Hover over sessions for detailed information
- Zoom in on specific time periods using the buttons at the top

## Troubleshooting PNG Generation

If you encounter issues with PNG file generation:

1. **Install or Update Kaleido**: The Plotly PNG export functionality requires the Kaleido package:
   ```bash
   pip3 install -U kaleido
   ```

2. **Fix Corrupted PNGs**: If your PNG files appear to be corrupted, you can regenerate them using:
   ```bash
   ./fix_pngs.sh
   ```
   
3. **Memory Issues**: If you encounter memory errors with large visualizations, try:
   - Increasing the minimum score to reduce the number of sessions
   - Generating only one visualization at a time
   - Restarting your system to free up memory

4. **Alternative Approach**: If PNG generation continues to fail, you can:
   - Use the interactive HTML visualizations instead
   - Take screenshots of the HTML visualizations
   - Use browser print/save functionality to create PDFs

## Generating Your Own Examples

You can generate your own examples by running:

```bash
# Using a predefined profile
python3 src/plotly_viz.py --profile battery --min-score 5 --output my_calendar.html

# Using a custom profile
python3 src/plotly_viz.py --interests my_profile.json --min-score 5 --output my_calendar.html
```

Or use the `generate_all_examples.sh` script to generate visualizations for all profiles at once.

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