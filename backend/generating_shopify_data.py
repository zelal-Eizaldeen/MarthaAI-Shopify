
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate Sample Shopify Sales Data

# Generate sample data
np.random.seed(42)
n = 500

sample_data = pd.DataFrame({
    'order_id': np.arange(1, n+1),
    'customer_id': np.random.randint(1000, 1100, n),
    'product_id': np.random.choice(['P001', 'P002', 'P003', 'P004'], n),
    'quantity': np.random.randint(1, 5, n),
    'price_per_unit': np.random.uniform(20.0, 150.0, n).round(2),
    'order_date': pd.date_range(start='2023-01-01', periods=n, freq='D')
})

sample_data['total_sale'] = sample_data['quantity'] * sample_data['price_per_unit']
sample_data.head()


#Save the results in a csv file
sample_data.to_csv('../data/shopify_data.csv', index=False)


#Perform Exploratory Data Analysis (EDA)
# Top-selling products
top_products = sample_data.groupby('product_id')['total_sale'].sum().sort_values(ascending=False)
print("Top Products by Revenue:")
print(top_products)


# Total sales over time
sample_data.set_index('order_date')['total_sale'].resample('ME').sum().plot(title='Monthly Sales Trend')
plt.ylabel("Total Sales ($)")
plt.show()

# Customer behavior: repeat customers
repeat_customers = sample_data['customer_id'].value_counts()
print(f"Repeat Customers (more than 2 orders): {(repeat_customers > 2).sum()}")

# Average order value
avg_order_value = sample_data.groupby('order_id')['total_sale'].sum().mean()
print(f"Average Order Value: ${avg_order_value:.2f}")


'''
Summary of Insights:
Top Product: Highest revenue contributor

Sales Trend: See if there’s seasonality or spikes

Customer Loyalty: % of returning customers

Average Order Value (AOV): Benchmark for campaign effectiveness
'''
