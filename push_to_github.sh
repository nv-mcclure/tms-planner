#!/bin/bash
# Script to push the TMS Planner to GitHub

# Change to the project directory
cd "$(dirname "$0")"

# Initialize git repo if not already done
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "Initial commit: TMS Conference Planner"
fi

# Add GitHub remote (replace with your GitHub username if different)
git remote add origin https://github.com/nv-mcclure/tms-planner.git

# Push to GitHub
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo "Your repository is now available at: https://github.com/nv-mcclure/tms-planner" 