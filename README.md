# FAOSTAT Colombia – Agricultural Data Analysis

## Project Overview

This project analyzes agricultural production data from Colombia using FAOSTAT data to identify production trends, productivity patterns, growth opportunities, and potential areas for innovation.

The project follows an end-to-end data analysis workflow, including data cleaning, exploratory analysis, statistical analysis, visualization, and interactive dashboard development.

The analysis combines agricultural data with a business-oriented perspective to move from descriptive insights toward potential opportunities in productivity improvement, market expansion, and circular economy.

## Key Results

- **374.5M tonnes** of cumulative sugar cane production between 2014 and 2024.
- Sugar cane reached approximately **4.6× the production** of the second-ranked product.
- Total agricultural production increased approximately **fourfold** between 1961 and 2024.
- Products were segmented according to **production scale, growth, and productivity**.
- An interactive **Looker Studio dashboard** was developed to explore the results.

## Business Questions

The analysis was structured around four main questions:

1. **What are the main agricultural products in Colombia?**

2. **How has agricultural production evolved over time?**

3. **Which products may represent opportunities for innovation or productivity improvement?**

4. **Which products could support potential new business lines or value-added opportunities?**

## Dataset & Data Preparation

The project uses FAOSTAT agricultural production data for Colombia.

The original dataset was intentionally modified as part of a training exercise to introduce data quality issues and simulate a real-world data cleaning scenario.

## Dashboard

An interactive dashboard was developed in **Looker Studio** to explore the agricultural production analysis.

The dashboard includes:

- Top agricultural products
- Historical production trends
- Average production
- Average productivity
- Cultivated area
- Production growth
- Product segmentation
- Production vs productivity
- Historical productivity evolution

The dashboard link is available in:

**[View Interactive Dashboard](https://datastudio.google.com/reporting/ef9c674b-8bfb-432c-ea78b0ffd7bc)**

### Data Quality Issues Addressed

- Missing and invalid values
- Inconsistent text formatting
- Typographical variations
- Incorrect data types
- Invalid years
- Negative and extreme values
- Missing production values
- Missing units

### Cleaning Approach

A Python-based cleaning pipeline was developed using Pandas and custom validation and imputation functions.

The process includes text normalization, edit-distance-based typo correction, missing-value handling, validation rules, and detection of suspicious imputed values.

The cleaned dataset is available in:

FAOSTAT_Clean.csv

The complete cleaning workflow is documented in:

FAOSTAT_data_cleaning.py

## Analytical Approach

Two complementary time periods were used:

1961–2024: long-term historical production trends.

2014–2024: recent product comparisons, productivity, cultivated area, growth, and strategic opportunity analysis.

### Analytical Methods

- Exploratory Data Analysis (EDA)
- Descriptive statistics
- Historical trend analysis
- Production rankings
- Productivity analysis
- Cultivated area analysis
- Production growth analysis
- Median-based segmentation
- Production vs. productivity analysis

## Key Findings

### 1. Production Landscape

Sugar cane was the dominant product in cumulative production between 2014 and 2024, reaching approximately 374.5 million tonnes.

The second-ranked product, palm kernel oil, accumulated approximately 81.7 million tonnes.

Sugar cane therefore had roughly 4.6 times the cumulative production of the second-ranked product.

Other major products included:

- Raw cow milk
- Rice
- Potatoes
- Green and cooking bananas
- Beer from malted barley
- Bananas
- Fresh chicken meat
- Maize
- Palm oil
- Cassava
- Chicken eggs

### 2. Long-Term Production Trends

Total agricultural production shows a strong long-term increase between 1961 and 2024, with overall production increasing approximately fourfold.

The trend is not strictly linear, however, with several periods of significant increases and decreases.

For example, production experienced a notable decline between 2016 and 2017 before recovering in 2018.

The dashboard also allows users to filter products and explore their individual historical production trajectories.

### 3. Production, Productivity and Cultivated Area

Production volume alone does not provide a complete picture of agricultural performance.

For this reason, the recent analysis compares three dimensions between 2014 and 2024:

#### Average Annual Production

The highest-production products include:

- Sugar cane
- Raw cow milk
- Palm kernel oil
- Green and cooking bananas
- Potatoes
- Rice

#### Average Annual Productivity

- Sugar cane
- Pineapple
- Papayas
- Cabbages
- Bananas
- Strawberries

#### Average Cultivated Area

- Palm oil
- Green coffee
- Maize
- Rice
- Sugar cane
- Green and cooking bananas

This comparison shows that production scale, productivity, and cultivated area provide different perspectives on agricultural performance.

### 4. Production Growth Segmentation

Products were classified according to their production scale and growth between 2014 and 2024.

Median values were used as thresholds to distinguish relatively high and low production and growth.

#### Estrellas

**High production + High growth**

Large-scale products with strong growth.

Examples:

- Chicken eggs
- Palm oil
- Raw cow milk
- Fresh chicken meat
- Avocado

#### Emergentes

**Low production + High growth**

Products growing from a smaller production base.

Examples:

- Cashew nuts
- Sesame oil
- Eggplants
- Asparagus
- Chili peppers
- Pears

#### Consolidados

**High production + Low growth**

Large-scale products with relatively limited growth.

Examples include:

- Sugar cane
- Skim milk
- Coconut with shell
- Other tropical fruits

#### Nicho

**Low production + Low growth**

Products with relatively lower production scale and growth.

These categories are relative to the analyzed dataset because median values are used as thresholds. They should therefore be interpreted as analytical classifications rather than absolute definitions of market status.

## R&D and Strategic Opportunities

A second analytical framework compares production volume with productivity.

Both variables are displayed using logarithmic scales because the products differ substantially in magnitude.

Median production and productivity values are used to identify four strategic categories.

### Improvement in Yield

**High production + Low productivity**

Products in this category combine significant production scale with comparatively lower productivity.

Cacao is a notable example.

Its historical productivity provides additional context, showing lower productivity in 2024 than in 1961.

This makes cacao a potential candidate for investigating:

- Production efficiency
- Agricultural practices
- Technological interventions
- Process optimization
- Factors associated with productivity changes

Chicken eggs with shell also fall within this category, showing relatively limited productivity change over the historical period.

### Circular Economy Potential

**High production + High productivity**

Products in this category combine significant production scale with relatively high productivity.

Representative examples include:

- Sugar cane
- Palm kernel oil
- Potatoes
- Bananas
- Sorghum
- Maize
- Rice
  
These products can be considered candidates for investigating:

- Agricultural residue valorization
- By-product utilization
- Biomass transformation
- Fermentation
- Bio-based products
- Value-added processing

The dataset does not establish the economic feasibility of these opportunities. It provides a quantitative basis for identifying products that may merit further investigation.

### Market Expansion

**Low production + High productivity**

Products in this category combine relatively high productivity with lower production scale.

Examples include:

- Eggplants
- Spinach
- Cashew nuts
- Asparagus
- Oats
- Peanuts with shell
- Beet sugar

These products can be considered candidates for further investigation into scaling, commercialization, processing, and market development.

Production growth should not be interpreted directly as consumer demand. Additional market, price, cost, and demand data would be required to evaluate these opportunities.

### Review Feasibility

**Low production + Low productivity**

Products in this category combine relatively low production with relatively low productivity.

Dry lentils are the clearest example.

Two products also appear close to the boundary with the Market Expansion category:

- Dry chickpeas
- Sesame seeds

These cases demonstrate that the classification depends on the relative position of each product around the median thresholds.

## Historical Productivity Analysis

The dashboard also includes a temporal analysis of productivity.

This provides additional context to the production-productivity framework by showing how productivity has changed over time.

The historical analysis can help distinguish between:

- Productivity improvement
- Productivity stagnation
- Productivity decline
- More recent changes

The cacao case demonstrates how a current strategic classification can be interpreted together with historical performance rather than from a single point in time.

## Tools & Technologies

### Data Analysis & Cleaning

- Python
- Pandas
- NumPy

### Data Inspection & Validation

- Microsoft Excel — used to inspect the dataset, review the cleaned CSV output, and visually validate changes during the cleaning process.

### Data Visualization & BI

- Looker Studio

### Analytical Methods

- Exploratory Data Analysis (EDA)
- Descriptive statistics
- Time-series analysis
- Productivity analysis
- Growth analysis
- Median-based segmentation
- Strategic opportunity analysis

## Limitations

This analysis provides a quantitative framework for identifying patterns and potential opportunities, but it is not a complete market or investment analysis.

Key limitations include:

Production and productivity data do not measure profitability.

The dataset does not directly measure consumer demand.

Production growth should not be interpreted as market-demand growth.

Circular economy and market expansion categories identify candidates for further investigation rather than proven business opportunities.

Median-based segmentation is relative to the analyzed dataset.

Additional economic, geographic, environmental, and market data would be required for deeper decision-making.

## Future Analysis

Future versions could incorporate:

Agricultural prices

Import and export data

Production costs

Geographic information

Climate variables

Water and land-use indicators

Agricultural waste data

Market demand indicators

These additions could support more advanced analyses such as:

Profitability assessment
Geographic opportunity mapping
Forecasting
Business opportunity prioritization
