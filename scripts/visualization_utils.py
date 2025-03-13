#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization Utilities for Bangladesh Climate Forecast Project

This script provides functions for creating various visualizations
for climate data analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec

# Set style for all plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("talk")

# Custom color palette for Bangladesh-themed visualizations
bd_colors = ["#006a4e", "#f42a41", "#0072b2", "#e69f00", "#56b4e9", "#009e73", "#d55e00"]
sns.set_palette(sns.color_palette(bd_colors))

def plot_temperature_trends(df, district=None, save_path=None):
    """
    Plot temperature trends over time
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataset containing temperature data
    district : str, optional
        District name to filter data (if None, shows average across all districts)
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 8))
    
    if district:
        district_data = df[df['District'] == district]
        sns.lineplot(data=district_data, x='Year', y='Avg_Temperature_C', 
                    marker='o', linewidth=2.5, markersize=8)
        plt.title(f'Average Temperature Trend in {district} (1990-2025)', fontsize=18)
    else:
        # Group by year and calculate mean temperature
        yearly_avg = df.groupby('Year')['Avg_Temperature_C'].mean().reset_index()
        sns.lineplot(data=yearly_avg, x='Year', y='Avg_Temperature_C', 
                    marker='o', linewidth=2.5, markersize=8)
        plt.title('Average Temperature Trend in Bangladesh (1990-2025)', fontsize=18)
    
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Average Temperature (°C)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Add trend line
    if district:
        x = district_data['Year']
        y = district_data['Avg_Temperature_C']
    else:
        x = yearly_avg['Year']
        y = yearly_avg['Avg_Temperature_C']
    
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--", alpha=0.8, linewidth=1.5)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    plt.show()

def plot_rainfall_distribution(df, year_range=None, save_path=None):
    """
    Plot rainfall distribution across districts
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataset containing rainfall data
    year_range : tuple, optional
        Range of years to include (start_year, end_year)
    save_path : str, optional
        Path to save the figure
    """
    if year_range:
        start_year, end_year = year_range
        filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    else:
        filtered_df = df
    
    # Calculate average rainfall by district
    district_rainfall = filtered_df.groupby('District')['Annual_Rainfall_mm'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(16, 10))
    ax = sns.barplot(x=district_rainfall.index, y=district_rainfall.values, palette='viridis')
    
    plt.title('Average Annual Rainfall by District', fontsize=20)
    plt.xlabel('District', fontsize=14)
    plt.ylabel('Average Annual Rainfall (mm)', fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on top of bars
    for i, v in enumerate(district_rainfall.values):
        ax.text(i, v + 50, f"{v:.0f}", ha='center', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    plt.show()

def plot_climate_correlation_heatmap(df, save_path=None):
    """
    Plot correlation heatmap for climate variables
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataset containing climate variables
    save_path : str, optional
        Path to save the figure
    """
    # Select relevant climate variables
    climate_vars = [
        'Avg_Temperature_C', 'Annual_Rainfall_mm', 'AQI', 
        'Forest_Cover_Percent', 'River_Water_Level_m', 'Cyclone_Count',
        'Flood_Impact_Score', 'Drought_Severity', 'Agricultural_Yield_ton_per_hectare',
        'Coastal_Erosion_m_per_year', 'Urbanization_Rate_Percent',
        'Carbon_Emission_Metric_Tons_per_Capita', 'Renewable_Energy_Usage_Percent'
    ]
    
    # Calculate correlation matrix
    corr_matrix = df[climate_vars].corr()
    
    plt.figure(figsize=(16, 14))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Generate custom colormap (green to white to red)
    cmap = LinearSegmentedColormap.from_list(
        "bd_climate", 
        [(0, "#006a4e"), (0.5, "#ffffff"), (1, "#f42a41")]
    )
    
    sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                annot=True, fmt=".2f", square=True, linewidths=.5, cbar_kws={"shrink": .8})
    
    plt.title('Correlation Between Climate Variables', fontsize=20, pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    plt.show()

def plot_climate_change_dashboard(df, district, save_path=None):
    """
    Create a comprehensive climate change dashboard for a specific district
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataset containing climate data
    district : str
        District name to create dashboard for
    save_path : str, optional
        Path to save the figure
    """
    district_data = df[df['District'] == district].sort_values('Year')
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(3, 3, figure=fig)
    
    # Temperature trend
    ax1 = fig.add_subplot(gs[0, :])
    sns.lineplot(data=district_data, x='Year', y='Avg_Temperature_C', marker='o', ax=ax1, color='#f42a41')
    ax1.set_title(f'Temperature Trend in {district}', fontsize=16)
    ax1.set_ylabel('Temperature (°C)')
    
    # Rainfall trend
    ax2 = fig.add_subplot(gs[1, 0])
    sns.lineplot(data=district_data, x='Year', y='Annual_Rainfall_mm', marker='o', ax=ax2, color='#006a4e')
    ax2.set_title('Annual Rainfall', fontsize=14)
    ax2.set_ylabel('Rainfall (mm)')
    
    # AQI trend
    ax3 = fig.add_subplot(gs[1, 1])
    sns.lineplot(data=district_data, x='Year', y='AQI', marker='o', ax=ax3, color='#e69f00')
    ax3.set_title('Air Quality Index', fontsize=14)
    ax3.set_ylabel('AQI')
    
    # Forest cover trend
    ax4 = fig.add_subplot(gs[1, 2])
    sns.lineplot(data=district_data, x='Year', y='Forest_Cover_Percent', marker='o', ax=ax4, color='#0072b2')
    ax4.set_title('Forest Cover', fontsize=14)
    ax4.set_ylabel('Forest Cover (%)')
    
    # Disaster metrics
    ax5 = fig.add_subplot(gs[2, 0])
    disaster_data = district_data[['Year', 'Cyclone_Count', 'Flood_Impact_Score', 'Drought_Severity']]
    disaster_data_melted = pd.melt(disaster_data, id_vars=['Year'], 
                                   var_name='Disaster Type', value_name='Value')
    sns.lineplot(data=disaster_data_melted, x='Year', y='Value', hue='Disaster Type', ax=ax5)
    ax5.set_title('Disaster Metrics', fontsize=14)
    ax5.legend(loc='upper left')
    
    # Agricultural yield
    ax6 = fig.add_subplot(gs[2, 1])
    sns.lineplot(data=district_data, x='Year', y='Agricultural_Yield_ton_per_hectare', marker='o', ax=ax6, color='#009e73')
    ax6.set_title('Agricultural Yield', fontsize=14)
    ax6.set_ylabel('Yield (ton/hectare)')
    
    # Carbon emissions vs Renewable energy
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.plot(district_data['Year'], district_data['Carbon_Emission_Metric_Tons_per_Capita'], 'r-', label='Carbon Emissions')
    ax7.set_ylabel('Carbon Emissions (Metric Tons per Capita)', color='r')
    ax7.tick_params(axis='y', labelcolor='r')
    
    ax8 = ax7.twinx()
    ax8.plot(district_data['Year'], district_data['Renewable_Energy_Usage_Percent'], 'g-', label='Renewable Energy')
    ax8.set_ylabel('Renewable Energy Usage (%)', color='g')
    ax8.tick_params(axis='y', labelcolor='g')
    
    lines1, labels1 = ax7.get_legend_handles_labels()
    lines2, labels2 = ax8.get_legend_handles_labels()
    ax7.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    ax7.set_title('Carbon Emissions vs Renewable Energy', fontsize=14)
    
    # Adjust layout
    plt.suptitle(f'Climate Change Dashboard for {district} (1990-2025)', fontsize=22, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Dashboard saved to {save_path}")
    
    plt.show()

def create_climate_forecast_plot(df, district, feature, years_to_forecast=5, save_path=None):
    """
    Create a forecast plot for a specific climate feature
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataset containing climate data
    district : str
        District name to create forecast for
    feature : str
        Climate feature to forecast (column name)
    years_to_forecast : int
        Number of years to forecast
    save_path : str, optional
        Path to save the figure
    """
    district_data = df[df['District'] == district].sort_values('Year')
    
    # Split data into historical and forecast
    max_historical_year = district_data[district_data['Year'] <= 2023]['Year'].max()
    historical = district_data[district_data['Year'] <= max_historical_year]
    forecast = district_data[district_data['Year'] > max_historical_year]
    
    plt.figure(figsize=(14, 8))
    
    # Plot historical data
    plt.plot(historical['Year'], historical[feature], 'o-', color='#0072b2', 
             linewidth=2.5, markersize=8, label='Historical Data')
    
    # Plot forecast data
    plt.plot(forecast['Year'], forecast[feature], 'o--', color='#d55e00', 
             linewidth=2.5, markersize=8, label='Forecast')
    
    # Add confidence interval for forecast (simplified example)
    if not forecast.empty:
        plt.fill_between(
            forecast['Year'], 
            forecast[feature] * 0.9,  # Lower bound (10% below)
            forecast[feature] * 1.1,  # Upper bound (10% above)
            color='#d55e00', alpha=0.2
        )
    
    # Format the plot
    plt.title(f'{feature} Forecast for {district}', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel(feature.replace('_', ' '), fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Add vertical line separating historical from forecast
    plt.axvline(x=max_historical_year, color='gray', linestyle='--', alpha=0.7)
    plt.text(max_historical_year+0.1, plt.ylim()[0] + (plt.ylim()[1]-plt.ylim()[0])*0.05, 
             'Forecast Start', rotation=90, color='gray')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Forecast plot saved to {save_path}")
    
    plt.show()

if __name__ == "__main__":
    # Example usage
    print("This is a module for visualization utilities. Import and use the functions in your analysis.")
    print("Example usage:")
    print("from visualization_utils import plot_temperature_trends")
    print("plot_temperature_trends(df, district='Dhaka')")