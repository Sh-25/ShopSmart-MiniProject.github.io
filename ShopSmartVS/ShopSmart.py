import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('ShopSmart_sales_dataset.csv')
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())

# •	Clean data (missing values, incorrect data types).
df['Return_Date'] = pd.to_datetime(df['Return_Date'], errors='coerce')
df['Reason'] = df['Reason'].fillna('Unknown')
df['Return_Date'] = df['Return_Date'].fillna(pd.Timestamp('2023-01-01'))
print(df.isnull().sum())
print(df)

#o	Aggregations: total revenue, avg order value
total_revenue = df['Total_Sales'].sum()
avg_order_value = df.groupby('Order_ID')['Total_Sales'].sum().mean()
print(f"Total Revenue:\n ${total_revenue:.2f}")
print(f"Average Order Value:\n ${avg_order_value:.2f}")

# o Visualizations: Enhanced heatmap of product sales, sales trend line

import matplotlib.ticker as mtick

# Convert Order_Date to datetime and extract month
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['month'] = df['Order_Date'].dt.to_period('M')

# Heatmap: Product sales by month
heatmap_data = df.pivot_table(
    index='Product_ID',
    columns='month',
    values='Total_Sales',
    aggfunc='sum'
).fillna(0)

plt.figure(figsize=(14, 8))
sns.heatmap(
    heatmap_data,
    cmap='YlOrRd',
    linewidths=0.5,
    linecolor='gray',
    annot=True,
    fmt='.0f',
    cbar_kws={'label': 'Total Sales'}
)
plt.title(' Heatmap of Product Sales by Month', fontsize=18, fontweight='bold')
plt.xlabel('Month', fontsize=14)
plt.ylabel('Product ID', fontsize=14)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Sales trend line: Monthly revenue
monthly_revenue = df.groupby('month')['Total_Sales'].sum().sort_index()

plt.figure(figsize=(12, 6))
sns.lineplot(
    x=monthly_revenue.index.astype(str),
    y=monthly_revenue.values,
    marker='o',
    color='navy',
    linewidth=2.5,
    markersize=8,
    label='Monthly Revenue'
)
plt.title('Monthly Sales Trend', fontsize=18, fontweight='bold')
plt.xlabel('Month', fontsize=14)
plt.ylabel('Revenue ($)', fontsize=14)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# Export cleaned data
df.to_csv('Cleaned_ShopSmart.csv', index=False)
print("Cleaned data exported to 'Cleaned_ShopSmart.csv'")
print(df)

