#!/usr/bin/env python
# coding: utf-8

# # Essential Commodity Price Analysis - Bangladesh

# Dataset: https://data.humdata.org/dataset/wfp-food-prices-for-bangladesh

# ## Data Cleaning

# In[237]:


import pandas as pd


# In[238]:


#loading dataset
df = pd.read_csv('Datasets/wfp_food_prices_bgd.csv')


# In[239]:


df.head()


# In[240]:


df.tail()


# In[241]:


df.info()


# In[242]:


#fixing data types: changing date to pd datetime, and price to numeric
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d", errors = 'coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')


# In[243]:


#removing all data before year 2000
df = df[df['date'].dt.year >= 2000]
print("Date range:", df['date'].min(), "to", df['date'].max())


# In[244]:


df.isnull().sum()
#no null values


# In[245]:


print("Categories:")
print(df['category'].value_counts())


# In[246]:


print("Comodities:")
print(df['commodity'].value_counts())
print(df['commodity'].unique())


# In[247]:


print(df['unit'].unique())
print(df['unit'].value_counts())


# In[248]:


#Since units differ, we need to normalize
unit_mapping = {'KG': 1, '100 KG': 1/100, '12 KG': 1/12, '500 G': 2,'L': 1}

#filtering rows to keep only the unit we can normalize - anything with L or KG
df_norm = df[df['unit'].isin(unit_mapping.keys())].copy()

#adding a unit_price column to store price per kg or l
df_norm['unit_price'] = df['price']*df_norm['unit'].map(unit_mapping)

df_norm['unit_price']


# In[249]:


print(df['pricetype'].unique())
print(df['pricetype'].value_counts())


# In[250]:


#since retails price is majority we remove wholesale prices
df_norm = df_norm[df_norm['pricetype'].str.lower() == 'retail']
df_norm['pricetype'].value_counts()


# In[251]:


#I only require these columns: date, division, category, commodity, unit_price
df_clean = df_norm[['date', 'admin1', 'category', 'commodity', 'unit_price']].copy()


# In[252]:


# Since there exists many types of rice, wheat, oil and more, I will group them into four common category
def group_commodity(name):
    name = name.lower()
    if 'rice' in name:
        return 'Rice'
    elif 'wheat' in name:
        return 'Wheat'
    elif 'lentils' in name or 'masur' in name:
        return 'Lentils'
    elif 'oil' in name:
        return 'Oil'
    else:
        return name  # keep original if not matching

df_clean['commodity_group'] = df_clean['commodity'].apply(group_commodity)


# In[253]:


df_clean.info()


# The dataset df_clean has 22056 rows with 5 columns. I dropped columns - admin2, market, market_id, latitude, longitude, priceflag, pricetype, currency, usdprice, unit, commodity_id - and added two columns - unit_price which contains normalized prices and commodity_group which contains the 4 major commodities. I also removed any rows that sold in wholesale. I set the start of the datatset from 2000. There are no null values.

# ## Part 1: Commodity Price Trends

# In[254]:


# I will analyze the top 4 commodities
key_commodities = ['Rice', 'Wheat', 'Lentils','Oil']
df_trend = df_clean[df_clean['commodity_group'].isin(key_commodities)].copy()
df_trend.head()


# In[255]:


#Removing day from date
df_trend['year_month'] = df_trend['date'].dt.to_period('M')
#Finding monthly average price per commodity group
monthly_avg = df_trend.groupby(['year_month', 'commodity_group'])['unit_price'].mean().reset_index()
print(monthly_avg)


# In[256]:


import matplotlib.dates as mdates

# Convert to timestamp (first day of month)
monthly_avg['year_month_dt'] = monthly_avg['year_month'].dt.to_timestamp()

plt.figure(figsize=(14,6))
for commodity in key_commodities:
    subset = monthly_avg[monthly_avg['commodity_group'] == commodity]
    plt.plot(subset['year_month_dt'], subset['unit_price'], label=commodity)

# Auto-format x-axis
plt.gca().xaxis.set_major_locator(mdates.YearLocator())   # one tick per year
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.xlabel("Year")
plt.ylabel("Average Price (BDT per KG/L)")
plt.legend()
plt.tight_layout()
plt.show()


# Prices of key categories (Rice, Wheat, Lentils and Oil) show clear upward trends from 2000 to 2024, with noticeable spikes during global food crises (e.g., 2008, 2022).
# Oil and Lentils prices tend to be more volatile, while Rice and Wheat exhibit gradual but consistent increases.

# ## Part 2: Regional Price Analysis

# In[257]:


import seaborn as sns

# Pivot table: divisions as rows, commodities as columns, average price
division_avg = df_trend.groupby(['admin1','commodity_group'])['unit_price'].mean().unstack()

plt.figure(figsize=(10,6))
sns.heatmap(division_avg, annot=True, fmt=".1f", cmap='YlOrRd')
plt.title("Average Commodity Prices by Division (2000–2024)")
plt.xlabel("Commodity")
plt.ylabel("Division")
plt.show()


# Mymensingh has a consistently higher price across all four commodities. Chittagong, Dhaka and Rangpur also have higher prices compared to others.

# In[258]:


# Extracting year from date
df_regional['year'] = df_regional['date'].dt.year
# Filtering for years 2000, 2012, 2024
years_to_plot = [2010, 2019, 2024]
df_hist = df_regional[df_regional['year'].isin(years_to_plot)]


# In[259]:


plt.figure(figsize=(18,5))

for i, year in enumerate(years_to_plot):
    plt.subplot(1,3,i+1)
    subset = df_hist[df_hist['year'] == year]
    sns.boxplot(x='admin1', y='unit_price', data=subset, palette="Set2")
    plt.xticks(rotation=45)
    plt.title(f"Division-wise Price Distribution in {year}")
    plt.xlabel("Division")
    plt.ylabel("Unit Price (BDT per KG/L)")

plt.tight_layout()
plt.show()


# ## Part 3: Commodity Correlations

# In[260]:


# Pivot table: rows = year_month, columns = commodity_group, values = average price
monthly_prices = df_trend.groupby(['year_month', 'commodity_group'])['unit_price'].mean().unstack()
print(monthly_prices.head())


# In[261]:


# Correlation between commodities
corr_matrix = monthly_prices.corr()
print(corr_matrix)


# In[262]:


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Commodity Prices (2000-2024)")
plt.show()


# In[263]:


Strong positive correlations exist between Rice and Oil.
Oil shows a moderate correlation with lentils.
Lentils have a weaker correlation with Rice.


# In[ ]:


# Yearly rolling correlation between Rice and Wheat
rolling_corr = monthly_prices['Rice'].rolling(12).corr(monthly_prices['Oil'])
rolling_corr.plot(figsize=(12,4), title="Rolling 12-month Correlation: Rice vs Oil")
plt.ylabel("Correlation")
plt.show()


# In[ ]:


# Yearly rolling correlation between Rice and Wheat
rolling_corr = monthly_prices['Rice'].rolling(12).corr(monthly_prices['Wheat'])
rolling_corr.plot(figsize=(12,4), title="Rolling 12-month Correlation: Rice vs Wheat")
plt.ylabel("Correlation")
plt.show()


# In[ ]:


# Yearly rolling correlation between Rice and Wheat
rolling_corr = monthly_prices['Rice'].rolling(12).corr(monthly_prices['Lentils'])
rolling_corr.plot(figsize=(12,4), title="Rolling 12-month Correlation: Rice vs Lentils")
plt.ylabel("Correlation")
plt.show()


# ## Part 4: Price Forecasting and Predictions

# In[ ]:


from statsmodels.tsa.statespace.sarimax import SARIMAX

# Example: Rice prices
rice_ts = monthly_prices['Rice']

# Fit SARIMA (seasonal order can be tuned)
model = SARIMAX(rice_ts, order=(1,1,1), seasonal_order=(1,1,1,12))
model_fit = model.fit(disp=False)

# Forecast next 12 months
forecast = model_fit.forecast(12)
forecast.plot(figsize=(12,5))
plt.title("Rice Price Forecast (Next 12 months)")
plt.show()


# In[ ]:


from statsmodels.tsa.statespace.sarimax import SARIMAX

# Example: Rice prices
rice_ts = monthly_prices['Wheat']

# Fit SARIMA (seasonal order can be tuned)
model = SARIMAX(rice_ts, order=(1,1,1), seasonal_order=(1,1,1,12))
model_fit = model.fit(disp=False)

# Forecast next 12 months
forecast = model_fit.forecast(12)
forecast.plot(figsize=(12,5))
plt.title("Wheat Price Forecast (Next 12 months)")
plt.show()


# In[ ]:


from statsmodels.tsa.statespace.sarimax import SARIMAX

# Example: Rice prices
rice_ts = monthly_prices['Oil']

# Fit SARIMA (seasonal order can be tuned)
model = SARIMAX(rice_ts, order=(1,1,1), seasonal_order=(1,1,1,12))
model_fit = model.fit(disp=False)

# Forecast next 12 months
forecast = model_fit.forecast(12)
forecast.plot(figsize=(12,5))
plt.title("Oil Price Forecast (Next 12 months)")
plt.show()


# In[ ]:


from statsmodels.tsa.statespace.sarimax import SARIMAX

# Example: Rice prices
rice_ts = monthly_prices['Lentils']

# Fit SARIMA (seasonal order can be tuned)
model = SARIMAX(rice_ts, order=(1,1,1), seasonal_order=(1,1,1,12))
model_fit = model.fit(disp=False)

# Forecast next 12 months
forecast = model_fit.forecast(12)
forecast.plot(figsize=(12,5))
plt.title("Lentils Price Forecast (Next 12 months)")
plt.show()


# In[ ]:


SARIMA forecasts indicate a continuation of current price trends over the next 12 months.
Rice and Wheat are expected to remain volatile but upward-trending, while Oil and Lentils will likely increase steadily.

