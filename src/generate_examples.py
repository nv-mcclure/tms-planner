#!/usr/bin/env python3
"""
Generate example visualizations for all available research profiles
"""

import os
import sys
import argparse
from pathlib import Path

# Import from tms-planner modules
from tms_planner import RESEARCH_PROFILES
from plotly_viz import save_interactive_calendar, create_interactive_calendar, find_data_file
from analyze_tms import load_conference_data
import plotly.io as pio

def generate_all_examples(output_dir="examples", min_score=3, format="html", open_browser=False):
    """
    Generate visualizations for all available research profiles
    
    Parameters:
    -----------
    output_dir : str
        Directory to save visualizations (will be created if it doesn't exist)
    min_score : int
        Minimum relevance score to include sessions
    format : str
        Output format ("html" or "png" or "both")
    open_browser : bool
        Whether to open the first visualization in a browser
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get available profiles
    profiles = list(RESEARCH_PROFILES.keys())
    print(f"Generating {format} visualizations for {len(profiles)} profiles: {', '.join(profiles)}")
    
    # Track if we successfully generated at least one visualization
    success = False
    
    # Generate visualization for each profile
    for i, profile in enumerate(profiles):
        print(f"\n[{i+1}/{len(profiles)}] Generating visualization for profile: {profile}")
        
        # HTML output filename
        html_file = os.path.join(output_dir, f"{profile}_calendar.html")
        
        # Create title with capitalized profile name
        title = f"TMS 2025 - {profile.title()} Focus Areas"
        
        # Generate the visualization
        result = save_interactive_calendar(
            profile=profile,
            min_score=min_score,
            output_file=html_file,
            title=title
        )
        
        if result:
            success = True
            print(f"Successfully saved HTML visualization to: {html_file}")
            
            # Generate PNG if requested
            if format == "png" or format == "both":
                try:
                    # Get data and create figure directly
                    print(f"Generating PNG visualization...")
                    data_file = find_data_file()
                    df = load_conference_data(data_file)
                    
                    # Import again to get access to the function
                    from tms_planner import RESEARCH_PROFILES
                    user_interests = RESEARCH_PROFILES[profile]["interests"]
                    
                    # Create the figure
                    fig = create_interactive_calendar(
                        df, 
                        min_score=min_score, 
                        focus_areas=user_interests, 
                        title=title
                    )
                    
                    # Save as PNG
                    png_file = os.path.join(output_dir, f"{profile}_calendar.png")
                    print(f"Saving PNG visualization to: {png_file}")
                    fig.write_image(png_file, width=1600, height=900, scale=2)
                    print(f"Successfully saved PNG visualization to: {png_file}")
                except Exception as e:
                    print(f"Error generating PNG: {e}")
            
            # Open the first successful visualization if requested
            if open_browser and i == 0:
                import webbrowser
                print(f"Opening visualization in browser: {html_file}")
                webbrowser.open_new_tab(f"file://{os.path.abspath(html_file)}")
        else:
            print(f"Failed to generate visualization for profile: {profile}")
    
    return success

def main():
    """Command-line interface for generating example visualizations"""
    parser = argparse.ArgumentParser(description="Generate example visualizations for all research profiles")
    
    parser.add_argument("--output-dir", "-o", default="examples",
                      help="Directory to save visualizations (default: examples)")
    parser.add_argument("--min-score", "-m", type=int, default=3,
                      help="Minimum relevance score to include sessions (default: 3)")
    parser.add_argument("--format", "-f", choices=["html", "png", "both"], default="html",
                      help="Output format (default: html)")
    parser.add_argument("--open", action="store_true",
                      help="Open the first visualization in a browser")
    
    args = parser.parse_args()
    
    # Generate visualizations
    success = generate_all_examples(
        output_dir=args.output_dir,
        min_score=args.min_score,
        format=args.format,
        open_browser=args.open
    )
    
    if success:
        print(f"\nSuccessfully generated visualizations in directory: {args.output_dir}")
        return 0
    else:
        print("\nFailed to generate visualizations")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 