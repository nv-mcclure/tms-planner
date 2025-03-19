#!/bin/bash
# Generate example visualizations for all profiles

# Create examples directory if it doesn't exist
mkdir -p examples

# Define profiles
profiles=("battery" "ml" "am" "quantum" "corrosion")
custom_profiles=("nvidia")
min_score=5  # Use a higher minimum score for less cluttered visualizations

echo "Generating visualizations for profiles: ${profiles[@]} ${custom_profiles[@]}"

# Process standard profiles
for profile in "${profiles[@]}"
do
  echo
  echo "=== Generating visualization for ${profile} profile ==="
  
  # Generate HTML visualizations
  echo "Creating standard calendar view (HTML)..."
  python3 src/plotly_viz.py --profile ${profile} --min-score ${min_score} \
    --output examples/${profile}_calendar.html --csv --symposium
  
  echo "Creating symposium view (HTML)..."
  python3 src/plotly_viz.py --profile ${profile} --min-score ${min_score} \
    --output examples/${profile}_calendar_symposiums.html --symposium-view
  
  # Generate PNG visualization (if needed)
  if command -v kaleido >/dev/null 2>&1 || python3 -c "import kaleido" >/dev/null 2>&1; then
    echo "Creating PNG visualization..."
    python3 src/save_calendar.py --profile ${profile} --min-score ${min_score} \
      --output examples/${profile}_calendar.png
  else
    echo "Skipping PNG generation (kaleido package not found)"
  fi
  
  # Move CSV and txt files to examples directory
  if [ -f "${profile}_sessions.csv" ]; then
    mv ${profile}_sessions.csv examples/
  fi
  
  if [ -f "${profile}_symposiums.txt" ]; then
    mv ${profile}_symposiums.txt examples/
  fi
done

# Process custom profile files
for profile in "${custom_profiles[@]}"
do
  echo
  echo "=== Generating visualization for ${profile} profile ==="
  
  # Generate HTML visualizations
  echo "Creating standard calendar view (HTML)..."
  python3 src/plotly_viz.py --interests ${profile}_profile.json --min-score ${min_score} \
    --output examples/${profile}_calendar.html --csv --symposium
  
  echo "Creating symposium view (HTML)..."
  python3 src/plotly_viz.py --interests ${profile}_profile.json --min-score ${min_score} \
    --output examples/${profile}_calendar_symposiums.html --symposium-view
  
  # Generate PNG visualization (if needed)
  if command -v kaleido >/dev/null 2>&1 || python3 -c "import kaleido" >/dev/null 2>&1; then
    echo "Creating PNG visualization..."
    python3 src/save_calendar.py --interests ${profile}_profile.json --min-score ${min_score} \
      --output examples/${profile}_calendar.png
  else
    echo "Skipping PNG generation (kaleido package not found)"
  fi
  
  # Move CSV and txt files to examples directory
  if [ -f "${profile}_profile_sessions.csv" ]; then
    mv ${profile}_profile_sessions.csv examples/${profile}_sessions.csv
  fi
  
  if [ -f "${profile}_profile_symposiums.txt" ]; then
    mv ${profile}_profile_symposiums.txt examples/${profile}_symposiums.txt
  fi
done

echo
echo "All visualizations generated in the 'examples' directory."
ls -la examples/

echo
echo "To view the HTML visualizations, open any of the .html files in your web browser."
echo "Example: firefox examples/battery_calendar.html" 