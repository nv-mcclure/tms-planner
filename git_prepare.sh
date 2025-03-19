#!/bin/bash
# Git preparation script for TMS Planner

echo "Preparing repository for Git..."

# Add core source files
git add src/*.py
git add setup.sh
git add git_prepare.sh

# Add documentation
git add README.md
git add examples/README.md
git add examples/example_usage.md

# Add example JSON profile
git add *.json
git add examples/*.json

# Add shell scripts
git add src/*.sh
git add *.sh

# Add utility scripts
git add check_time_issues.py

# Create data directory with README
mkdir -p data
cat > data/README.md << 'EOL'
# TMS Conference Data

This directory should contain the TMS conference data file:

`TMS2025AI_Excel_02-21-2025.xlsx`

This file is not included in the repository due to size constraints. Please obtain it from TMS or your conference organizer and place it in this directory.

## Automatic Detection

The application will automatically detect the data file if it's placed in this directory. Alternatively, you can specify its location using the `--file` option when running the planner.
EOL

# Add data directory README
git add data/README.md

# Create examples directory and make sure it's tracked
mkdir -p examples
git add examples/README.md

# Add .gitignore
git add .gitignore

echo "Files have been added to git staging area."
echo "Use 'git status' to review changes and 'git commit' to commit them." 