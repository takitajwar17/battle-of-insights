# Retail Transaction Analysis Dashboard

A comprehensive data analysis and visualization project for retail transaction insights, featuring interactive dashboards and detailed statistical analysis.

## Project Overview

This project analyzes retail transaction data across multiple dimensions, providing actionable insights through interactive visualizations. The analysis covers store performance, payment methods, discount impact, city performance, and promotion effectiveness.

### Key Features

- Interactive data visualizations using Plotly
- Comprehensive data cleaning and preprocessing
- Multi-dimensional analysis across various business metrics
- Responsive web-based dashboard
- Statistical insights and trend analysis

## Technical Stack

### Languages & Libraries
- **Python 3.12**
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - plotly
  - openpyxl

### Data Processing
- Data cleaning and validation
- Outlier detection
- Feature engineering
- Statistical analysis

### Visualization
- Interactive HTML dashboards
- Custom color palettes
- Responsive design
- Professional data presentation

## Analysis Components

### 1. Store Performance Analysis
- Transaction amounts by store type and season
- Volume distribution analysis
- Performance heatmaps
- Temporal trend analysis

### 2. Payment Methods Analysis
- Regional distribution patterns
- High-value transaction analysis
- Temporal usage trends
- Customer category preferences

### 3. Discount Impact Analysis
- Seasonal effectiveness
- ROI measurements
- Customer response patterns
- Temporal optimization

### 4. City Performance Analysis
- Geographic performance metrics
- Seasonal variations
- Transaction patterns
- Regional benchmarking

### 5. Promotion Effectiveness
- Campaign performance metrics
- Seasonal optimization
- ROI analysis
- Customer segment response

## Data Overview

- Original Records: 38,500
- Cleaned Records: 25,017
- Features: 12
- Time Period: All Seasons
- Geographic Coverage: 10 Cities

### Data Quality Metrics
- Data Completeness: 65%
- Data Accuracy: 98.7%
- Missing Values Handled: 12,971
- Outliers Removed: 512

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/takitajwar17/battle-of-insights.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the analysis:
```bash
python enhanced_analysis.py
```

4. Open the dashboard:
```bash
cd visualizations
open index.html
```

## Project Structure

```
retail-analysis-dashboard/
├── Data/
│   ├── transactions.xlsx
│   ├── enhanced_analysis.py
│   └── analysis.py
├── visualizations/
│   ├── index.html
│   ├── store_analysis.html
│   ├── payment_analysis.html
│   ├── discount_analysis.html
│   ├── city_analysis.html
│   └── promo_analysis.html
└── README.md
```

## Key Insights

- Specialty Stores peak in Summer ($53.59) and Spring ($53.52)
- Cash transactions dominate in Boston, Chicago, Houston (p < 0.01)
- November shows highest discount effectiveness ($53.66, CI: ±0.42)
- Chicago leads with 5.55 items/transaction (σ = 0.34)
- BOGO promotions show optimal ROI in Summer (1.31x)

## Development Notes

- Developed on Windows
- Python 3.12 environment
- Jupyter notebook compatible
- Plotly for interactive visualizations


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
