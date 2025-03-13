# Project Structure

This document provides an overview of the repository organization and file structure.

## Repository Structure

```
Bangladesh-Climate-Forecast/
├── data/                               # Data directory
│   └── Bangladesh_Environmental_Climate_Change_Impact.csv  # Main dataset
├── notebooks/                          # Jupyter notebooks
│   └── bangladesh-climate-data-analysis-prediction.ipynb   # Main analysis notebook
├── .gitignore                          # Git ignore file
├── CONTRIBUTING.md                     # Contribution guidelines
├── LICENSE                             # License information
├── PROJECT_STRUCTURE.md                # This file
├── README.md                           # Project overview and documentation
└── requirements.txt                    # Python dependencies
```

## Files Description

### Data Files
- **Bangladesh_Environmental_Climate_Change_Impact.csv**: The primary dataset containing historical climate data for various districts in Bangladesh from 1990 to 2025 (including forecasted data).

### Notebooks
- **bangladesh-climate-data-analysis-prediction.ipynb**: The main Jupyter notebook containing all data analysis, visualizations, and predictive modeling.

### Documentation
- **README.md**: Project overview, features, installation instructions, and usage guidelines.
- **CONTRIBUTING.md**: Guidelines for contributing to the project.
- **PROJECT_STRUCTURE.md**: Description of repository organization.
- **LICENSE**: MIT License file.

### Configuration Files
- **.gitignore**: Specifies intentionally untracked files to ignore.
- **requirements.txt**: Lists all Python dependencies required to run the analysis.

## Data Structure

The main dataset contains the following columns:
- Year
- District
- Avg_Temperature_C
- Annual_Rainfall_mm
- AQI
- Forest_Cover_Percent
- River_Water_Level_m
- Cyclone_Count
- Flood_Impact_Score
- Drought_Severity
- Agricultural_Yield_ton_per_hectare
- Coastal_Erosion_m_per_year
- Urbanization_Rate_Percent
- Carbon_Emission_Metric_Tons_per_Capita
- Renewable_Energy_Usage_Percent

## Analysis Workflow

The analysis in the main notebook follows this general workflow:
1. Data loading and cleaning
2. Exploratory data analysis
3. Feature engineering
4. Statistical analysis
5. Time series analysis
6. Predictive modeling
7. Visualization and interpretation
8. Conclusion and recommendations