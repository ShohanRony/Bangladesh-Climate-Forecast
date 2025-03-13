#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Preprocessing Script for Bangladesh Climate Forecast Project

This script performs basic preprocessing on the Bangladesh climate dataset.
It includes functions for data cleaning, handling missing values, and feature engineering.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_data(filepath):
    """
    Load the climate dataset from a CSV file
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
        
    Returns:
    --------
    pandas.DataFrame
        Loaded dataset
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Dataset loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def clean_data(df):
    """
    Clean the dataset by handling missing values and outliers
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataset
        
    Returns:
    --------
    pandas.DataFrame
        Cleaned dataset
    """
    # Create a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Check for missing values
    missing_values = cleaned_df.isnull().sum()
    print(f"Missing values before cleaning:\n{missing_values}")
    
    # Handle missing values
    for col in cleaned_df.columns:
        if cleaned_df[col].isnull().sum() > 0:
            if cleaned_df[col].dtype in ['int64', 'float64']:
                # Fill numeric columns with median
                cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
            else:
                # Fill categorical columns with mode
                cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
    
    # Check for outliers using IQR method for numeric columns
    numeric_cols = cleaned_df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        Q1 = cleaned_df[col].quantile(0.25)
        Q3 = cleaned_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Replace outliers with bounds
        cleaned_df.loc[cleaned_df[col] < lower_bound, col] = lower_bound
        cleaned_df.loc[cleaned_df[col] > upper_bound, col] = upper_bound
    
    return cleaned_df

def feature_engineering(df):
    """
    Create new features from existing data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataset
        
    Returns:
    --------
    pandas.DataFrame
        Dataset with new features
    """
    # Create a copy to avoid modifying the original
    engineered_df = df.copy()
    
    # Add decade column
    engineered_df['Decade'] = (engineered_df['Year'] // 10) * 10
    
    # Create climate risk score (example composite feature)
    engineered_df['Climate_Risk_Score'] = (
        engineered_df['Flood_Impact_Score'] * 0.3 + 
        engineered_df['Drought_Severity'] * 0.3 + 
        engineered_df['Cyclone_Count'] * 0.4
    )
    
    # Create environmental health index
    engineered_df['Environmental_Health_Index'] = (
        engineered_df['Forest_Cover_Percent'] * 0.4 + 
        (100 - engineered_df['AQI']) * 0.3 +
        engineered_df['Renewable_Energy_Usage_Percent'] * 0.3
    ) / 100
    
    # Create seasonal features if month data is available
    if 'Month' in engineered_df.columns:
        engineered_df['Season'] = pd.cut(
            engineered_df['Month'], 
            bins=[0, 2, 5, 8, 11, 12], 
            labels=['Winter', 'Spring', 'Summer', 'Autumn', 'Winter'],
            include_lowest=True
        )
    
    return engineered_df

def split_by_region(df):
    """
    Split the dataset by regions for regional analysis
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataset
        
    Returns:
    --------
    dict
        Dictionary containing dataframes for each region
    """
    # Define regions (example grouping of districts)
    coastal_districts = ['Cox\'s Bazar', 'Chattogram', 'Khulna', 'Barishal', 'Satkhira', 'Patuakhali']
    northern_districts = ['Rangpur', 'Rajshahi', 'Dinajpur', 'Bogura', 'Panchagarh', 'Thakurgaon']
    central_districts = ['Dhaka', 'Gazipur', 'Narayanganj', 'Tangail', 'Mymensingh']
    
    # Create regional dataframes
    regions = {
        'coastal': df[df['District'].isin(coastal_districts)],
        'northern': df[df['District'].isin(northern_districts)],
        'central': df[df['District'].isin(central_districts)],
        'other': df[~df['District'].isin(coastal_districts + northern_districts + central_districts)]
    }
    
    return regions

def save_processed_data(df, output_path):
    """
    Save the processed dataframe to a CSV file
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataset
    output_path : str
        Path to save the processed CSV file
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")
    except Exception as e:
        print(f"Error saving processed data: {e}")

def main():
    """Main function to run the preprocessing pipeline"""
    # Define file paths
    input_file = "../Bangladesh_Environmental_Climate_Change_Impact.csv"
    output_file = "../data/processed_climate_data.csv"
    
    # Load data
    df = load_data(input_file)
    if df is None:
        return
    
    # Preprocessing steps
    print("Cleaning data...")
    cleaned_df = clean_data(df)
    
    print("Engineering features...")
    processed_df = feature_engineering(cleaned_df)
    
    # Save processed data
    save_processed_data(processed_df, output_file)
    
    print("Preprocessing completed successfully!")

if __name__ == "__main__":
    main()