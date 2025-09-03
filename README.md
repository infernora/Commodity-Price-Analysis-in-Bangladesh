#  Essential Commodity Price Analysis – Bangladesh  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)  
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-yellow?logo=pandas)](https://pandas.pydata.org/)  
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?logo=plotly)](https://matplotlib.org/)  
[![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-teal)](https://seaborn.pydata.org/)  
[![Statsmodels](https://img.shields.io/badge/Statsmodels-TS%20Forecasting-purple)](https://www.statsmodels.org/)  

---

##  Motivation  
Food security is one of the most pressing challenges in Bangladesh. Tracking and analyzing the price movement of essential commodities such as Rice, Wheat, Lentils, and Oil provides insights that can support policymakers, businesses, and households.  
I analyzed historical food price data (2000–2024) to uncover long-term trends, regional variations, commodity correlations, and future forecasts.  

 Dataset source: [WFP Food Prices for Bangladesh](https://data.humdata.org/dataset/wfp-food-prices-for-bangladesh)  

---

##  Tools & Libraries  
-  **Pandas** – data cleaning & preprocessing  
-  **Matplotlib & Seaborn** – visualizations  
-  **Statsmodels (SARIMA)** – time-series forecasting  
-  **NumPy** – numerical operations  

---

##  Project Workflow  

### Data Cleaning & Normalization  
- Converted dates into `datetime`.  
- Standardized prices (per KG/L).  
- Removed wholesale entries, kept retail only.  
- Selected essential columns (`date`, `division`, `category`, `commodity`, `unit_price`).  

###  Commodity Grouping  
- Grouped multiple varieties into **Rice, Wheat, Lentils, Oil**.  

### Price Trend Analysis  
- Monthly average prices (2000–2024).  
- Clear upward trends with spikes during global food crises (2008, 2022).  

### Regional Comparison  
- Heatmaps & boxplots of division-wise averages.  
- Mymensingh, Dhaka & Chittagong showed higher prices.  

### Correlation Analysis  
- Correlation heatmap across commodities.  
- Strong Rice–Oil relationship, weaker links for Lentils.  

### Forecasting  
- Built **SARIMA models** for each commodity.  
- Forecasted 12 months ahead.  
- Predicted steady upward movement with volatility in Rice & Wheat.  

---

##  What I Learned  
 Data cleaning & normalization using pandas.  
 Aggregating time-series data to identify long-term trends.  
 Visualizations (heatmaps, boxplots, rolling correlations).  
 SARIMA models can forecast commodity prices effectively.  
 Commodity markets in Bangladesh show both global influences (crises) and regional differences.  

