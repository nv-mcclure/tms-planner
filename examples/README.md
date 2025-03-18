# TMS Planner Example Profiles

This directory contains example interest profiles that can be used with the TMS Planner tool.

## Available Examples

- **example_profile.json**: A sample profile focused on battery materials research
  - Includes interests in battery materials, characterization techniques, and manufacturing processes
  - Uses weighted preferences to prioritize certain categories

## Using Example Profiles

You can use any example profile with the TMS Planner by running:

```bash
python src/tms_planner.py --interests examples/example_profile.json
```

## Creating Your Own Profiles

The easiest way to create your own profile is to use the interactive helper:

```bash
python src/create_interests.py
```

This will guide you through the process of defining research interests and will save the profile as a JSON file.

Alternatively, you can copy and modify any example profile to suit your needs. 