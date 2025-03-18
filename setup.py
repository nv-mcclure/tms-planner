from setuptools import setup, find_packages

setup(
    name="tms-planner",
    version="0.1.0",
    description="A tool for personalizing TMS conference schedules",
    author="NVIDIA Materials Science Team",
    packages=find_packages("src"),
    package_dir={"": "src"},
    scripts=[
        "src/tms_planner.py",
        "src/create_interests.py"
    ],
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "openpyxl>=3.0.7",
    ],
    python_requires=">=3.6",
) 