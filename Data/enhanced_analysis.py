import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
warnings.filterwarnings('ignore')

# Custom color palettes
CUSTOM_PALETTE = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5']
CUSTOM_PALETTE_2 = ['#22577A', '#38A3A5', '#57CC99', '#80ED99', '#C7F9CC']
CUSTOM_DIVERGING = ['#2D00F7', '#6A00F4', '#8900F2', '#A100F2', '#B100E8', '#BC00DD', '#D100D1']

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette(CUSTOM_PALETTE)
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'sans-serif'

# Create visualizations directory if it doesn't exist
output_dir = 'visualizations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the data
print("Loading and cleaning data...")
df = pd.read_excel('transactions.xlsx')

# Data Cleaning and Preprocessing
def clean_data(df):
    """
    Clean and preprocess the dataset
    """
    df_clean = df.copy()
    
    # Convert date to datetime
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    
    # Extract temporal features
    df_clean['Month'] = df_clean['Date'].dt.month
    df_clean['Day'] = df_clean['Date'].dt.day
    df_clean['Hour'] = df_clean['Date'].dt.hour
    df_clean['DayOfWeek'] = df_clean['Date'].dt.day_name()
    
    # Check for duplicates
    duplicates = df_clean.duplicated().sum()
    if duplicates > 0:
        df_clean = df_clean.drop_duplicates()
        print(f"Removed {duplicates} duplicate entries")
    
    # Handle missing values
    missing_values = df_clean.isnull().sum()
    if missing_values.sum() > 0:
        print("\nMissing values found:")
        print(missing_values[missing_values > 0])
        df_clean = df_clean.dropna()
        print("Removed rows with missing values")
    
    # Check for outliers in Amount and Total_Items
    def handle_outliers(df, column, lower_percentile=1, upper_percentile=99):
        lower = np.percentile(df[column], lower_percentile)
        upper = np.percentile(df[column], upper_percentile)
        outliers = df[(df[column] < lower) | (df[column] > upper)].shape[0]
        if outliers > 0:
            print(f"Found {outliers} outliers in {column}")
            df = df[(df[column] >= lower) & (df[column] <= upper)]
        return df
    
    df_clean = handle_outliers(df_clean, 'Amount($)')
    df_clean = handle_outliers(df_clean, 'Total_Items')
    
    return df_clean

# Clean the data
df_clean = clean_data(df)
print("\nData cleaning completed!")
print(f"Original shape: {df.shape}")
print(f"Clean data shape: {df_clean.shape}")

# 1. Enhanced Store Performance Analysis
def plot_store_performance():
    # Create a subplot with multiple visualizations
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "heatmap"}, {"type": "scatter"}]],
        subplot_titles=(
            'Average Transaction Amount by Store Type and Season',
            'Transaction Volume by Store Type',
            'Store Performance Heatmap',
            'Store Type Performance Trends'
        )
    )
    
    # Plot 1: Average transaction amount
    avg_by_store_season = df_clean.groupby(['Store_Type', 'Season'])['Amount($)'].mean().round(2).unstack()
    for i, season in enumerate(avg_by_store_season.columns):
        fig.add_trace(
            go.Bar(name=season, x=avg_by_store_season.index, y=avg_by_store_season[season]),
            row=1, col=1
        )
    
    # Plot 2: Transaction volume
    trans_volume = df_clean['Store_Type'].value_counts()
    fig.add_trace(
        go.Pie(labels=trans_volume.index, values=trans_volume.values, hole=0.4),
        row=1, col=2
    )
    
    # Plot 3: Heatmap
    pivot_data = df_clean.pivot_table(
        values='Amount($)', 
        index='Store_Type',
        columns='Season',
        aggfunc='mean'
    )
    fig.add_trace(
        go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis'
        ),
        row=2, col=1
    )
    
    # Plot 4: Performance trends
    monthly_store_perf = df_clean.groupby(['Month', 'Store_Type'])['Amount($)'].mean().unstack()
    for store in monthly_store_perf.columns:
        fig.add_trace(
            go.Scatter(x=monthly_store_perf.index, y=monthly_store_perf[store], name=store),
            row=2, col=2
        )
    
    fig.update_layout(height=1000, showlegend=False, title_text="Comprehensive Store Performance Analysis")
    return fig

# 2. Enhanced Payment Analysis
def plot_payment_analysis():
    avg_amount = df_clean['Amount($)'].mean()
    high_value_trans = df_clean[df_clean['Amount($)'] > avg_amount]
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "heatmap"}]],
        subplot_titles=(
            'Payment Methods Distribution by City (High-Value Transactions)',
            'Average Transaction Value by Payment Method',
            'Payment Method Usage Over Time',
            'Payment Method Preference by Customer Category'
        )
    )
    
    # Plot 1: Payment methods by city
    payment_by_city = pd.crosstab(high_value_trans['City'], high_value_trans['Payment_Method'])
    fig.add_trace(
        go.Bar(
            x=payment_by_city.index,
            y=payment_by_city.sum(axis=1),
            marker_color=CUSTOM_PALETTE[0]
        ),
        row=1, col=1
    )
    
    # Plot 2: Average value by payment method
    avg_by_payment = df_clean.groupby('Payment_Method')['Amount($)'].mean()
    fig.add_trace(
        go.Bar(
            x=avg_by_payment.index,
            y=avg_by_payment.values,
            marker_color=CUSTOM_PALETTE[1]
        ),
        row=1, col=2
    )
    
    # Plot 3: Payment trends
    payment_trends = df_clean.groupby(['Month', 'Payment_Method']).size().unstack()
    for method in payment_trends.columns:
        fig.add_trace(
            go.Scatter(x=payment_trends.index, y=payment_trends[method], name=method),
            row=2, col=1
        )
    
    # Plot 4: Payment by customer category
    payment_by_category = pd.crosstab(df_clean['Customer_Category'], df_clean['Payment_Method'])
    fig.add_trace(
        go.Heatmap(
            z=payment_by_category.values,
            x=payment_by_category.columns,
            y=payment_by_category.index,
            colorscale='Viridis'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=1000, showlegend=True, title_text="Comprehensive Payment Method Analysis")
    return fig

# 3. Enhanced Discount Analysis
def plot_discount_analysis():
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "box"}]],
        subplot_titles=(
            'Discount Impact on Sales',
            'Discount Effectiveness by Store Type',
            'Seasonal Discount Patterns',
            'Average Transaction Value: Discount vs No Discount'
        )
    )
    
    # Plot 1: Monthly comparison
    monthly_discount = df_clean.groupby(['Month', 'Discount_Applied'])['Amount($)'].mean().unstack()
    for discount in monthly_discount.columns:
        fig.add_trace(
            go.Scatter(
                x=monthly_discount.index,
                y=monthly_discount[discount],
                name=str(discount),
                mode='lines+markers'
            ),
            row=1, col=1
        )
    
    # Plot 2: Store type effectiveness
    store_discount = df_clean.groupby(['Store_Type', 'Discount_Applied'])['Amount($)'].mean().unstack()
    fig.add_trace(
        go.Bar(
            x=store_discount.index,
            y=store_discount[True] - store_discount[False],
            name='Discount Impact',
            marker_color=CUSTOM_PALETTE[2]
        ),
        row=1, col=2
    )
    
    # Plot 3: Seasonal patterns
    season_discount = pd.crosstab(df_clean['Season'], df_clean['Discount_Applied'])
    fig.add_trace(
        go.Bar(
            x=season_discount.index,
            y=season_discount[True] / (season_discount[True] + season_discount[False]) * 100,
            name='Discount Rate (%)',
            marker_color=CUSTOM_PALETTE[3]
        ),
        row=2, col=1
    )
    
    # Plot 4: Value comparison
    fig.add_trace(
        go.Box(
            x=df_clean['Discount_Applied'],
            y=df_clean['Amount($)'],
            name='Transaction Distribution'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=1000, showlegend=True, title_text="Comprehensive Discount Analysis")
    return fig

# 4. Enhanced City Analysis
def plot_city_analysis():
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "box"}]],
        subplot_titles=(
            'Average Items per Transaction by City',
            'Seasonal Sales Patterns by City',
            'City Performance Matrix',
            'Transaction Value Distribution by City'
        )
    )
    
    # Plot 1: Average items
    avg_items = df_clean.groupby('City')['Total_Items'].mean().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(
            x=avg_items.index,
            y=avg_items.values,
            marker_color=CUSTOM_PALETTE[0]
        ),
        row=1, col=1
    )
    
    # Plot 2: Seasonal patterns
    top_cities = avg_items.head(3).index
    seasonal_sales = df_clean[df_clean['City'].isin(top_cities)].groupby(['City', 'Season'])['Amount($)'].mean().unstack()
    for season in seasonal_sales.columns:
        fig.add_trace(
            go.Bar(
                name=season,
                x=seasonal_sales.index,
                y=seasonal_sales[season]
            ),
            row=1, col=2
        )
    
    # Plot 3: Performance matrix
    city_metrics = pd.pivot_table(
        df_clean,
        values=['Amount($)', 'Total_Items'],
        index='City',
        aggfunc={'Amount($)': 'mean', 'Total_Items': 'mean'}
    )
    fig.add_trace(
        go.Scatter(
            x=city_metrics['Amount($)'],
            y=city_metrics['Total_Items'],
            mode='markers+text',
            text=city_metrics.index,
            marker=dict(size=12, color=CUSTOM_PALETTE[2])
        ),
        row=2, col=1
    )
    
    # Plot 4: Value distribution
    fig.add_trace(
        go.Box(
            x=df_clean['City'],
            y=df_clean['Amount($)'],
            marker_color=CUSTOM_PALETTE[3]
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=1000, showlegend=True, title_text="Comprehensive City Analysis")
    return fig

# 5. Enhanced Promotion Analysis
def plot_promotion_analysis():
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "box"}]],
        subplot_titles=(
            'Promotion Effectiveness by Season',
            'Average Transaction Value by Promotion',
            'Promotion Usage Patterns',
            'Promotion Impact on Items per Transaction'
        )
    )
    
    # Plot 1: Seasonal effectiveness
    promo_season = df_clean.groupby(['Season', 'Promotion'])['Amount($)'].mean().unstack()
    for promo in promo_season.columns:
        fig.add_trace(
            go.Bar(name=promo, x=promo_season.index, y=promo_season[promo]),
            row=1, col=1
        )
    
    # Plot 2: Average value
    promo_avg = df_clean.groupby('Promotion')['Amount($)'].agg(['mean', 'std']).round(2)
    fig.add_trace(
        go.Bar(
            x=promo_avg.index,
            y=promo_avg['mean'],
            error_y=dict(type='data', array=promo_avg['std']),
            marker_color=CUSTOM_PALETTE[1]
        ),
        row=1, col=2
    )
    
    # Plot 3: Usage patterns
    promo_usage = pd.crosstab(df_clean['Month'], df_clean['Promotion'])
    for promo in promo_usage.columns:
        fig.add_trace(
            go.Scatter(
                x=promo_usage.index,
                y=promo_usage[promo],
                name=promo,
                mode='lines+markers'
            ),
            row=2, col=1
        )
    
    # Plot 4: Items per transaction
    fig.add_trace(
        go.Box(
            x=df_clean['Promotion'],
            y=df_clean['Total_Items'],
            marker_color=CUSTOM_PALETTE[3]
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=1000, showlegend=True, title_text="Comprehensive Promotion Analysis")
    return fig

# Generate all plots
print("\nGenerating visualizations...")
store_fig = plot_store_performance()
payment_fig = plot_payment_analysis()
discount_fig = plot_discount_analysis()
city_fig = plot_city_analysis()
promo_fig = plot_promotion_analysis()

# Save the figures
store_fig.write_html(f"{output_dir}/store_analysis.html")
payment_fig.write_html(f"{output_dir}/payment_analysis.html")
discount_fig.write_html(f"{output_dir}/discount_analysis.html")
city_fig.write_html(f"{output_dir}/city_analysis.html")
promo_fig.write_html(f"{output_dir}/promo_analysis.html")

print("\nAnalysis complete! Interactive visualizations have been saved to the 'visualizations' directory.")
