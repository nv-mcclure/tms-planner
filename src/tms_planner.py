#!/usr/bin/env python3
# tms_planner.py
# A command-line interface for generating personalized TMS conference schedules

import argparse
import json
import pandas as pd
import numpy as np
from analyze_tms import load_conference_data, user_customized_featurizer

# Pre-defined research profiles
RESEARCH_PROFILES = {
    "battery": {
        "interests": {
            "Battery Materials": ["battery", "lithium", "cathode", "anode", "electrolyte", "energy storage", "solid-state"],
            "Characterization": ["XRD", "XPS", "TEM", "SEM", "spectroscopy", "in-situ", "operando"],
            "Manufacturing": ["coating", "roll-to-roll", "scale-up", "production", "synthesis"]
        },
        "weights": {
            "Battery Materials": 2.0,
            "Characterization": 1.2,
            "Manufacturing": 1.0
        }
    },
    "ml": {
        "interests": {
            "AI Methods": ["machine learning", "deep learning", "neural network", "AI", "artificial intelligence", 
                          "computer vision", "natural language processing"],
            "Data Science": ["data mining", "feature engineering", "big data", "high-throughput", "database", 
                            "informatics", "prediction"],
            "Applications": ["materials discovery", "property prediction", "microstructure analysis", 
                            "generative design", "optimization"]
        },
        "weights": {
            "AI Methods": 1.5,
            "Data Science": 1.3,
            "Applications": 2.0
        }
    },
    "am": {
        "interests": {
            "AM Processes": ["additive manufacturing", "AM", "3D printing", "powder bed fusion", "LPBF", 
                           "directed energy deposition", "DED", "wire arc", "binder jetting"],
            "Materials": ["titanium", "aluminum", "superalloy", "stainless steel", "inconel", "powder", 
                         "feedstock", "porosity"],
            "Characterization": ["microstructure", "mechanical properties", "defect", "residual stress", 
                                "texture", "grain", "phase"]
        },
        "weights": {
            "AM Processes": 2.0,
            "Materials": 1.5,
            "Characterization": 1.2
        }
    },
    "quantum": {
        "interests": {
            "Quantum Methods": ["quantum", "DFT", "density functional theory", "ab initio", "first principles",
                              "molecular dynamics", "monte carlo"],
            "Materials": ["electronic structure", "band structure", "phonon", "defect", "surface", "interface",
                         "phase stability"],
            "Applications": ["catalysis", "energy materials", "magnetic materials", "superconductors",
                            "topological materials"]
        },
        "weights": {
            "Quantum Methods": 2.0,
            "Materials": 1.5,
            "Applications": 1.7
        }
    },
    "corrosion": {
        "interests": {
            "Corrosion": ["corrosion", "oxidation", "passivation", "galvanic", "pitting", "rust", "degradation"],
            "Environments": ["aqueous", "marine", "high temperature", "molten salt", "acid", "alkaline"],
            "Materials": ["steel", "stainless", "aluminum", "magnesium", "titanium", "coating", "inhibitor"]
        },
        "weights": {
            "Corrosion": 2.0,
            "Environments": 1.3,
            "Materials": 1.5
        }
    }
}

def load_interests_from_file(file_path):
    """Load user interests from a JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Verify the structure
        if "interests" not in data:
            print("Error: 'interests' key not found in JSON file")
            return None, None
            
        # Weights are optional
        weights = data.get("weights", None)
        return data["interests"], weights
        
    except Exception as e:
        print(f"Error loading interests file: {e}")
        return None, None

def save_template_interests(file_path, profile="battery"):
    """Save a template interests file for users to customize"""
    if profile not in RESEARCH_PROFILES:
        profile = "battery"  # Default to battery if profile not found
    
    data = RESEARCH_PROFILES[profile]
    
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Template interests file saved to {file_path}")
        print("You can customize this file and use it with the -i/--interests option")
    except Exception as e:
        print(f"Error saving template file: {e}")

def main():
    """Command-line interface for the TMS planner"""
    parser = argparse.ArgumentParser(description="Generate personalized TMS conference schedules")
    
    # Input file options
    parser.add_argument("-f", "--file", default="TMS2025AI_Excel_02-21-2025.xlsx", 
                      help="Path to the TMS Excel file (default: TMS2025AI_Excel_02-21-2025.xlsx)")
    
    # Interests options
    interests_group = parser.add_argument_group("Interests options (choose one)")
    interests_group.add_argument("-p", "--profile", choices=list(RESEARCH_PROFILES.keys()),
                               help="Use a pre-defined research profile")
    interests_group.add_argument("-i", "--interests", 
                               help="Path to a JSON file with custom interests")
    interests_group.add_argument("-t", "--template", 
                               help="Generate a template interests file at the specified path")
    
    # Additional options
    parser.add_argument("-m", "--min-score", type=int, default=3,
                      help="Minimum relevance score to include a session (default: 3)")
    parser.add_argument("-l", "--list-profiles", action="store_true",
                      help="List available pre-defined profiles")
    
    args = parser.parse_args()
    
    # List profiles and exit
    if args.list_profiles:
        print("Available research profiles:")
        for profile, data in RESEARCH_PROFILES.items():
            print(f"  {profile}:")
            for area, keywords in data["interests"].items():
                print(f"    - {area}: {', '.join(keywords[:3])}...")
        return
    
    # Save template and exit
    if args.template:
        profile = args.profile if args.profile else "battery"
        save_template_interests(args.template, profile)
        return
    
    # Make sure we have interests defined
    if not args.profile and not args.interests:
        print("Error: You must specify either a pre-defined profile (-p) or a custom interests file (-i)")
        parser.print_help()
        return
    
    # Load conference data
    print("Loading TMS conference data...")
    df = load_conference_data(args.file)
    
    if df is None:
        print(f"Error: Could not load conference data from {args.file}")
        return
    
    # Get interests and weights
    if args.interests:
        interests, weights = load_interests_from_file(args.interests)
        if interests is None:
            return
    else:  # Use profile
        profile_data = RESEARCH_PROFILES[args.profile]
        interests = profile_data["interests"]
        weights = profile_data["weights"]
    
    # Generate personalized schedule
    user_customized_featurizer(df, interests, weights, min_score=args.min_score)

if __name__ == "__main__":
    main() 