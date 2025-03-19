#!/usr/bin/env python3
"""
Interactive calendar visualization for TMS Conference Planner using Plotly
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from pathlib import Path

# Import from analyze_tms module
from analyze_tms import score_session_relevance, find_data_file

def time_to_float(time_str):
    """Convert time string to float hours (e.g., '09:30' → 9.5)"""
    try:
        if isinstance(time_str, str):
            if ':' in time_str:
                hours, minutes = map(int, time_str.split(':'))
                # Handle 24-hour format correctly
                # Make sure to constrain hours to 0-23 range
                if hours < 0 or hours > 23:
                    print(f"Warning: Invalid hour in time format: {time_str}, constraining to valid range")
                    hours = max(0, min(hours, 23))
                return hours + minutes / 60.0
            else:
                print(f"Warning: Unexpected time format: {time_str}, using default")
                return 12.0
        elif hasattr(time_str, 'hour') and hasattr(time_str, 'minute'):
            return time_str.hour + time_str.minute / 60.0
        else:
            print(f"Warning: Unknown time format: {time_str}, using default")
            return 12.0
    except Exception as e:
        print(f"Error parsing time '{time_str}': {e}")
        return 12.0

def get_focus_area_colors(focus_areas):
    """Generate distinct colors for each focus area"""
    # Pre-defined distinct colors for better contrast between areas
    distinct_colors = [
        'rgba(31, 119, 180, 0.7)',   # Blue
        'rgba(44, 160, 44, 0.7)',     # Green
        'rgba(214, 39, 40, 0.7)',     # Red
        'rgba(148, 103, 189, 0.7)',   # Purple
        'rgba(140, 86, 75, 0.7)',     # Brown
        'rgba(227, 119, 194, 0.7)',   # Pink
        'rgba(188, 189, 34, 0.7)',    # Olive
        'rgba(23, 190, 207, 0.7)',    # Cyan
    ]
    
    colors = {}
    for i, area in enumerate(focus_areas.keys()):
        # Use pre-defined colors or generate if we have more areas than colors
        if i < len(distinct_colors):
            colors[area] = distinct_colors[i]
        else:
            # Fall back to a generated color if we have more than 8 areas
            import plotly.colors as pc
            colorscale = pc.sequential.Viridis
            colors[area] = pc.sample_colorscale(colorscale, i/(len(focus_areas)-1 or 1))[0]
    
    return colors

def wrap_text(text, width=80):
    """Wrap text to specified width for better hover readability"""
    if not text or not isinstance(text, str):
        return ""
    
    import textwrap
    return "<br>".join(textwrap.wrap(text, width=width))

def generate_symposium_report(df, focus_areas=None, min_score=3):
    """
    Generate a report of suggested symposiums to attend based on interest matches.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Conference data
    focus_areas : dict
        Dictionary mapping focus areas to lists of keywords
    min_score : int
        Minimum relevance score to include sessions
        
    Returns:
    --------
    dict
        A dictionary with symposium information and ratings
    """
    if df is None or df.empty:
        print("No data available to analyze.")
        return None
    
    # Score sessions based on focus areas
    if focus_areas:
        df['relevance_score'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
        # Filter by minimum score
        relevant_df = df[df['relevance_score'] >= min_score].copy()
    else:
        relevant_df = df.copy()
        relevant_df['relevance_score'] = 1
    
    if relevant_df.empty:
        print(f"No sessions with relevance score >= {min_score} found.")
        return None
    
    # Group by symposium
    symposium_data = {}
    
    for symposium, group in relevant_df.groupby('Symposium'):
        # Calculate metrics for this symposium
        total_sessions = len(group)
        avg_score = group['relevance_score'].mean()
        max_score = group['relevance_score'].max()
        session_count_by_date = group.groupby(group['Date'].dt.date).size().to_dict()
        
        # Get room info
        rooms = group['Location'].unique()
        
        # Get matching focus areas
        focus_area_matches = {}
        if focus_areas:
            for area, keywords in focus_areas.items():
                # Count sessions matching this area
                matches = sum(1 for _, row in group.iterrows() if any(
                    keyword.lower() in ' '.join([str(val) for val in row.values if isinstance(val, str)]).lower()
                    for keyword in keywords
                ))
                if matches > 0:
                    focus_area_matches[area] = matches
        
        # Store symposium data
        symposium_data[symposium] = {
            'total_sessions': total_sessions,
            'avg_score': avg_score,
            'max_score': max_score,
            'sessions_by_date': session_count_by_date,
            'rooms': list(rooms),
            'focus_area_matches': focus_area_matches
        }
    
    # Sort symposiums by average score
    sorted_symposiums = sorted(symposium_data.items(), key=lambda x: x[1]['avg_score'], reverse=True)
    
    return dict(sorted_symposiums)

def export_sessions_to_csv(df, focus_areas=None, min_score=3, output_file=None):
    """
    Export relevant sessions to a CSV file.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Conference data
    focus_areas : dict
        Dictionary mapping focus areas to lists of keywords
    min_score : int
        Minimum relevance score to include sessions
    output_file : str
        Path to save the CSV file
        
    Returns:
    --------
    bool
        True if successful, False otherwise
    """
    if df is None or df.empty:
        print("No data available to export.")
        return False
    
    # Score sessions based on focus areas
    if focus_areas:
        df['relevance_score'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
        # Filter by minimum score
        relevant_df = df[df['relevance_score'] >= min_score].copy()
    else:
        relevant_df = df.copy()
        relevant_df['relevance_score'] = 1
    
    if relevant_df.empty:
        print(f"No sessions with relevance score >= {min_score} found.")
        return False
    
    # Add a column for matched focus areas
    def get_matched_areas(row):
        if not focus_areas:
            return ""
        
        session_text = ' '.join([str(val) for val in row.values if isinstance(val, str)]).lower()
        matched = []
        
        for area, keywords in focus_areas.items():
            if any(kw.lower() in session_text for kw in keywords):
                matched.append(area)
        
        return ", ".join(matched)
    
    relevant_df['matched_areas'] = relevant_df.apply(get_matched_areas, axis=1)
    
    # Sort by date, start time, and relevance score
    sorted_df = relevant_df.sort_values(['Date', 'Start', 'relevance_score'], ascending=[True, True, False])
    
    # Select columns for export
    export_columns = ['Date', 'Start', 'End', 'Location', 'Symposium', 'Session', 'Title', 
                      'Speaker', 'SpeakerAffiliation', 'Type', 'relevance_score', 'matched_areas']
    
    # Make sure all columns exist
    actual_columns = [col for col in export_columns if col in sorted_df.columns]
    
    # If output file not specified, create a default name
    if output_file is None:
        output_file = "tms_sessions_export.csv"
    
    # Export to CSV
    try:
        sorted_df[actual_columns].to_csv(output_file, index=False)
        print(f"Successfully exported {len(sorted_df)} sessions to {output_file}")
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def create_interactive_calendar(df, min_score=0, focus_areas=None, title="Conference Schedule", 
                               symposium_view=False, selected_areas=None):
    """
    Create an interactive Plotly visualization of the conference schedule.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Conference data
    min_score : int
        Minimum relevance score to include sessions
    focus_areas : dict
        Dictionary mapping focus areas to lists of keywords
    title : str
        Title for the visualization
    symposium_view : bool
        If True, group sessions by symposium instead of showing all individual sessions
    selected_areas : list
        List of specific focus areas to display (if None, show all)
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        Interactive Plotly figure
    """
    if df is None or df.empty:
        print("No data available to visualize.")
        return None
    
    # Convert date strings to datetime if needed
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Get unique dates for subplots
    unique_dates = sorted(df['Date'].dt.date.unique())
    
    if not unique_dates:
        print("No valid dates found in the schedule.")
        return None
    
    # Score sessions based on focus areas
    if focus_areas:
        df['relevance_score'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
        # Filter by minimum score
        if min_score > 0:
            df = df[df['relevance_score'] >= min_score].copy()
    else:
        # If no focus areas, just include all sessions
        df['relevance_score'] = 1
    
    if df.empty:
        print(f"No sessions with relevance score >= {min_score} found.")
        return None
    
    # Fix any time issues - ensure start time is before end time
    def fix_times(row):
        start_float = time_to_float(row['Start'])
        end_float = time_to_float(row['End'])
        
        # If end time appears to be before start time (possible AM/PM confusion)
        if end_float < start_float:
            # This likely means end time is PM when it's a small number like 1:00 or 2:00
            # Add 12 hours to end time to correct this
            print(f"Fixed reversed time: {row['Start']} - {row['End']} → {row['Start']} - {float_to_time(end_float + 12)} for session: {row['Title']}")
            end_float += 12.0
            # Store the fixed float value to be used later
            row['end_time_float'] = end_float
        else:
            row['end_time_float'] = end_float
            
        row['start_time_float'] = start_float
        return row
    
    # Helper function to convert float time back to string for display
    def float_to_time(float_time):
        hours = int(float_time)
        minutes = int((float_time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    
    # Apply time fixing to all rows
    df = df.apply(fix_times, axis=1)
    
    # Create a color map for focus areas
    if focus_areas:
        focus_area_colors = get_focus_area_colors(focus_areas)
    
    # Filter by selected focus areas if specified
    if selected_areas and focus_areas:
        # Keep track of session ids that match any of the selected areas
        selected_sessions = set()
        for _, row in df.iterrows():
            session_text = ' '.join([str(val) for val in row.values if isinstance(val, str)])
            for area in selected_areas:
                if area in focus_areas:
                    keywords = focus_areas[area]
                    if any(keyword.lower() in session_text.lower() for keyword in keywords):
                        selected_sessions.add(row.name)
                        break
        
        if selected_sessions:
            df = df.loc[list(selected_sessions)]
        else:
            print(f"No sessions match the selected focus areas.")
            return None
    
    # Create subplots - one per day
    fig = make_subplots(
        rows=1, 
        cols=len(unique_dates),
        subplot_titles=[datetime.combine(date, datetime.min.time()).strftime('%A<br>%B %d, %Y') 
                       for date in unique_dates],
        shared_yaxes=True,
        horizontal_spacing=0.02
    )
    
    # Time range for y-axis
    time_min, time_max = 7.0, 19.0  # 7:00 AM to 7:00 PM
    
    # SYMPOSIUM VIEW - Group by symposium
    if symposium_view:
        # Keep track of which areas/symposiums have been added to the legend
        in_legend = set()
        
        # Process each day
        for i, date in enumerate(unique_dates):
            day_data = df[df['Date'].dt.date == date]
            if day_data.empty:
                continue
            
            # Group by symposium and room
            symposium_groups = day_data.groupby(['Symposium', 'Location'])
            
            # Get unique rooms
            unique_rooms = sorted(day_data['Location'].unique())
            room_dict = {room: idx for idx, room in enumerate(unique_rooms)}
            
            # For each symposium group
            for (symposium, room), group in symposium_groups:
                try:
                    # Skip if symposium is empty
                    if not symposium or pd.isna(symposium):
                        continue
                    
                    # Get time range for this symposium in this room
                    start_times = [row['start_time_float'] for _, row in group.iterrows()]
                    end_times = [row['end_time_float'] for _, row in group.iterrows()]
                    
                    min_start = min(start_times)
                    max_end = max(end_times)
                    
                    # Get room position
                    room_pos = room_dict.get(room, 0)
                    
                    # Find which focus areas match this symposium
                    matching_areas = []
                    if focus_areas:
                        # Concatenate all text in this symposium
                        symposium_text = ' '.join([str(val) for row in group.itertuples() 
                                                 for val in row if isinstance(val, str)])
                        
                        # Check which areas match
                        for area, keywords in focus_areas.items():
                            if any(keyword.lower() in symposium_text.lower() for keyword in keywords):
                                matching_areas.append(area)
                    
                    # If selected areas were specified, only use matching ones
                    if selected_areas:
                        matching_areas = [area for area in matching_areas if area in selected_areas]
                    
                    # If no matching areas, or no focus areas defined, use a default color
                    if not matching_areas:
                        color = 'rgba(100,100,100,0.6)'  # Default gray
                        name = "Other Symposiums"
                    else:
                        # Use color of first matching area
                        color = focus_area_colors[matching_areas[0]]
                        name = matching_areas[0]
                    
                    # Create a wider rectangle for the symposium block with better spacing
                    rect_x = [room_pos - 0.4, room_pos + 0.4, room_pos + 0.4, room_pos - 0.4, room_pos - 0.4]
                    rect_y = [min_start, min_start, max_end, max_end, min_start]
                    
                    # Count sessions and get avg score
                    session_count = len(group)
                    avg_score = group['relevance_score'].mean()
                    max_score = group['relevance_score'].max()
                    
                    # Format scores
                    score_text = f"<br><b>Sessions:</b> {session_count}<br><b>Avg Score:</b> {avg_score:.1f}<br><b>Max Score:</b> {max_score:.1f}"
                    
                    # Create hover text that summarizes the symposium
                    hover_text = f"<b>Symposium:</b> {symposium}<br>" + \
                                f"<b>Time:</b> {group['Start'].iloc[0]} - {group['End'].iloc[-1]}<br>" + \
                                f"<b>Room:</b> {room}" + \
                                score_text + \
                                f"<br><b>Focus Areas:</b> {', '.join(matching_areas)}" + \
                                f"<br><br><b>Top Sessions:</b>"
                    
                    # Add top 3 sessions by relevance score
                    top_sessions = group.sort_values('relevance_score', ascending=False).head(3)
                    for _, session in top_sessions.iterrows():
                        hover_text += f"<br>• <i>{session['Title']}</i> ({session['relevance_score']:.1f})"
                    
                    # Add rectangle for this symposium
                    legend_trace = name not in in_legend
                    fig.add_trace(
                        go.Scatter(
                            x=rect_x,
                            y=rect_y,
                            fill="toself",
                            fillcolor=color,
                            line=dict(color="black", width=1),
                            opacity=0.7,
                            mode="lines",
                            hoverinfo="text",
                            hoveron="fills",
                            text=hover_text,
                            name=name,
                            showlegend=bool(legend_trace),
                            legendgroup=name,
                            marker=dict(color=color) if legend_trace else dict(),
                        ),
                        row=1, col=i+1
                    )
                    
                    # Add text label in middle of symposium block
                    # Truncate symposium name for better display
                    symp_display = symposium
                    if len(symp_display) > 25:
                        words = symp_display.split()
                        if len(words) > 3:
                            symp_display = ' '.join(words[:3]) + '...'
                        else:
                            symp_display = symp_display[:25] + '...'
                    
                    fig.add_trace(
                        go.Scatter(
                            x=[room_pos],
                            y=[(min_start + max_end) / 2],
                            mode="text",
                            text=symp_display,
                            textposition="middle center",
                            textfont=dict(
                                size=10,
                                color="black",
                                family="Arial, sans-serif"
                            ),
                            marker=dict(opacity=0),
                            hoverinfo="none",
                            showlegend=False,
                        ),
                        row=1, col=i+1
                    )
                    
                    # Add to legend tracker
                    if legend_trace:
                        in_legend.add(name)
                    
                except Exception as e:
                    print(f"Error processing symposium {symposium}: {e}")
                    continue
    
    # STANDARD VIEW - Show individual sessions
    else:
        # Keep track of which areas have been added to the legend
        area_in_legend = set()
        
        # Process each focus area
        if focus_areas:
            # Group sessions by focus area for proper legend filtering
            for area_name, keywords in focus_areas.items():
                # Skip if not in selected areas
                if selected_areas and area_name not in selected_areas:
                    continue
                    
                # Get color for this area
                color = focus_area_colors[area_name]
                
                # For each day
                for i, date in enumerate(unique_dates):
                    day_data = df[df['Date'].dt.date == date]
                    if day_data.empty:
                        continue
                    
                    # Get unique rooms with increased spacing
                    unique_rooms = sorted(day_data['Location'].unique())
                    room_dict = {room: idx*1.5 for idx, room in enumerate(unique_rooms)}  # Multiply by 1.5 for spacing
                    
                    # Filter sessions for this area
                    area_sessions = []
                    for _, session in day_data.iterrows():
                        session_text = ' '.join([str(val) for val in session.values if isinstance(val, str)])
                        # Check if this session matches any keywords for this area
                        if any(keyword.lower() in session_text.lower() for keyword in keywords):
                            area_sessions.append(session)
                    
                    # Skip if no sessions for this area on this day
                    if not area_sessions:
                        continue
                    
                    # For each session on this day
                    for session in area_sessions:
                        try:
                            # Use the corrected time values
                            start_float = session['start_time_float']
                            end_float = session['end_time_float']
                            
                            # Check duration
                            duration = end_float - start_float
                            if duration <= 0:
                                print(f"Warning: Invalid duration for {session['Title']}: {duration}")
                                continue
                            
                            # Get room position
                            room = session['Location']
                            room_pos = room_dict.get(room, 0)
                            
                            # Make rectangles wider for better text display - with improved spacing
                            rect_x = [room_pos - 0.4, room_pos + 0.4, room_pos + 0.4, room_pos - 0.4, room_pos - 0.4]
                            rect_y = [start_float, start_float, end_float, end_float, start_float]
                            
                            # Prepare hover text
                            speaker = f"<br><b>Speaker:</b> {session['Speaker']}" if 'Speaker' in session and pd.notna(session['Speaker']) else ""
                            affiliation = f"<br><b>Affiliation:</b> {session['SpeakerAffiliation']}" if 'SpeakerAffiliation' in session and pd.notna(session['SpeakerAffiliation']) else ""
                            
                            # Include symposium information
                            symposium = f"<br><b>Symposium:</b> {session['Symposium']}" if 'Symposium' in session and pd.notna(session['Symposium']) else ""
                            
                            # Wrap description text for better readability
                            description = ""
                            if 'Description' in session and pd.notna(session['Description']):
                                description = f"<br><br>{wrap_text(session['Description'], width=60)}"
                            
                            score_text = f"<br><b>Relevance Score:</b> {session['relevance_score']}" if 'relevance_score' in session else ""
                            
                            # Format matching keywords
                            session_text = ' '.join([str(val) for val in session.values if isinstance(val, str)])
                            matches = [kw for kw in keywords if kw.lower() in session_text.lower()]
                            keywords_matched = f"<br><b>Matching Keywords:</b> <br><b>{area_name}:</b> {', '.join(matches)}" if matches else ""
                            
                            hover_text = f"<b>{session['Title']}</b><br>" + \
                                        f"<b>Time:</b> {session['Start']} - {session['End']}<br>" + \
                                        f"<b>Room:</b> {session['Location']}" + \
                                        symposium + \
                                        speaker + \
                                        affiliation + \
                                        score_text + \
                                        keywords_matched + \
                                        description
                            
                            # Add rectangle trace for this session
                            legend_trace = area_name not in area_in_legend
                            fig.add_trace(
                                go.Scatter(
                                    x=rect_x,
                                    y=rect_y,
                                    fill="toself",
                                    fillcolor=color,
                                    line=dict(color="black", width=1),
                                    opacity=0.7,
                                    mode="lines",
                                    hoverinfo="text",
                                    hoveron="fills",
                                    text=hover_text,
                                    name=area_name,
                                    showlegend=bool(legend_trace),
                                    legendgroup=area_name,
                                    # Fix for legend showing half-colored items
                                    marker=dict(color=color) if legend_trace else dict(),
                                ),
                                row=1, col=i+1
                            )
                            
                            # Only add text labels for sessions of sufficient duration (15+ min)
                            # This significantly reduces text clutter
                            if duration >= 0.25:  # 15 min = 0.25 hour
                                # Add text label in middle of session block with improved readability
                                title_text = session['Title']
                                if len(title_text) > 25:
                                    title_text = title_text[:25] + "..."
                                
                                fig.add_trace(
                                    go.Scatter(
                                        x=[room_pos],
                                        y=[(start_float + end_float) / 2],
                                        mode="text",
                                        text=title_text,
                                        textposition="middle center",
                                        textfont=dict(
                                            size=9, 
                                            color="black",
                                            family="Arial, sans-serif"
                                        ),
                                        # Add background to text for better contrast
                                        marker=dict(
                                            opacity=0
                                        ),
                                        hoverinfo="none",
                                        showlegend=False,
                                        legendgroup=area_name,
                                    ),
                                    row=1, col=i+1
                                )
                            
                            # Then after adding the trace if it was shown in the legend, update the tracking set:
                            if area_name not in area_in_legend:
                                area_in_legend.add(area_name)
                            
                        except Exception as e:
                            print(f"Error processing session: {e}")
                            continue
            else:
                # If no focus areas, just show all sessions in one color
                color = 'rgba(70,130,180,0.7)'  # Steel blue
                
                # For each day
                for i, date in enumerate(unique_dates):
                    day_data = df[df['Date'].dt.date == date]
                    if day_data.empty:
                        continue
                    
                    # Get unique rooms
                    unique_rooms = sorted(day_data['Location'].unique())
                    room_dict = {room: idx*1.5 for idx, room in enumerate(unique_rooms)}  # Multiply by 1.5 for spacing
                    
                    # Process each session
                    for _, session in day_data.iterrows():
                        try:
                            # Use the corrected time values
                            start_float = session['start_time_float']
                            end_float = session['end_time_float']
                            
                            # Check duration
                            duration = end_float - start_float
                            if duration <= 0:
                                print(f"Warning: Invalid duration for {session['Title']}: {duration}")
                                continue
                            
                            # Get room position
                            room = session['Location']
                            room_pos = room_dict.get(room, 0)
                            
                            # Create a rectangle (calendar block) for this session - with improved spacing
                            rect_x = [room_pos - 0.4, room_pos + 0.4, room_pos + 0.4, room_pos - 0.4, room_pos - 0.4]
                            rect_y = [start_float, start_float, end_float, end_float, start_float]
                            
                            # Prepare hover text
                            speaker = f"<br><b>Speaker:</b> {session['Speaker']}" if 'Speaker' in session and pd.notna(session['Speaker']) else ""
                            affiliation = f"<br><b>Affiliation:</b> {session['SpeakerAffiliation']}" if 'SpeakerAffiliation' in session and pd.notna(session['SpeakerAffiliation']) else ""
                            
                            # Include symposium info
                            symposium = f"<br><b>Symposium:</b> {session['Symposium']}" if 'Symposium' in session and pd.notna(session['Symposium']) else ""
                            
                            # Wrap description text for better readability
                            description = ""
                            if 'Description' in session and pd.notna(session['Description']):
                                description = f"<br><br>{wrap_text(session['Description'], width=60)}"
                            
                            hover_text = f"<b>{session['Title']}</b><br>" + \
                                        f"<b>Time:</b> {session['Start']} - {session['End']}<br>" + \
                                        f"<b>Room:</b> {session['Location']}" + \
                                        symposium + \
                                        speaker + \
                                        affiliation + \
                                        description
                            
                            # Add rectangle trace for this session
                            fig.add_trace(
                                go.Scatter(
                                    x=rect_x,
                                    y=rect_y,
                                    fill="toself",
                                    fillcolor=color,
                                    line=dict(color="black", width=1),
                                    opacity=0.7,
                                    mode="lines",
                                    hoverinfo="text",
                                    hoveron="fills",
                                    text=hover_text,
                                    name='Sessions',
                                    showlegend=bool(i==0 and _==day_data.index[0]),  # Convert to Python bool
                                ),
                                row=1, col=i+1
                            )
                            
                            # Only add text for sessions with sufficient duration
                            if duration >= 0.25:  # 15 min = 0.25 hour
                                # Add text label in middle of rectangle
                                title_text = session['Title']
                                if len(title_text) > 25:
                                    title_text = title_text[:25] + "..."
                                
                                fig.add_trace(
                                    go.Scatter(
                                        x=[room_pos],
                                        y=[(start_float + end_float) / 2],
                                        mode="text",
                                        text=title_text,
                                        textposition="middle center",
                                        textfont=dict(
                                            size=9, 
                                            color="black",
                                            family="Arial, sans-serif"
                                        ),
                                        marker=dict(
                                            opacity=0
                                        ),
                                        hoverinfo="none",
                                        showlegend=False,
                                    ),
                                    row=1, col=i+1
                                )
                        
                        except Exception as e:
                            print(f"Error processing session: {e}")
                            continue
    
    # Configure layout
    fig.update_layout(
        title=dict(
            text=title + (" (Symposium View)" if symposium_view else ""),
            font=dict(size=24, family="Arial, sans-serif"),
            x=0.5,
            xanchor="center"
        ),
        height=800,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12, family="Arial, sans-serif"),
            # Make legend items larger and more clickable
            itemsizing="constant",
            itemwidth=30
        ),
        margin=dict(t=80, b=100, l=50, r=50),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial, sans-serif"
        ),
        hovermode="closest",
        # Set overall font
        font=dict(family="Arial, sans-serif"),
        # Use white background for better printing
        paper_bgcolor='white',
        plot_bgcolor='rgba(240,240,240,0.5)'
    )
    
    # Configure axes
    for i in range(1, len(unique_dates) + 1):
        # X-axis (rooms)
        day_data = df[df['Date'].dt.date == unique_dates[i-1]]
        if day_data.empty:
            continue
            
        unique_rooms = sorted(day_data['Location'].unique())
        
        fig.update_xaxes(
            tickvals=list(range(len(unique_rooms)*3//2))[::3] if not symposium_view else list(range(len(unique_rooms))),
            ticktext=unique_rooms,
            tickangle=45,
            title_text="Room",
            row=1, col=i
        )
        
        # Y-axis (time)
        hour_ticks = list(range(int(time_min), int(time_max) + 1))
        fig.update_yaxes(
            tickvals=hour_ticks,
            ticktext=[f"{h:02d}:00" for h in hour_ticks],
            range=[time_max, time_min],  # Reversed for top-to-bottom
            title_text="Time" if i == 1 else None,
            row=1, col=i
        )
        
        # Add grid lines
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray", row=1, col=i)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgray", row=1, col=i)
    
    # Add buttons for interactive features
    updatemenus = [
        # Zoom controls
        dict(
            type="buttons",
            direction="left",
            buttons=[
                dict(label="Reset View",
                     method="relayout",
                     args=[{"yaxis.range": [time_max, time_min]}]),
                dict(label="Morning",
                     method="relayout",
                     args=[{"yaxis.range": [13, 7]}]),
                dict(label="Afternoon",
                     method="relayout",
                     args=[{"yaxis.range": [19, 13]}])
            ],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
    
    fig.update_layout(updatemenus=updatemenus)
    
    # Add annotations for instructions
    fig.add_annotation(
        text="👆 Hover over sessions for details | Click on legend items to filter",
        xref="paper", yref="paper",
        x=0.5, y=1.06,
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig

def save_interactive_calendar(df=None, data_file=None, profile=None, interests_file=None, 
                            min_score=3, output_file=None, title=None, gen_csv=False, gen_symposium=False,
                            symposium_view=False, selected_areas=None):
    """
    Generate and save an interactive calendar visualization of the conference schedule.
    
    Parameters:
    -----------
    df : pandas DataFrame, optional
        Pre-loaded conference data (default: None, will load from data_file)
    data_file : str, optional
        Path to the Excel data file (default: None, will auto-detect)
    profile : str, optional
        Name of a predefined research profile (default: None)
    interests_file : str, optional
        Path to a JSON file with custom interests (default: None)
    min_score : int, optional
        Minimum relevance score to include sessions (default: 3)
    output_file : str, optional
        Path to save the HTML file (default: derived from profile/interests)
    title : str, optional
        Custom title for the visualization (default: derived from profile/interests)
    gen_csv : bool, optional
        Whether to generate a CSV export of sessions (default: False)
    gen_symposium : bool, optional
        Whether to generate a symposium report (default: False)
    symposium_view : bool, optional
        If True, group sessions by symposium instead of showing individual sessions (default: False)
    selected_areas : list, optional
        List of specific focus areas to display (default: None, show all)
    
    Returns:
    --------
    bool
        True if successful, False otherwise
    """
    try:
        # Import RESEARCH_PROFILES from tms_planner
        from tms_planner import RESEARCH_PROFILES
        
        # Load data if not provided
        if df is None:
            if data_file is None:
                data_file = find_data_file()
                if not data_file:
                    print("Error: Could not find TMS data file.")
                    return False
            
            print(f"Loading data from: {data_file}")
            from analyze_tms import load_conference_data
            df = load_conference_data(data_file)
            
            if df is None:
                print("Error: Failed to load conference data.")
                return False
        
        # Get user interests
        user_interests = None
        user_weights = None
        profile_name = None
        
        if profile and profile in RESEARCH_PROFILES:
            profile_name = profile
            print(f"Using predefined '{profile}' profile")
            user_interests = RESEARCH_PROFILES[profile]["interests"]
            user_weights = RESEARCH_PROFILES[profile].get("weights")
            
            # Set default title if not specified
            if title is None:
                title = f"TMS 2025 - {profile.title()} Focus Areas"
                
            # Set default output file if not specified
            if output_file is None:
                view_suffix = "_symposiums" if symposium_view else ""
                output_file = f"{profile}_calendar{view_suffix}.html"
                
        elif interests_file:
            profile_name = Path(interests_file).stem
            print(f"Loading custom interests from: {interests_file}")
            try:
                with open(interests_file, 'r') as f:
                    data = json.load(f)
                
                if "interests" in data:
                    user_interests = data["interests"]
                    user_weights = data.get("weights")
                    
                    # Set default title if not specified
                    if title is None:
                        title = f"TMS 2025 - Custom Interests"
                        
                    # Set default output file if not specified
                    if output_file is None:
                        base_name = Path(interests_file).stem
                        view_suffix = "_symposiums" if symposium_view else ""
                        output_file = f"{base_name}_calendar{view_suffix}.html"
                else:
                    print("Error: Invalid interests file format.")
                    return False
            except Exception as e:
                print(f"Error loading interests file: {e}")
                return False
        else:
            print("Error: Either profile or interests file must be specified.")
            return False
        
        # Generate CSV if requested
        if gen_csv:
            csv_file = f"{profile_name}_sessions.csv" if profile_name else "sessions_export.csv"
            print(f"Generating CSV export to: {csv_file}")
            export_sessions_to_csv(df, user_interests, min_score, csv_file)
        
        # Generate symposium report if requested
        if gen_symposium:
            symposium_file = f"{profile_name}_symposiums.txt" if profile_name else "symposium_report.txt"
            print(f"Generating symposium report to: {symposium_file}")
            
            symposium_data = generate_symposium_report(df, user_interests, min_score)
            
            if symposium_data:
                with open(symposium_file, 'w') as f:
                    f.write(f"TMS 2025 SYMPOSIUM RECOMMENDATIONS\n")
                    f.write(f"Based on {profile_name if profile_name else 'custom'} interests\n")
                    f.write(f"Minimum score: {min_score}\n\n")
                    
                    f.write("TOP RECOMMENDED SYMPOSIUMS:\n")
                    f.write("--------------------------\n\n")
                    
                    for i, (symposium, data) in enumerate(symposium_data.items(), 1):
                        if i > 10:  # Top 10 symposiums
                            break
                            
                        f.write(f"{i}. {symposium}\n")
                        f.write(f"   Average relevance score: {data['avg_score']:.2f}\n")
                        f.write(f"   Number of relevant sessions: {data['total_sessions']}\n")
                        
                        if data['focus_area_matches']:
                            f.write(f"   Matching focus areas:\n")
                            for area, count in data['focus_area_matches'].items():
                                f.write(f"     - {area}: {count} sessions\n")
                        
                        f.write(f"   Rooms: {', '.join(data['rooms'])}\n")
                        f.write(f"   Sessions by date:\n")
                        for date, count in data['sessions_by_date'].items():
                            f.write(f"     - {date.strftime('%A, %B %d')}: {count} sessions\n")
                        
                        f.write("\n")
                
                print(f"Symposium report saved to {symposium_file}")
        
        # Generate visualization
        print(f"Generating interactive visualization with minimum score: {min_score}" + 
              (", symposium view" if symposium_view else ""))
        
        fig = create_interactive_calendar(
            df, 
            min_score=min_score, 
            focus_areas=user_interests, 
            title=title,
            symposium_view=symposium_view,
            selected_areas=selected_areas
        )
        
        if fig is None:
            print("Error: Failed to generate the visualization.")
            return False
        
        # Save the figure to HTML
        print(f"Saving interactive visualization to: {output_file}")
        pio.write_html(fig, output_file, auto_open=False)
        print(f"Successfully saved to {output_file}")
        
        return True
    
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return False

def main():
    """Command-line interface for creating interactive calendar visualizations"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate interactive calendar visualizations for TMS conference")
    
    # Input data options
    parser.add_argument("--file", "-f", help="Path to the TMS Excel file (auto-detected if not specified)")
    
    # Interests options - must choose one
    interests_group = parser.add_argument_group("Interests options (choose one)")
    profile_group = interests_group.add_mutually_exclusive_group(required=True)
    profile_group.add_argument("--profile", "-p", help="Use a predefined research profile")
    profile_group.add_argument("--interests", "-i", help="Path to a JSON file with custom interests")
    
    # Visualization options
    parser.add_argument("--min-score", "-m", type=int, default=3,
                      help="Minimum relevance score to include sessions (default: 3)")
    parser.add_argument("--output", "-o", default=None,
                      help="Path to save the HTML visualization (default: derived from profile/interests)")
    parser.add_argument("--title", "-t", default=None,
                      help="Custom title for the visualization")
    parser.add_argument("--open", action="store_true",
                      help="Automatically open the visualization in a browser")
    parser.add_argument("--csv", action="store_true",
                      help="Generate a CSV export of matched sessions")
    parser.add_argument("--symposium", action="store_true",
                      help="Generate a report of recommended symposiums")
    parser.add_argument("--symposium-view", action="store_true",
                      help="Group sessions by symposium in the visualization")
    parser.add_argument("--areas", nargs="+", 
                      help="Specific focus areas to display (space-separated)")
    
    args = parser.parse_args()
    
    # Generate and save the visualization
    success = save_interactive_calendar(
        data_file=args.file,
        profile=args.profile,
        interests_file=args.interests,
        min_score=args.min_score,
        output_file=args.output,
        title=args.title,
        gen_csv=args.csv,
        gen_symposium=args.symposium,
        symposium_view=args.symposium_view,
        selected_areas=args.areas
    )
    
    # Open the visualization if requested
    if success and args.open:
        import webbrowser
        output_file = args.output
        if output_file is None:
            view_suffix = "_symposiums" if args.symposium_view else ""
            if args.profile:
                output_file = f"{args.profile}_calendar{view_suffix}.html"
            elif args.interests:
                base_name = Path(args.interests).stem
                output_file = f"{base_name}_calendar{view_suffix}.html"
        
        print(f"Opening visualization in browser: {output_file}")
        webbrowser.open_new_tab(f"file://{os.path.abspath(output_file)}")

if __name__ == "__main__":
    main() 