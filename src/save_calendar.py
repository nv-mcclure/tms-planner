#!/usr/bin/env python3
"""
save_calendar.py - Generate and save calendar visualizations as PNG files

This script loads conference data and generates high-quality calendar visualizations
for specific research profiles or custom interests.
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyze_tms import (
    load_conference_data, 
    visualize_schedule_calendar, 
    find_data_file
)

# Import predefined research profiles from tms_planner.py
try:
    from src.tms_planner import RESEARCH_PROFILES
except ImportError:
    # If importing fails, define a minimal set
    RESEARCH_PROFILES = {
        "battery": {
            "Battery Materials": ["battery", "lithium", "cathode", "anode", "electrolyte", "energy storage", "solid-state"],
            "Characterization": ["XRD", "XPS", "TEM", "SEM", "spectroscopy", "in-situ", "operando"],
            "Manufacturing": ["coating", "roll-to-roll", "scale-up", "production", "synthesis"]
        }
    }

def save_calendar_visualization(data_file=None, profile=None, interests_file=None,
                              min_score=5, output_file=None, dpi=300, 
                              title=None, nvidia_focus=False):
    """Generate and save a calendar visualization as a PNG file.
    
    Parameters:
    -----------
    data_file : str, optional
        Path to the conference data Excel file (default: auto-detect)
    profile : str, optional
        Name of a predefined research profile (default: None)
    interests_file : str, optional
        Path to a JSON file with custom interests (default: None)
    min_score : int, optional
        Minimum relevance score (default: 5)
    output_file : str, optional
        Path to save the PNG file (default: "calendar_{profile/interests}_{min_score}.png")
    dpi : int, optional
        Resolution of the output image (default: 300)
    title : str, optional
        Custom title for the visualization (default: derived from profile/interests)
    nvidia_focus : bool, optional
        Highlight NVIDIA product relevance (default: False)
    """
    # Auto-detect the data file if not specified
    if data_file is None:
        data_file = find_data_file("TMS2025AI_Excel_02-21-2025.xlsx")
        if data_file is None:
            print("Error: Could not find the conference data file.")
            sys.exit(1)
    
    # Load the conference data
    print(f"Loading data from: {data_file}")
    df = load_conference_data(data_file)
    if df is None:
        print("Error: Failed to load the conference data.")
        sys.exit(1)
    
    # Determine the focus areas
    focus_areas = None
    
    # If a profile is specified, use the predefined focus areas
    if profile:
        if profile in RESEARCH_PROFILES:
            focus_areas = RESEARCH_PROFILES[profile]
            label = profile
        else:
            print(f"Error: Unknown profile '{profile}'.")
            print(f"Available profiles: {', '.join(RESEARCH_PROFILES.keys())}")
            sys.exit(1)
    
    # If an interests file is specified, load the custom focus areas
    elif interests_file:
        try:
            import json
            with open(interests_file, 'r') as f:
                data = json.load(f)
            
            if "interests" in data:
                # New format
                focus_areas = data["interests"]
            elif "user_interests" in data:
                # Legacy format
                focus_areas = data["user_interests"]
            else:
                print("Error: Interests file doesn't contain 'interests' or 'user_interests' key.")
                sys.exit(1)
            
            label = os.path.splitext(os.path.basename(interests_file))[0]
        except Exception as e:
            print(f"Error loading interests file: {e}")
            sys.exit(1)
    else:
        print("Error: Either a profile or an interests file must be specified.")
        sys.exit(1)
    
    # Determine the output file if not specified
    if output_file is None:
        output_file = f"calendar_{label}_score{min_score}.png"
    
    # Determine the title if not specified
    if title is None:
        title = f"TMS Conference Schedule - {label.title()} Focus (min score: {min_score})"
    
    # Generate the visualization
    print(f"Generating visualization with minimum score: {min_score}")
    fig = visualize_schedule_calendar(df, min_score=min_score, focus_areas=focus_areas, title=title)
    
    if fig is None:
        print("Error: Failed to generate the visualization.")
        sys.exit(1)
    
    # Save the figure
    print(f"Saving visualization to: {output_file}")
    fig.savefig(output_file, dpi=dpi, bbox_inches='tight')
    print(f"Successfully saved to {output_file}")
    
    # Also display it if running interactively
    plt.show()

def main():
    """Main function to parse command line arguments and generate the visualization."""
    parser = argparse.ArgumentParser(
        description="Generate and save calendar visualizations as PNG files"
    )
    
    # Input options
    parser.add_argument("--file", "-f", help="Path to the conference data Excel file")
    
    # Content selection options
    profile_group = parser.add_mutually_exclusive_group(required=True)
    profile_group.add_argument("--profile", "-p", help="Use a predefined research profile")
    profile_group.add_argument("--interests", "-i", help="Path to a JSON file with custom interests")
    
    # Visualization options
    parser.add_argument("--min-score", "-m", type=int, default=5, 
                      help="Minimum relevance score (default: 5)")
    parser.add_argument("--output", "-o", help="Path to save the PNG file")
    parser.add_argument("--dpi", type=int, default=300, 
                      help="Resolution of the output image (default: 300)")
    parser.add_argument("--title", "-t", help="Custom title for the visualization")
    parser.add_argument("--nvidia", action="store_true", 
                      help="Highlight NVIDIA product relevance")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Generate and save the visualization
    save_calendar_visualization(
        data_file=args.file,
        profile=args.profile,
        interests_file=args.interests,
        min_score=args.min_score,
        output_file=args.output,
        dpi=args.dpi,
        title=args.title,
        nvidia_focus=args.nvidia
    )

if __name__ == "__main__":
    main() 