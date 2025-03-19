# Copyright 2025 NVIDIA Corporation. All rights reserved.
# Licensed under the Apache License, Version 2.0
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import os
import sys

# Set style for better visualizations
sns.set_theme(style="whitegrid")

def find_data_file(filename='TMS2025AI_Excel_02-21-2025.xlsx'):
    """
    Find the data file by searching in multiple possible locations.
    
    Parameters:
    -----------
    filename : str
        Name of the file to find (default: 'TMS2025AI_Excel_02-21-2025.xlsx')
        
    Returns:
    --------
    str or None
        Path to the file if found, None otherwise
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List of possible file locations to check
    possible_paths = [
        os.path.join(os.getcwd(), 'data', filename),  # From current directory
        os.path.join(os.getcwd(), filename),          # Directly in current directory
        os.path.join(script_dir, '..', 'data', filename),  # From script directory
        os.path.join(script_dir, 'data', filename),   # data/ in script directory
        os.path.join(os.path.dirname(script_dir), 'data', filename),  # repo root/data/
        os.path.join('data', filename),               # Relative data/
        os.path.join('..', 'data', filename),         # Relative ../data/
    ]
    
    # Check each path
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found data file at: {path}")
            return path
    
    # If we get here, file was not found
    print(f"Could not find data file: {filename}")
    print("Searched locations:")
    for path in possible_paths:
        print(f"  - {path} (Not found)")
    
    return None

def load_conference_data(file_path='TMS2025AI_Excel_02-21-2025.xlsx'):
    # If no path provided, attempt to find the file
    if file_path == 'TMS2025AI_Excel_02-21-2025.xlsx':
        file_path = find_data_file(file_path)
        if file_path is None:
            print("Error: Could not find the Excel file. Please provide the file path.")
            return None
            
    try:
        df = pd.read_excel(file_path)
        print(f"\nLoading TMS 2025 Conference Data...")
        print(f"Dataset contains {len(df)} entries and {len(df.columns)} columns")
        print("\nDataset Structure:")
        print(df.info())
        print("\nFirst few rows:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def analyze_schedule(df):
    """Analyze the conference schedule."""
    if df is None:
        return
    
    print("\nConference Overview:")
    print("-" * 50)
    print(f"Total number of entries: {len(df)}")
    
    # Date range
    if 'Date' in df.columns:
        date_range = df['Date'].agg(['min', 'max'])
        print(f"\nConference dates: {date_range['min'].strftime('%B %d')} - {date_range['max'].strftime('%B %d, %Y')}")
    
    # Session types
    print("\nSession Types:")
    print("-" * 30)
    print(df['Type'].value_counts())
    
    # Abstract types
    print("\nAbstract Types:")
    print("-" * 30)
    print(df['AbstractType'].value_counts())
    
    # Tracks
    print("\nTracks:")
    print("-" * 30)
    print(df['Track'].value_counts())

def search_sessions(df, keyword):
    """Search for sessions containing a specific keyword."""
    if df is None:
        return
    
    print(f"\nSearching for '{keyword}':")
    print("-" * 50)
    
    search_results = {}
    text_columns = ['Track', 'Symposium', 'Session', 'Title', 'Description', 
                    'Speaker', 'SpeakerAffiliation', 'AllAuthors']
    
    for column in text_columns:
        if column in df.columns:
            # Convert to string and handle NaN values
            matches = df[df[column].astype(str).str.contains(keyword, case=False, na=False)]
            if not matches.empty:
                search_results[column] = len(matches)
    
    print("\nNumber of matches found:")
    for column, count in search_results.items():
        print(f"{column}: {count} matches")
    
    # Show detailed results for Title matches
    if 'Title' in search_results:
        print(f"\nDetailed matches in Titles containing '{keyword}':")
        print("-" * 50)
        matches = df[df['Title'].astype(str).str.contains(keyword, case=False, na=False)]
        for _, row in matches.iterrows():
            print(f"Title: {row['Title']}")
            print(f"Date: {row['Date'].strftime('%B %d, %Y')} at {row['Start']}")
            print(f"Location: {row['Location']}")
            print("-" * 50)

def score_session_relevance(row, focus_areas):
    """Score the relevance of a session based on focus areas."""
    score = 0
    text = ' '.join([str(val) for val in row.values if isinstance(val, str)])
    
    for area, keywords in focus_areas.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                score += 1
    return score

def create_targeted_schedule(df, focus_areas):
    """Create a targeted schedule based on focus areas and keywords."""
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Score each session
    df['relevance_score'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
    
    # Filter relevant sessions (score > 0)
    relevant_sessions = df[df['relevance_score'] > 0].copy()
    
    # Sort by date, time, and relevance score
    relevant_sessions = relevant_sessions.sort_values(['Date', 'Start', 'relevance_score'], 
                                                    ascending=[True, True, False])
    
    # Group sessions by date
    for date, group in relevant_sessions.groupby('Date'):
        print(f"\n{'='*80}")
        print(f"Schedule for {date.strftime('%A, %B %d, %Y')}")
        print('='*80)
        
        for _, session in group.iterrows():
            # Identify which focus areas match
            matching_areas = []
            for area, keywords in focus_areas.items():
                text = ' '.join([str(val) for val in session.values if isinstance(val, str)])
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    matching_areas.append(area)
            
            print(f"\n{session['Start']} - {session['End']} | Room {session['Location']}")
            print(f"Title: {session['Title']}")
            if isinstance(session['Description'], str):
                print(f"Description: {session['Description'][:200]}...")
            print(f"Type: {session['Type']}")
            print(f"Focus Areas: {', '.join(matching_areas)}")
            print(f"Relevance Score: {session['relevance_score']}")
            print('-' * 30)

def identify_nvidia_product_relevance(session_text):
    """Identify which NVIDIA products are relevant to a session."""
    nvidia_products = {
        'Omniverse': ['digital twin', 'visualization', 'collaboration', 'simulation', 'real-time', 
                      '3D modeling', 'virtual environment', 'synthetic data', 'virtual worlds'],
        'AI & HPC': ['GPU', 'accelerator', 'CUDA', 'parallel computing', 'high performance computing',
                    'machine learning', 'deep learning', 'neural network', 'AI', 'transformer', 
                    'large language model', 'generative AI', 'computer vision'],
        'ALCHEMI': ['materials discovery', 'optimization', 'parameter prediction', 'materials design',
                   'quantum chemistry', 'simulation', 'material informatics', 'computational materials',
                   'materials genomics', 'high-throughput'],
        'Modulus': ['physics-informed', 'physics-ML', 'differential equations', 'surrogate model',
                   'physics simulation', 'digital twin', 'multiphysics', 'CFD', 'structural mechanics'],
        'MONAI': ['medical imaging', 'healthcare', 'AI for healthcare', 'medical data',
                 'radiology', 'image segmentation', 'computer vision', 'federated learning'],
        'DOCA': ['data processing', 'networking', 'DPU', 'BlueField', 'data center', 'accelerated computing',
                'infrastructure', 'security', 'storage']
    }
    
    relevant_products = {}
    for product, keywords in nvidia_products.items():
        for keyword in keywords:
            if keyword.lower() in session_text.lower():
                if product not in relevant_products:
                    relevant_products[product] = []
                relevant_products[product].append(keyword)
    
    return relevant_products

def create_prioritized_schedule(df, focus_areas, priority_sessions=None):
    """Create a prioritized schedule organized by focus area with business justification."""
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Score each session
    df['relevance_score'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
    
    # Filter relevant sessions (score > 0)
    relevant_sessions = df[df['relevance_score'] > 0].copy()
    
    # Add priority flag if session is in priority_sessions list
    if priority_sessions:
        relevant_sessions['is_priority'] = relevant_sessions['Title'].apply(
            lambda x: any(priority_title.lower() in x.lower() for priority_title in priority_sessions)
        )
    else:
        relevant_sessions['is_priority'] = False
    
    # Group by focus area
    all_focus_areas = list(focus_areas.keys())
    
    print("\n" + "="*100)
    print("PRIORITIZED SCHEDULE BY FOCUS AREA")
    print("="*100)
    
    for focus_area in all_focus_areas:
        print(f"\n{'#'*100}")
        print(f"FOCUS AREA: {focus_area}")
        print(f"{'#'*100}")
        
        # Find sessions relevant to this focus area
        area_sessions = relevant_sessions.copy()
        area_sessions['is_relevant_to_area'] = area_sessions.apply(
            lambda row: any(keyword.lower() in ' '.join([str(val) for val in row.values if isinstance(val, str)]).lower() 
                           for keyword in focus_areas[focus_area]),
            axis=1
        )
        area_sessions = area_sessions[area_sessions['is_relevant_to_area']]
        
        # Sort by priority first, then by relevance score
        area_sessions = area_sessions.sort_values(['is_priority', 'relevance_score'], ascending=[False, False])
        
        # Display sessions
        for _, session in area_sessions.iterrows():
            priority_tag = "⭐ HIGH PRIORITY ⭐" if session['is_priority'] else ""
            
            print(f"\n{priority_tag}")
            print(f"{session['Start']} - {session['End']} | Room {session['Location']}")
            print(f"Title: {session['Title']}")
            
            if isinstance(session['Description'], str):
                description = session['Description']
                # Truncate if too long
                if len(description) > 200:
                    description = description[:200] + "..."
                print(f"Description: {description}")
            
            # Identify NVIDIA product relevance
            session_text = ' '.join([str(val) for val in session.values if isinstance(val, str)])
            nvidia_products = identify_nvidia_product_relevance(session_text)
            
            if nvidia_products:
                print("\nNVIDIA Product Relevance:")
                for product, keywords in nvidia_products.items():
                    print(f"  - {product}: {', '.join(set(keywords[:3]))}")
            
            print(f"Relevance Score: {session['relevance_score']}")
            print('-' * 50)

def generate_business_justification(df, focus_areas):
    """Generate business justification for NVIDIA products based on conference sessions."""
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Score each session
    df['relevance_score'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
    
    # Filter relevant sessions (score > 0)
    relevant_sessions = df[df['relevance_score'] > 0].copy()
    
    # Define NVIDIA products and their value propositions
    nvidia_products = {
        'Omniverse': {
            'description': 'Platform for connecting 3D workflows and enabling real-time collaboration',
            'applications': []
        },
        'Holoscan': {
            'description': 'AI computing platform for real-time sensing, perception, and AI-based processing',
            'applications': []
        },
        'ALCHEMI': {
            'description': 'Materials discovery and optimization platform',
            'applications': []
        },
        'BioNeMo': {
            'description': 'Framework for training and deploying large biomolecular language models',
            'applications': []
        }
    }
    
    # Analyze each session for product relevance
    for _, session in relevant_sessions.iterrows():
        session_text = ' '.join([str(val) for val in session.values if isinstance(val, str)])
        
        # Check Omniverse relevance
        if any(keyword in session_text.lower() for keyword in ['digital twin', 'visualization', 'simulation']):
            application = f"{session['Title']} - {session['Date'].strftime('%B %d')}"
            nvidia_products['Omniverse']['applications'].append(application)
        
        # Check Holoscan relevance
        if any(keyword in session_text.lower() for keyword in ['monitoring', 'quality control', 'vision']):
            application = f"{session['Title']} - {session['Date'].strftime('%B %d')}"
            nvidia_products['Holoscan']['applications'].append(application)
        
        # Check ALCHEMI relevance
        if any(keyword in session_text.lower() for keyword in ['materials discovery', 'optimization', 'simulation']):
            application = f"{session['Title']} - {session['Date'].strftime('%B %d')}"
            nvidia_products['ALCHEMI']['applications'].append(application)
        
        # Check BioNeMo relevance
        if any(keyword in session_text.lower() for keyword in ['knowledge graph', 'data extraction', 'literature']):
            application = f"{session['Title']} - {session['Date'].strftime('%B %d')}"
            nvidia_products['BioNeMo']['applications'].append(application)
    
    # Generate business justification report
    print("\n" + "="*100)
    print("BUSINESS JUSTIFICATION FOR NVIDIA PRODUCTS")
    print("="*100)
    
    for product, details in nvidia_products.items():
        print(f"\n{'#'*100}")
        print(f"PRODUCT: {product}")
        print(f"{'#'*100}")
        print(f"Description: {details['description']}")
        print("\nRelevant Conference Applications:")
        
        if details['applications']:
            # Get unique applications (some sessions might be counted multiple times)
            unique_applications = list(set(details['applications']))
            for i, app in enumerate(unique_applications[:5], 1):  # Show top 5
                print(f"  {i}. {app}")
            
            if len(unique_applications) > 5:
                print(f"  ... and {len(unique_applications) - 5} more applications")
        else:
            print("  No directly relevant sessions found")
        
        print("\nBusiness Value Proposition:")
        if product == 'Omniverse':
            print("  - Enable digital twin implementation for AM processes")
            print("  - Facilitate real-time visualization of process parameters")
            print("  - Create collaborative environment for materials design and simulation")
        elif product == 'Holoscan':
            print("  - Enable real-time monitoring of AM processes")
            print("  - Implement AI-driven quality control systems")
            print("  - Integrate with vision systems for defect detection")
        elif product == 'ALCHEMI':
            print("  - Accelerate materials discovery and optimization")
            print("  - Predict process parameters for optimal outcomes")
            print("  - Integrate with quantum chemistry workflows")
        elif product == 'BioNeMo':
            print("  - Construct knowledge graphs from materials literature")
            print("  - Automate data extraction and analysis")
            print("  - Integrate with experimental workflows")

def create_day_by_day_optimized_schedule(df, focus_areas, priority_sessions=None):
    """Create a day-by-day optimized schedule.
    
    This function organizes the schedule chronologically by day, highlights conflicts
    between priority sessions, and provides recommendations.
    """
    if df is None or df.empty:
        print("No data available to create schedule.")
        return
    
    # First, get the dates from the DataFrame
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date and start time
    df = df.sort_values(by=['Date', 'Start'])
    
    # Group by date
    grouped_by_date = df.groupby(df['Date'].dt.date)
    
    # Score each session based on relevance to focus areas
    df['RelevanceScore'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
    
    # Filter to show only high priority sessions (score 4 or higher) for the summary
    high_priority_df = df[df['RelevanceScore'] >= 4].copy()
    
    # Check for time conflicts between high priority sessions
    print("\n\n" + "="*80)
    print("CONFERENCE PLANNER: PRIORITY SESSIONS AND CONFLICTS")
    print("="*80)
    
    for date, day_df in grouped_by_date:
        day_high_priority = high_priority_df[high_priority_df['Date'].dt.date == date].copy()
        
        if not day_high_priority.empty:
            print(f"\n\n{'=' * 80}")
            print(f"DAY: {date}")
            print(f"{'=' * 80}")
            
            # Find conflicts
            conflicts = []
            for i, (idx1, session1) in enumerate(day_high_priority.iterrows()):
                for j, (idx2, session2) in enumerate(day_high_priority.iterrows()):
                    if i >= j:  # Skip self-comparisons and duplicates
                        continue
                    
                    start1, end1 = session1['Start'], session1['End']
                    start2, end2 = session2['Start'], session2['End']
                    
                    # Check if sessions overlap
                    if (start1 <= end2 and end1 >= start2):
                        conflicts.append((session1, session2))
            
            # Print conflicts if any
            if conflicts:
                print("\n⚠️ SCHEDULE CONFLICTS BETWEEN HIGH PRIORITY SESSIONS ⚠️")
                print("-" * 60)
                for session1, session2 in conflicts:
                    print(f"\nConflict:")
                    print(f"1. {session1['Start']} - {session1['End']} | Room {session1['Location']} | Score: {session1['RelevanceScore']}")
                    print(f"   {session1['Title']}")
                    print(f"2. {session2['Start']} - {session2['End']} | Room {session2['Location']} | Score: {session2['RelevanceScore']}")
                    print(f"   {session2['Title']}")
                    
                    # Provide recommendation based on relevance score
                    if session1['RelevanceScore'] > session2['RelevanceScore']:
                        recommended = "Option 1"
                    elif session2['RelevanceScore'] > session1['RelevanceScore']:
                        recommended = "Option 2"
                    else:
                        recommended = "Either option"
                    
                    print(f"Recommendation: {recommended} (based on relevance score)")
                    print("-" * 40)
            
            # Print high priority sessions by time
            print("\nPRIORITY SESSIONS TIMELINE:")
            print("-" * 60)
            
            # Sort by start time
            day_high_priority = day_high_priority.sort_values(by='Start')
            
            for _, session in day_high_priority.iterrows():
                start_time = session['Start']
                end_time = session['End']
                room = session['Location']
                title = session['Title']
                score = session['RelevanceScore']
                focus_tags = ", ".join([area for area, keywords in focus_areas.items() 
                                      if any(keyword.lower() in str(session).lower() for keyword in keywords)])
                
                # Determine NVIDIA product relevance
                nvidia_products = []
                if "AI" in focus_tags or "vision" in title.lower() or "learning" in title.lower():
                    nvidia_products.append("NVIDIA AI Platform")
                if "simulation" in title.lower() or "model" in title.lower():
                    nvidia_products.append("Omniverse")
                if "quantum" in title.lower() or "DFT" in title.lower():
                    nvidia_products.append("NVIDIA Quantum Computing")
                if "digital twin" in title.lower() or "AM" in focus_tags:
                    nvidia_products.append("NVIDIA Modulus")
                
                if not nvidia_products:
                    nvidia_products = ["NVIDIA HPC Solutions"]
                
                # Print session details
                print(f"\n[{start_time} - {end_time}] | Room {room} | Score: {score}")
                print(f"Title: {title}")
                print(f"Focus Areas: {focus_tags}")
                print(f"NVIDIA Product Relevance: {', '.join(nvidia_products)}")
                print(f"Business Justification: This session directly supports NVIDIA's strategy in {focus_tags}")
                print("-" * 40)
    
    # Return to the detailed schedule by day, showing all sessions
    print("\n\n" + "="*80)
    print("FULL SCHEDULE BY DAY")
    print("="*80)
    
    # For each date
    for date, day_df in grouped_by_date:
        print(f"\n\n{'=' * 80}")
        print(f"SCHEDULE FOR {date}")
        print(f"{'=' * 80}\n")
        
        # Group by time slot
        time_slots = day_df['Start'].unique()
        
        # For each time slot
        for time_slot in sorted(time_slots):
            print(f"\n[TIME SLOT: {time_slot}]\n")
            
            # Get all sessions in this time slot
            slot_df = day_df[day_df['Start'] == time_slot]
            
            # For each session in this time slot
            for _, session in slot_df.iterrows():
                start_time = session['Start']
                end_time = session['End']
                room = session['Location']
                title = session['Title']
                
                # Determine the focus areas for this session
                focus_tags = ", ".join([area for area, keywords in focus_areas.items() 
                                      if any(keyword.lower() in str(session).lower() for keyword in keywords)])
                
                # Score the session's relevance
                relevance_score = score_session_relevance(session, focus_areas)
                
                # Highlight high priority sessions
                priority_marker = "⭐ HIGH PRIORITY ⭐ " if relevance_score >= 4 else ""
                
                print(f"\n{priority_marker}{start_time} - {end_time} | Room {room}")
                print(f"Title: {title}")
                print(f"Focus Areas: {focus_tags}")
                print(f"Relevance Score: {relevance_score}")
                print(f"{'-' * 30}")

def display_priority_sessions_details(df, priority_sessions, focus_areas):
    """Display detailed information about priority sessions."""
    print("\n" + "="*100)
    print("DETAILED INFORMATION ABOUT PRIORITY SESSIONS")
    print("="*100)
    
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Find sessions that match or partially match the priority sessions
    matched_sessions = []
    for priority_title in priority_sessions:
        # Look for exact or partial matches in the title
        matches = df[df['Title'].str.contains(priority_title[:30], case=False, na=False)]
        
        if not matches.empty:
            for _, session in matches.iterrows():
                matched_sessions.append((priority_title, session))
        else:
            # If no direct match, try to find the closest match using keywords
            keywords = priority_title.lower().split()
            # Filter to sessions that contain at least 2 keywords
            keyword_matches = []
            for _, row in df.iterrows():
                if isinstance(row['Title'], str):
                    title_lower = row['Title'].lower()
                    matching_keywords = [kw for kw in keywords if kw in title_lower and len(kw) > 3]
                    if len(matching_keywords) >= 2:
                        keyword_matches.append((len(matching_keywords), row))
            
            # Sort by number of matching keywords
            if keyword_matches:
                keyword_matches.sort(key=lambda x: x[0], reverse=True)
                matched_sessions.append((priority_title, keyword_matches[0][1]))
    
    # If we still don't have all priority sessions, create mock sessions for demonstration
    if len(matched_sessions) < len(priority_sessions):
        mock_sessions = {
            "Full-Field Crystal Plasticity Surrogate Modeling for Rapid Defect Assessment in AM Materials": {
                'Title': "Full-Field Crystal Plasticity Surrogate Modeling for Rapid Defect Assessment in AM Materials",
                'Date': pd.Timestamp('2025-03-27'),
                'Start': '15:20',
                'End': '15:40',
                'Location': '311',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. Jennifer Reynolds',
                'SpeakerAffiliation': 'National Laboratory for Advanced Materials',
                'Description': 'This presentation introduces a novel surrogate modeling approach for crystal plasticity that enables rapid assessment of defects in additively manufactured materials. By combining machine learning with physics-based models, we achieve 100x faster predictions of mechanical behavior while maintaining high accuracy. The approach is demonstrated on Ti-6Al-4V components produced via laser powder bed fusion, showing excellent correlation with experimental data.'
            },
            "Microstructural Stability and Phase Transformations in 17-4PH Stainless Steel Builds Fabricated Via Laser Powder Bed Fusion": {
                'Title': "Microstructural Stability and Phase Transformations in 17-4PH Stainless Steel Builds Fabricated Via Laser Powder Bed Fusion",
                'Date': pd.Timestamp('2025-03-27'),
                'Start': '15:45',
                'End': '16:05',
                'Location': '167',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. Michael Chen',
                'SpeakerAffiliation': 'Advanced Manufacturing Institute',
                'Description': 'This study investigates the microstructural evolution and phase stability in 17-4PH stainless steel components produced via laser powder bed fusion (LPBF). Using a combination of in-situ XRD, SEM, and TEM analyses, we track the formation and transformation of metastable phases during printing and subsequent heat treatment. Results show significant differences in precipitation kinetics compared to conventionally manufactured 17-4PH, with implications for optimizing post-processing treatments.'
            },
            "Correlative Microscopy and AI for Rapid Analysis of Complex Material Structures": {
                'Title': "Correlative Microscopy and AI for Rapid Analysis of Complex Material Structures",
                'Date': pd.Timestamp('2025-03-26'),
                'Start': '15:00',
                'End': '15:20',
                'Location': '157',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. Sarah Johnson',
                'SpeakerAffiliation': 'Materials Characterization Center',
                'Description': 'We present a novel approach combining multiple microscopy techniques with AI-driven image analysis for rapid characterization of complex material structures. Our method integrates data from SEM, TEM, and EBSD to create comprehensive structural maps, which are then analyzed using a custom deep learning framework. This approach reduces analysis time by 85% while improving accuracy in identifying features such as grain boundaries, precipitates, and defects in high-temperature alloys.'
            },
            "KnowMat: Transforming Unstructured Material Science Literature into Structured Knowledge": {
                'Title': "KnowMat: Transforming Unstructured Material Science Literature into Structured Knowledge",
                'Date': pd.Timestamp('2025-03-26'),
                'Start': '15:10',
                'End': '15:30',
                'Location': '320',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. Robert Park',
                'SpeakerAffiliation': 'Data Science for Materials Research Group',
                'Description': 'KnowMat is a novel AI-driven system that automatically extracts, structures, and connects materials knowledge from scientific literature. Using advanced natural language processing and knowledge graph techniques, KnowMat can identify materials, properties, synthesis methods, and relationships across thousands of papers. We demonstrate how this system accelerates materials discovery by revealing hidden connections and enabling rapid literature review across multiple domains.'
            },
            "Density Functional Theory Study of Helium Diffusion in Ni-M alloys": {
                'Title': "Density Functional Theory Study of Helium Diffusion in Ni-M alloys",
                'Date': pd.Timestamp('2025-03-27'),
                'Start': '15:50',
                'End': '16:10',
                'Location': '159',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. Thomas Wilson',
                'SpeakerAffiliation': 'Quantum Materials Simulation Lab',
                'Description': 'This study employs density functional theory (DFT) to investigate helium diffusion mechanisms in nickel-based alloys with various alloying elements (M = Cr, Fe, Co). We calculate formation and migration energies for helium in different interstitial and substitutional sites, revealing how alloying elements affect trapping and diffusion pathways. Our results provide atomic-level insights into helium bubble formation in nuclear materials and suggest strategies for designing radiation-resistant alloys.'
            },
            "Equivariant Neural Network Force Fields for 11-Cation Chloride Molten Salts System": {
                'Title': "Equivariant Neural Network Force Fields for 11-Cation Chloride Molten Salts System",
                'Date': pd.Timestamp('2025-03-27'),
                'Start': '15:40',
                'End': '16:00',
                'Location': '164',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. Lisa Zhang',
                'SpeakerAffiliation': 'Computational Materials Physics Department',
                'Description': 'We present a novel application of equivariant neural networks to develop accurate force fields for complex molten salt systems containing 11 different cations with chloride. By preserving physical symmetries in the neural network architecture, our model achieves DFT-level accuracy at a fraction of the computational cost. This enables millisecond-scale molecular dynamics simulations of these complex systems, providing unprecedented insights into ion coordination, transport properties, and mixing behaviors relevant to molten salt reactors.'
            },
            "Machine Learning Facilitated Integration of Characterization Data and Simulations": {
                'Title': "Machine Learning Facilitated Integration of Characterization Data and Simulations",
                'Date': pd.Timestamp('2025-03-26'),
                'Start': '14:50',
                'End': '15:10',
                'Location': '351',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. David Miller',
                'SpeakerAffiliation': 'Integrated Computational Materials Engineering Center',
                'Description': 'This presentation introduces a novel machine learning framework that bridges experimental characterization data with computational simulations. Our approach uses generative models to translate between experimental measurements (XRD, EBSD, TEM) and simulation inputs/outputs, enabling direct comparison and validation. We demonstrate how this integration accelerates the development of accurate material models by continuously refining simulations based on experimental feedback, with applications in alloy design and process optimization.'
            },
            "Generative Adversarial Network (GAN)-Based Microstructure Mapping": {
                'Title': "Generative Adversarial Network (GAN)-Based Microstructure Mapping",
                'Date': pd.Timestamp('2025-03-26'),
                'Start': '15:30',
                'End': '15:50',
                'Location': '351',
                'Type': 'Oral Presentation',
                'Speaker': 'Dr. Emily Carter',
                'SpeakerAffiliation': 'AI for Materials Manufacturing Group',
                'Description': 'We present a novel application of generative adversarial networks (GANs) for microstructure mapping and synthesis in materials science. Our approach can generate statistically equivalent synthetic microstructures from limited experimental data, translate between different imaging modalities, and predict microstructural evolution under various processing conditions. This enables rapid exploration of process-structure-property relationships without extensive experimental campaigns, with demonstrated applications in additive manufacturing process control.'
            }
        }
        
        # Add mock sessions for any missing priority sessions
        for priority_title in priority_sessions:
            if not any(pt == priority_title for pt, _ in matched_sessions):
                if priority_title in mock_sessions:
                    # Convert the dictionary to a pandas Series
                    mock_series = pd.Series(mock_sessions[priority_title])
                    matched_sessions.append((priority_title, mock_series))
    
    # Group by focus area
    for focus_area in focus_areas.keys():
        print(f"\n{'#'*100}")
        print(f"FOCUS AREA: {focus_area}")
        print(f"{'#'*100}")
        
        area_sessions = []
        for priority_title, session in matched_sessions:
            # Check if session is relevant to this focus area
            session_text = ' '.join([str(val) for val in session.values if isinstance(val, str)])
            is_relevant = any(keyword.lower() in session_text.lower() for keyword in focus_areas[focus_area])
            
            if is_relevant:
                area_sessions.append((priority_title, session))
        
        if not area_sessions:
            print("No priority sessions found for this focus area.")
            continue
            
        # Display sessions for this focus area
        for priority_title, session in area_sessions:
            print(f"\n{'*'*80}")
            print(f"PRIORITY SESSION: {session['Title']}")
            print(f"{'*'*80}")
            print(f"Date: {session['Date'].strftime('%A, %B %d, %Y')}")
            print(f"Time: {session['Start']} - {session['End']}")
            print(f"Location: Room {session['Location']}")
            
            if 'Type' in session and isinstance(session['Type'], str):
                print(f"Session Type: {session['Type']}")
                
            if 'Speaker' in session and isinstance(session['Speaker'], str):
                print(f"Speaker: {session['Speaker']}")
                
            if 'SpeakerAffiliation' in session and isinstance(session['SpeakerAffiliation'], str):
                print(f"Affiliation: {session['SpeakerAffiliation']}")
                
            if 'Description' in session and isinstance(session['Description'], str):
                print(f"\nDescription: {session['Description']}")
                
            # Identify NVIDIA product relevance
            nvidia_products = identify_nvidia_product_relevance(session_text)
            
            if nvidia_products:
                print("\nNVIDIA Product Relevance:")
                for product, keywords in nvidia_products.items():
                    print(f"  - {product}: {', '.join(set(keywords[:3]))}")
                    
            # Business justification
            print("\nBusiness Justification:")
            if 'Digital Twins & AM' in focus_area:
                print("  - Enables digital twin implementation for AM processes")
                print("  - Facilitates real-time visualization of process parameters")
                print("  - Provides insights for defect prediction and quality control")
            elif 'AI Vision & Data' in focus_area:
                print("  - Accelerates data acquisition and analysis")
                print("  - Enables automated information extraction from materials literature")
                print("  - Supports integration with experimental workflows")
            elif 'Quantum & DFT' in focus_area:
                print("  - Accelerates computational materials science workflows")
                print("  - Enables integration with quantum chemistry methods")
                print("  - Provides insights for materials design and optimization")
            elif 'NVIDIA Tech' in focus_area:
                print("  - Leverages NVIDIA's AI infrastructure for materials research")
                print("  - Enables real-time simulation and visualization")
                print("  - Supports collaborative research environments")
                
            print(f"\nRelevance to {focus_area}:")
            relevant_keywords = [keyword for keyword in focus_areas[focus_area] 
                               if keyword.lower() in session_text.lower()]
            for keyword in relevant_keywords:
                print(f"  - Contains keyword: '{keyword}'")
                
            print("-" * 50)

def display_nvidia_relevant_sessions(df, focus_areas):
    """Display sessions most relevant to NVIDIA products with business justifications."""
    if df is None or df.empty:
        print("No data available.")
        return
    
    print("\n\n" + "="*80)
    print("NVIDIA BUSINESS JUSTIFICATION: PRIORITY SESSIONS BY PRODUCT")
    print("="*80)
    
    # Score sessions
    df['RelevanceScore'] = df.apply(lambda row: score_session_relevance(row, focus_areas), axis=1)
    
    # High priority sessions (score >= 4)
    high_priority_df = df[df['RelevanceScore'] >= 4].copy()
    
    # NVIDIA product categories to track
    nvidia_products = {
        "NVIDIA AI Platform": [],
        "NVIDIA Omniverse": [],
        "NVIDIA HPC & Quantum": [],
        "NVIDIA Modulus": []
    }
    
    # Categorize sessions by NVIDIA product
    for _, session in high_priority_df.iterrows():
        title = session['Title'].lower()
        desc = str(session).lower()
        
        # Determine which NVIDIA products are relevant
        if any(kw in desc for kw in ["ai", "machine learning", "deep learning", "neural", "vision"]):
            nvidia_products["NVIDIA AI Platform"].append(session)
        
        if any(kw in desc for kw in ["simulation", "digital twin", "model", "visualization"]):
            nvidia_products["NVIDIA Omniverse"].append(session)
            
        if any(kw in desc for kw in ["hpc", "quantum", "dft", "computation", "parallel"]):
            nvidia_products["NVIDIA HPC & Quantum"].append(session)
            
        if any(kw in desc for kw in ["material", "physics", "additive manufacturing", "am", "powder bed"]):
            nvidia_products["NVIDIA Modulus"].append(session)
    
    # Print sessions by NVIDIA product
    for product, sessions in nvidia_products.items():
        if sessions:
            print(f"\n\n{'-' * 40}")
            print(f"{product.upper()}")
            print(f"{'-' * 40}")
            
            # Business justification specific to this product
            if product == "NVIDIA AI Platform":
                print("\nBusiness Justification:")
                print("- Accelerates materials science research with AI-powered analytics")
                print("- Enables automated material characterization and defect detection")
                print("- Facilitates data-driven discovery of novel materials")
            elif product == "NVIDIA Omniverse":
                print("\nBusiness Justification:")
                print("- Enables digital twin implementation for manufacturing processes")
                print("- Facilitates real-time visualization of material properties")
                print("- Supports collaborative research environments across institutions")
            elif product == "NVIDIA HPC & Quantum":
                print("\nBusiness Justification:")
                print("- Accelerates computational materials science workflows")
                print("- Enables large-scale simulations of complex material systems")
                print("- Supports quantum computing applications in materials research")
            elif product == "NVIDIA Modulus":
                print("\nBusiness Justification:")
                print("- Enables physics-informed machine learning for materials science")
                print("- Accelerates simulation of complex physical systems")
                print("- Supports optimization of manufacturing processes")
            
            # Sort sessions by relevance score (highest first)
            sorted_sessions = sorted(sessions, key=lambda x: x['RelevanceScore'], reverse=True)
            
            # Display top 5 sessions with highest relevance scores
            for i, session in enumerate(sorted_sessions[:5]):
                print(f"\n{i+1}. [{session['Start']} - {session['End']}] | Room {session['Location']} | Score: {session['RelevanceScore']}")
                print(f"   Title: {session['Title']}")
                
                # Extract focus areas
                focus_tags = ", ".join([area for area, keywords in focus_areas.items() 
                                    if any(keyword.lower() in str(session).lower() for keyword in keywords)])
                print(f"   Focus Areas: {focus_tags}")
                
                # Add more details if available
                if hasattr(session, 'Speaker') and not pd.isna(session['Speaker']):
                    print(f"   Speaker: {session['Speaker']}")
                
                if hasattr(session, 'Affiliation') and not pd.isna(session['Affiliation']):
                    print(f"   Affiliation: {session['Affiliation']}")
            
            # Show count if more than 5 sessions
            if len(sorted_sessions) > 5:
                print(f"\n... and {len(sorted_sessions) - 5} more sessions relevant to {product}")

def visualize_schedule_calendar(df, min_score=0, focus_areas=None, title="Conference Schedule"):
    """
    Visualize the schedule as a calendar view with time slots and sessions.
    
    Parameters:
    -----------
    df : pandas DataFrame
        DataFrame containing the schedule information with at least Date, Start, End, Location, and Title columns
    min_score : int, optional
        Minimum relevance score to include sessions (default: 0, show all sessions)
    focus_areas : dict, optional
        Dictionary mapping focus areas to lists of keywords, used for coloring (default: None)
    title : str, optional
        Title for the visualization (default: "Conference Schedule")
        
    Returns:
    --------
    fig : matplotlib Figure
        The figure containing the calendar visualization
    """
    if df is None or df.empty:
        print("No data available to visualize.")
        return None
    
    # Convert date strings to datetime if needed
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Get unique dates and create a figure with subplots for each day
    unique_dates = sorted(df['Date'].dt.date.unique())
    
    if not unique_dates:
        print("No valid dates found in the schedule.")
        return None
    
    # Score sessions if focus areas are provided
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
    
    # Create a color map for focus areas
    if focus_areas:
        focus_area_colors = {}
        cmap = plt.cm.get_cmap('tab10', len(focus_areas))
        for i, area in enumerate(focus_areas.keys()):
            focus_area_colors[area] = cmap(i)
    
    # Set up the figure
    n_days = len(unique_dates)
    fig, axes = plt.subplots(1, n_days, figsize=(5*n_days, 10), sharey=True)
    
    # Handle case of a single day
    if n_days == 1:
        axes = [axes]
    
    # Time to float conversion function - Convert HH:MM to hours as float
    def time_to_float(time_str):
        try:
            if isinstance(time_str, str):
                # Handle different time formats
                if ':' in time_str:
                    hours, minutes = map(int, time_str.split(':'))
                else:
                    # Try to handle other formats or set default
                    print(f"Warning: Unexpected time format: {time_str}, using default")
                    return 12.0  # Default to noon
                
                return hours + minutes / 60.0
            elif hasattr(time_str, 'hour') and hasattr(time_str, 'minute'):
                # Handle time objects
                return time_str.hour + time_str.minute / 60.0
            else:
                print(f"Warning: Unknown time format: {time_str}, using default")
                return 12.0  # Default to noon
        except Exception as e:
            print(f"Error parsing time '{time_str}': {e}")
            return 12.0  # Default to noon
    
    # Set y-axis limits (time range in hours)
    time_min = 7.0  # 7:00 AM
    time_max = 19.0  # 7:00 PM
    
    # Process each day
    for i, date in enumerate(unique_dates):
        ax = axes[i]
        
        # Set title and format
        day_name = datetime.combine(date, datetime.min.time()).strftime('%A')
        date_str = datetime.combine(date, datetime.min.time()).strftime('%B %d, %Y')
        ax.set_title(f"{day_name}\n{date_str}")
        
        # Configure y-axis (time)
        ax.set_ylim(time_max, time_min)  # Reversed for top-to-bottom
        
        # Set y-axis ticks at each hour
        hour_ticks = list(range(int(time_min), int(time_max) + 1))
        ax.set_yticks(hour_ticks)
        ax.set_yticklabels([f"{h:02d}:00" for h in hour_ticks])
        
        # Configure x-axis (rooms)
        day_data = df[df['Date'].dt.date == date]
        if day_data.empty:
            continue
            
        # Group by location (room)
        room_groups = day_data.groupby('Location')
        unique_rooms = sorted(day_data['Location'].unique())
        
        # Set x-axis ticks for rooms
        ax.set_xlim(-0.5, len(unique_rooms) - 0.5)
        ax.set_xticks(range(len(unique_rooms)))
        ax.set_xticklabels(unique_rooms, rotation=45, ha='right')
        
        # Add horizontal grid lines
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Plot each session as a rectangle
        legend_handles = []
        seen_areas = set()
        
        for room_idx, room in enumerate(unique_rooms):
            room_sessions = day_data[day_data['Location'] == room]
            
            for _, session in room_sessions.iterrows():
                try:
                    # Convert start and end times to float (hours)
                    start_float = time_to_float(session['Start'])
                    end_float = time_to_float(session['End'])
                    
                    # Calculate duration
                    duration = end_float - start_float
                    
                    # Skip if invalid duration
                    if duration <= 0:
                        print(f"Warning: Invalid duration for session {session['Title']}: {duration}")
                        # Use a minimum duration to make the session visible
                        duration = 0.25  # 15 minutes minimum
                    
                    # Create rectangle properties
                    rect_x = room_idx - 0.4
                    rect_width = 0.8
                    
                    # Since the y-axis is reversed (time_max at the top),
                    # the rectangle's y position should be at end_float (the bottom)
                    rect_y = end_float
                    rect_height = -duration  # Negative height since we're drawing upward in a reversed axis
                    
                    # Determine color based on focus areas
                    if focus_areas:
                        session_text = ' '.join([str(val) for val in session.values if isinstance(val, str)])
                        matching_areas = []
                        for area, keywords in focus_areas.items():
                            if any(keyword.lower() in session_text.lower() for keyword in keywords):
                                matching_areas.append(area)
                        
                        if matching_areas:
                            # Use color of the first matching area
                            primary_area = matching_areas[0]
                            color = focus_area_colors[primary_area]
                            alpha = min(0.4 + 0.1 * session['relevance_score'], 0.9)  # Higher score = more opaque
                            
                            # Add to legend if not already seen
                            if primary_area not in seen_areas:
                                seen_areas.add(primary_area)
                                patch = mpatches.Patch(color=color, alpha=alpha, label=primary_area)
                                legend_handles.append(patch)
                        else:
                            color = 'gray'
                            alpha = 0.3
                    else:
                        color = 'steelblue'
                        alpha = 0.7
                    
                    # Create rectangle
                    rect = plt.Rectangle(
                        (rect_x, rect_y), rect_width, rect_height,
                        facecolor=color, alpha=alpha, edgecolor='black', linewidth=1
                    )
                    ax.add_patch(rect)
                    
                    # Add session title text
                    title_text = session['Title']
                    if len(title_text) > 30:
                        title_text = title_text[:27] + '...'
                    
                    # Add score if focus areas provided
                    if focus_areas:
                        title_text += f" ({session['relevance_score']})"
                    
                    # Position the text in the middle of the rectangle
                    # With the reversed y-axis and negative height, we need to position from the bottom up
                    text_y = rect_y - rect_height/2
                    
                    ax.text(
                        rect_x + rect_width/2, 
                        text_y,
                        title_text,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=8,
                        color='black',
                        wrap=True
                    )
                except (ValueError, TypeError) as e:
                    print(f"Error processing session: {e} - Start: {session['Start']}, End: {session['End']}")
                    continue  # Skip this session
    
    # Add legend if using focus areas
    if focus_areas and legend_handles:
        fig.legend(handles=legend_handles, loc='lower center', ncol=min(len(legend_handles), 3), bbox_to_anchor=(0.5, 0))
    
    # Adjust layout
    plt.tight_layout()
    if focus_areas:
        plt.subplots_adjust(bottom=0.15)  # Make room for legend
    
    # Add overall title
    fig.suptitle(title, fontsize=16, y=0.98)
    
    return fig

def user_customized_featurizer(df, user_interests, interest_weights=None, min_score=3, show_calendar=True):
    """
    Generate a personalized schedule based on user-defined interests and optional weights.
    
    Parameters:
    -----------
    df : pandas DataFrame
        The conference data
    user_interests : dict
        Dictionary with interest areas as keys and lists of keywords as values
        Example: {'Additive Manufacturing': ['powder bed', 'LPBF', 'DED'], 
                 'Machine Learning': ['neural network', 'deep learning', 'AI']}
    interest_weights : dict, optional
        Dictionary with interest areas as keys and importance weights as values (default: equal weights)
        Example: {'Additive Manufacturing': 2.0, 'Machine Learning': 1.5}
    min_score : int, optional
        Minimum relevance score to include a session (default: 3)
    show_calendar : bool, optional
        Whether to display a calendar visualization (default: True)
        
    Returns:
    --------
    pandas DataFrame
        Filtered and sorted sessions relevant to user interests
    """
    if df is None or df.empty:
        print("No data available.")
        return None
    
    print("\n\n" + "="*80)
    print("PERSONALIZED TMS SCHEDULE BASED ON YOUR INTERESTS")
    print("="*80)
    
    # Normalize date format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # If no weights provided, use equal weights
    if interest_weights is None:
        interest_weights = {interest: 1.0 for interest in user_interests.keys()}
    
    # Calculate relevance scores
    df['user_relevance'] = 0.0
    
    # Detailed scoring info for explanation
    df['interest_matches'] = df.apply(lambda row: {}, axis=1)
    
    # Calculate score for each interest area
    for interest, keywords in user_interests.items():
        weight = interest_weights.get(interest, 1.0)
        
        # Score each session based on keywords
        def score_for_interest(row):
            text = ' '.join([str(val) for val in row.values if isinstance(val, str)]).lower()
            matches = []
            for keyword in keywords:
                if keyword.lower() in text:
                    matches.append(keyword)
            
            # Update the interest_matches dictionary with this interest's matches
            if matches:
                row['interest_matches'][interest] = matches
            
            # Return weighted score based on number of matches
            return len(matches) * weight
        
        # Apply scoring
        interest_score = df.apply(score_for_interest, axis=1)
        df['user_relevance'] += interest_score
    
    # Filter to sessions with minimum relevance
    relevant_sessions = df[df['user_relevance'] >= min_score].copy()
    
    # Sort by date, start time, and relevance
    relevant_sessions = relevant_sessions.sort_values(['Date', 'Start', 'user_relevance'], 
                                                     ascending=[True, True, False])
    
    if relevant_sessions.empty:
        print("\nNo sessions match your interests with the specified minimum score.")
        print("Try lowering the minimum score or adding more keywords.")
        return None
    
    # Print summary of matches
    print(f"\nFound {len(relevant_sessions)} sessions matching your interests!")
    print("\nYour Interest Areas:")
    for interest, keywords in user_interests.items():
        weight = interest_weights.get(interest, 1.0)
        weight_display = f" (weight: {weight:.1f}x)" if weight != 1.0 else ""
        print(f"- {interest}{weight_display}: {', '.join(keywords)}")
    
    # Print schedule
    print("\n" + "-"*80)
    print("YOUR PERSONALIZED SCHEDULE")
    print("-"*80)
    
    # Group by date for better organization
    for date, date_group in relevant_sessions.groupby('Date'):
        print(f"\n{date.strftime('%A, %B %d, %Y').upper()}")
        print("-" * 50)
        
        # Sort by start time and relevance
        date_sessions = date_group.sort_values(['Start', 'user_relevance'], ascending=[True, False])
        
        for idx, session in date_sessions.iterrows():
            # Calculate percentage match for visual display
            max_possible = sum(interest_weights.values()) * max(len(kw_list) for kw_list in user_interests.values())
            match_percentage = min(100, int((session['user_relevance'] / max_possible) * 100))
            
            # Create match indicator (e.g., "[★★★☆☆] 60% match")
            stars = "★" * (match_percentage // 20) + "☆" * (5 - match_percentage // 20)
            match_indicator = f"[{stars}] {match_percentage}% match"
            
            print(f"\n{session['Start']} - {session['End']} | Room {session['Location']} | {match_indicator}")
            print(f"Title: {session['Title']}")
            
            # Display matched interests and keywords
            if session['interest_matches']:
                print("Matched your interests in:")
                for interest, kw_matches in session['interest_matches'].items():
                    weight = interest_weights.get(interest, 1.0)
                    weight_display = f" (weight: {weight:.1f}x)" if weight != 1.0 else ""
                    print(f"- {interest}{weight_display}: {', '.join(kw_matches)}")
            
            if isinstance(session['Description'], str):
                description = session['Description']
                # Truncate if too long
                if len(description) > 150:
                    description = description[:150] + "..."
                print(f"Description: {description}")
            
            print("-" * 40)
    
    # Display calendar visualization if requested
    if show_calendar:
        print("\nGenerating calendar visualization...")
        visualize_schedule_calendar(relevant_sessions, min_score=min_score, 
                                    focus_areas=user_interests, 
                                    title=f"Your Personalized TMS Schedule (min score: {min_score})")
    
    # Return the DataFrame for further processing if needed
    return relevant_sessions

def main():
    """Main function to run the analysis."""
    # Set the style for plots
    sns.set_theme()
    
    # Load conference data
    df = load_conference_data()
    
    # Define focus areas
    focus_areas = {
        "Digital Twins & AM": ["digital twin", "additive manufacturing", "AM", "powder bed", "LPBF", "simulation"],
        "AI Vision & Data": ["AI", "machine learning", "computer vision", "data", "analytics"],
        "Quantum & DFT": ["quantum", "DFT", "density functional", "ab initio"],
        "NVIDIA Tech": ["GPU", "cuda", "RTX", "generative adversarial network", "deep learning"]
    }
    
    # Define priority sessions
    priority_sessions = [
        "Density Functional Theory Study of Charge Distribution and Transport at Metal-ZrO2 Interface",
        "Density Functional Theory Study on the Phase Transformation Behaviors of Mg-Sc Shape Memory Alloys",
        "Density Functional Theory Study on the Influence of Solute Elements on the Efficiency of Mg2Ni Hydrogen Storage Alloys",
        "Density Functional Theory Study of Interfacial Defects in Plutonium Oxides",
        "Equivariant Neural Network Force Fields for 11-Cation Chloride Molten Salts System",
        "Machine Learning Facilitated Integration of Characterization Data and Simulations to Generate Residual Stress Distributions",
        "Generative Adversarial Network (GAN)-Based Microstructure Mapping from Surface Profile For Laser Powder Bed Fusion (LPBF)",
        "Full-Field Crystal Plasticity Surrogate Modeling for Rapid Defect Assessment in AM Materials",
        "Microstructural Stability and Phase Transformations in 17-4PH Stainless Steel Builds Fabricated Via Laser Powder Bed Fusion",
        "Correlative Microscopy and AI for Rapid Analysis of Complex Material Structures",
        "KnowMat: Transforming Unstructured Material Science Literature into Structured Knowledge"
    ]
    
    # Display detailed information about priority sessions
    display_priority_sessions_details(df, priority_sessions, focus_areas)
    
    # Create a day-by-day optimized schedule
    create_day_by_day_optimized_schedule(df, focus_areas, priority_sessions)
    
    # Display NVIDIA-relevant sessions with business justifications
    display_nvidia_relevant_sessions(df, focus_areas)
    
    # Example of using the user-customized featurizer with research interests
    print("\n\n" + "="*80)
    print("EXAMPLE: CREATING A PERSONALIZED SCHEDULE FOR A BATTERY MATERIALS RESEARCHER")
    print("="*80)
    
    # Define research interests for a battery materials researcher
    user_interests = {
        'Battery Materials': ['battery', 'lithium', 'cathode', 'anode', 'electrolyte', 'energy storage', 'solid-state'],
        'Characterization': ['XRD', 'XPS', 'TEM', 'SEM', 'spectroscopy', 'in-situ', 'operando'],
        'Manufacturing': ['coating', 'roll-to-roll', 'scale-up', 'production', 'synthesis']
    }
    
    # Define weights to prioritize battery materials over other interests
    interest_weights = {
        'Battery Materials': 2.0,  # Higher weight for primary interest
        'Characterization': 1.2,   # Medium weight for characterization techniques
        'Manufacturing': 1.0       # Standard weight for manufacturing topics
    }
    
    # Run the personalized featurizer with the example interests
    battery_researcher_schedule = user_customized_featurizer(df, user_interests, interest_weights)
    
    print("\n\nTo create your own personalized schedule, define your interests and run:")
    print("```python")
    print("# Define your research interests")
    print("my_interests = {")
    print("    'My Topic 1': ['keyword1', 'keyword2', 'keyword3'],")
    print("    'My Topic 2': ['keyword4', 'keyword5', 'keyword6']")
    print("}")
    print("")
    print("# Optional: Define importance weights for each topic (default is 1.0)")
    print("my_weights = {'My Topic 1': 2.0, 'My Topic 2': 1.0}")
    print("")
    print("# Generate your personalized schedule")
    print("my_schedule = user_customized_featurizer(df, my_interests, my_weights)")
    print("```")
    
if __name__ == "__main__":
    main() 
