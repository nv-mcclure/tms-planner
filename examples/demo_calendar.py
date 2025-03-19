#!/usr/bin/env python3
# demo_calendar.py
# Demonstration of the TMS Conference Planner Calendar Visualization

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from src.analyze_tms import visualize_schedule_calendar, find_data_file, load_conference_data

def create_sample_data():
    """Create a sample dataset for demonstration"""
    # Sample conference dates (3 days)
    dates = [
        pd.Timestamp('2025-03-25'),
        pd.Timestamp('2025-03-26'),
        pd.Timestamp('2025-03-27')
    ]
    
    # Define sample rooms
    rooms = ['101', '102', '201', '202', '301']
    
    # Set up data structure
    data = []
    
    # Sample topics organized by research area
    session_topics = {
        'Battery Materials': [
            'Advances in Solid-State Battery Materials',
            'Novel Cathode Materials for Li-ion Batteries',
            'Understanding Interface Reactions in Battery Systems',
            'Next-Generation Electrolytes for Energy Storage',
            'Sustainable Battery Materials and Recycling',
            'High-Energy Density Anode Development'
        ],
        'Machine Learning': [
            'Machine Learning for Materials Discovery',
            'AI Applications in Process Optimization',
            'Deep Learning for Microstructure Analysis',
            'Data Science in Materials Engineering',
            'Neural Networks for Property Prediction',
            'Generative Models for Material Design'
        ],
        'Additive Manufacturing': [
            'Powder Bed Fusion Process Optimization',
            'Microstructure Control in AM Components',
            'In-situ Monitoring of AM Processes',
            'Design for Additive Manufacturing',
            'Post-Processing of AM Materials',
            'Novel Alloys for Metal AM'
        ]
    }
    
    # Generate sessions spread across the conference
    session_id = 1
    for date in dates:
        # Morning sessions (9:00 - 12:00)
        for start_hour in range(9, 12):
            for room in rooms:
                # Randomly select a research area
                area = np.random.choice(list(session_topics.keys()))
                # Randomly select a topic from that area
                topic = np.random.choice(session_topics[area])
                
                # Create a session
                data.append({
                    'ID': session_id,
                    'Date': date,
                    'Start': f'{start_hour:02d}:00',
                    'End': f'{start_hour+1:02d}:00',
                    'Location': room,
                    'Title': topic,
                    'Type': 'Technical Session',
                    'Track': area,
                    'Description': f'This session explores recent advances in {topic.lower()}.',
                    'RelevanceScore': np.random.randint(1, 11)  # Random score 1-10
                })
                session_id += 1
        
        # Afternoon sessions (13:30 - 17:30)
        for start_hour in range(13, 17):
            for room in rooms:
                # Randomly select a research area
                area = np.random.choice(list(session_topics.keys()))
                # Randomly select a topic from that area
                topic = np.random.choice(session_topics[area])
                
                # Create a session
                data.append({
                    'ID': session_id,
                    'Date': date,
                    'Start': f'{start_hour:02d}:30',
                    'End': f'{start_hour+1:02d}:30',
                    'Location': room,
                    'Title': topic,
                    'Type': 'Technical Session',
                    'Track': area,
                    'Description': f'This session explores recent advances in {topic.lower()}.',
                    'RelevanceScore': np.random.randint(1, 11)  # Random score 1-10
                })
                session_id += 1
    
    # Create DataFrame
    return pd.DataFrame(data)

def main():
    """Main function to demonstrate the calendar visualization"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Demonstrate TMS calendar visualization")
    parser.add_argument("--no-calendar", action="store_true", help="Disable calendar visualization (text output only)")
    parser.add_argument("--min-score", type=int, default=5, help="Minimum relevance score (default: 5)")
    args = parser.parse_args()
    
    # Set visualization flag
    show_calendar = not args.no_calendar
    min_score = args.min_score
    
    # Try to use the real data file first
    file_path = find_data_file("TMS2025AI_Excel_02-21-2025.xlsx")
    
    if file_path:
        print(f"Using real conference data from: {file_path}")
        df = load_conference_data(file_path)
    else:
        print("Real data file not found. Creating sample data for demonstration.")
        df = create_sample_data()
    
    if df is None or df.empty:
        print("Error: Failed to load or create data.")
        return
    
    # Define sample focus areas for demonstration
    focus_areas = {
        "Battery Materials": ["battery", "lithium", "cathode", "anode", "electrolyte", "energy storage", "solid-state"],
        "Machine Learning": ["machine learning", "deep learning", "neural network", "AI", "data science", "prediction"],
        "Additive Manufacturing": ["additive manufacturing", "AM", "3D printing", "powder bed", "LPBF", "DED"]
    }
    
    # Print text-based schedule summary
    print("\nSchedule Summary:")
    print(f"Total sessions: {len(df)}")
    
    # Group by date
    if 'Date' in df.columns:
        for date, group in df.groupby('Date'):
            print(f"\n{date.strftime('%A, %B %d, %Y')}: {len(group)} sessions")
    
    # Print some key sessions by area
    print("\nSample Sessions by Research Area:")
    for area in focus_areas.keys():
        area_keywords = focus_areas[area]
        area_sessions = df[df.apply(lambda row: any(kw.lower() in str(row).lower() for kw in area_keywords), axis=1)]
        print(f"\n{area}: {len(area_sessions)} relevant sessions")
        
        # Print top 3 sessions by score
        if not area_sessions.empty and 'RelevanceScore' in area_sessions.columns:
            top_sessions = area_sessions.sort_values('RelevanceScore', ascending=False).head(3)
            for _, session in top_sessions.iterrows():
                print(f"  - {session['Title']} (Score: {session['RelevanceScore']})")
    
    # Only show visualizations if enabled
    if show_calendar:
        try:
            # Visualize the full schedule
            print("\nGenerating full conference schedule visualization...")
            visualize_schedule_calendar(df, title="Full TMS Conference Schedule")
            
            # Visualize schedule with minimum score filter
            print(f"\nGenerating filtered schedule visualization (min score: {min_score})...")
            visualize_schedule_calendar(df, min_score=min_score, focus_areas=focus_areas, 
                                      title=f"Filtered Conference Schedule (min score: {min_score})")
            
            # Save the visualization
            output_file = "calendar_visualization.png"
            print(f"\nSaving visualization to {output_file}...")
            fig = visualize_schedule_calendar(df, min_score=min_score, focus_areas=focus_areas, 
                                            title=f"TMS Conference Schedule (min score: {min_score})")
            if fig:
                fig.savefig(output_file, dpi=300, bbox_inches='tight')
                print(f"Visualization saved to {output_file}")
        except Exception as e:
            print(f"\nError generating calendar visualization: {e}")
            print("Try running with --no-calendar to use text-based output only.")
    else:
        print("\nCalendar visualization is disabled. Use text-based output above.")
        print("To enable visualization, run without the --no-calendar flag.")

if __name__ == "__main__":
    main() 