#!/bin/bash

# Copyright 2025 NVIDIA Corporation. All rights reserved.
# Licensed under the Apache License, Version 2.0
# Initialize Git repository

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit of TMS Planner"

echo "Git repository initialized!"
echo "Next steps:"
echo "1. Connect to a remote repository: git remote add origin <repository-url>"
echo "2. Push your code: git push -u origin main" 