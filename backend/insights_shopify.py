import pandas as pd
#Automated Insights & Recommendations
#Load the data
shopify_data=pd.read_csv('data/shopify_data.csv')

# Convert to datetime if not already
shopify_data['order_date'] = pd.to_datetime(shopify_data['order_date'])

# 1. Targeting Recommendations
# High-value customers
customer_sales = shopify_data.groupby('customer_id')['total_sale'].sum().sort_values(ascending=False)
top_10_percent = customer_sales.head(int(0.1 * len(customer_sales)))
print("🎯 Recommend retargeting these high-LTV customers via email campaigns or loyalty programs.")

# Best-selling products
top_products = shopify_data.groupby('product_id')['total_sale'].sum().sort_values(ascending=False)
print("📌 Focus promotional campaigns on top product(s):", list(top_products.index[:2]))

# 2. Budget Shift Recommendations
# Sales by month
monthly_sales = shopify_data.set_index('order_date').resample('M')['total_sale'].sum()

# Identify strongest month(s)
peak_months = monthly_sales.sort_values(ascending=False).head(2).index.strftime('%B %Y').tolist()
print("📆 Shift more ad budget to peak months like:", peak_months)

# Product ROAS assumption
# Let’s pretend product P001 performs best on ad campaigns
print("💸 Allocate more budget to campaigns featuring:", top_products.idxmax())


# 3. A/B Testing Recommendations
# Test product pricing (if price variance exists)
price_variance = shopify_data.groupby('product_id')['price_per_unit'].std()
testable_products = price_variance[price_variance > 5].index.tolist()

print("🧪 Suggest A/B testing pricing for:", testable_products)

# Test different email strategies on repeat vs. new customers
repeat_customers = shopify_data['customer_id'].value_counts()
repeat_ids = repeat_customers[repeat_customers > 2].index.tolist()

print("📧 Run A/B test comparing email content/performance for:")
print(f" - Repeat customers ({len(repeat_ids)} IDs)")
print(f" - New customers")
