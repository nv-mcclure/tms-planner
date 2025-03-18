#!/usr/bin/env python3
# create_interests.py
# Interactive helper script to create custom interest profiles for TMS planner

import json
import os
import sys

def print_header():
    """Print the welcome header"""
    print("\n" + "=" * 80)
    print("TMS Conference Planner: Custom Interest Profile Creator".center(80))
    print("=" * 80)
    print("\nThis script will help you create a custom interest profile for the TMS Conference Planner.")
    print("You'll define categories of research interests and keywords for each category.")
    print("Optionally, you can also assign weights to prioritize certain categories.\n")

def get_profile_name():
    """Get a name for the profile"""
    while True:
        name = input("Enter a name for your interest profile (e.g., 'my_research'): ").strip()
        if name:
            return name
        print("Please enter a valid name.")

def get_categories():
    """Get research categories from the user"""
    print("\n" + "-" * 80)
    print("STEP 1: Define your research interest categories".center(80))
    print("-" * 80)
    print("Examples: 'Battery Materials', 'Quantum Computing', 'Additive Manufacturing'")
    
    categories = []
    while True:
        category = input("\nEnter a research category (or press Enter when done): ").strip()
        if not category:
            if not categories:
                print("You must enter at least one category.")
                continue
            break
        categories.append(category)
        print(f"Added: {category}")
    
    return categories

def get_keywords(category):
    """Get keywords for a category"""
    print(f"\nEnter keywords for '{category}' (press Enter after each, blank to finish):")
    print("Examples: 'battery', 'lithium', 'cathode', 'anode'")
    
    keywords = []
    while True:
        keyword = input("Keyword: ").strip().lower()
        if not keyword:
            if not keywords:
                print("You must enter at least one keyword.")
                continue
            break
        keywords.append(keyword)
    
    return keywords

def get_weights(categories):
    """Get optional weights for categories"""
    print("\n" + "-" * 80)
    print("STEP 3: Assign weights to your categories (optional)".center(80))
    print("-" * 80)
    print("Weights help prioritize certain categories. Default weight is 1.0.")
    print("Higher numbers (like 2.0) increase importance, lower numbers (like 0.5) decrease it.")
    
    use_weights = input("\nDo you want to assign custom weights? (y/n): ").lower() == 'y'
    
    if not use_weights:
        return None
    
    weights = {}
    for category in categories:
        while True:
            try:
                weight = input(f"Weight for '{category}' (0.1-5.0, default 1.0): ").strip()
                if not weight:
                    weight = 1.0
                    break
                weight = float(weight)
                if 0.1 <= weight <= 5.0:
                    break
                print("Weight must be between 0.1 and 5.0")
            except ValueError:
                print("Please enter a valid number")
        weights[category] = weight
    
    return weights

def main():
    """Main function to create a custom interest profile"""
    print_header()
    
    # Get profile name
    profile_name = get_profile_name()
    
    # Get categories
    categories = get_categories()
    
    # Get keywords for each category
    print("\n" + "-" * 80)
    print("STEP 2: Define keywords for each category".center(80))
    print("-" * 80)
    interests = {}
    for category in categories:
        keywords = get_keywords(category)
        interests[category] = keywords
    
    # Get optional weights
    weights = get_weights(categories)
    
    # Create the profile
    profile = {"interests": interests}
    if weights:
        profile["weights"] = weights
    
    # Save the profile
    filename = f"{profile_name}.json"
    with open(filename, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"✅ Success! Custom interest profile saved to '{filename}'".center(80))
    print("=" * 80)
    
    # Show how to use it
    print("\nTo use your custom profile with the TMS planner, run:")
    print(f"python tms_planner.py --interests {filename}")
    
    # Show a preview
    print("\nProfile preview:")
    print(json.dumps(profile, indent=2))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled. No profile was saved.")
        sys.exit(1) 