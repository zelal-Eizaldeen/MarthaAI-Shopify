import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

# Load data
PATH_TO_DATA = '../data'
shopify_data = pd.read_csv(f'{PATH_TO_DATA}/shopify_data.csv')
shopify_data['order_date'] = pd.to_datetime(shopify_data['order_date'])

# Pre-calculate insights
customer_sales = shopify_data.groupby('customer_id')['total_sale'].sum().sort_values(ascending=False)
top_10_percent = customer_sales.head(int(0.1 * len(customer_sales)))
top_products = shopify_data.groupby('product_id')['total_sale'].sum().sort_values(ascending=False)
monthly_sales = shopify_data.set_index('order_date').resample('ME')['total_sale'].sum()
peak_months = monthly_sales.sort_values(ascending=False).head(2).index.strftime('%B %Y').tolist()
price_variance = shopify_data.groupby('product_id')['price_per_unit'].std()
testable_products = price_variance[price_variance > 5].index.tolist()
repeat_customers = shopify_data['customer_id'].value_counts()
repeat_ids = repeat_customers[repeat_customers > 2].index.tolist()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Shopify Sales Dashboard"

app.layout = html.Div([
    html.H1("\U0001F6D2 Shopify Sales Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Filter by Product:"),
        dcc.Dropdown(
            options=[{'label': p, 'value': p} for p in shopify_data['product_id'].unique()],
            value=[],
            multi=True,
            id='product-filter'
        )
    ], style={'width': '40%', 'margin': 'auto'}),

    html.Div(id='metrics', style={'textAlign': 'center', 'marginTop': 30}),
    dcc.Graph(id='monthly-sales'),

    html.H2("\U0001F4A1 Strategic Recommendations", style={'textAlign': 'center', 'marginTop': 50}),
    html.Div([
        html.Div([
            html.H4("🎯 Targeting Suggestions"),
            html.Ul([
                html.Li("Retarget top 10% high-value customers via email or loyalty programs."),
                html.Li(f"Focus promotions on top products: {list(top_products.index[:2])}")
            ])
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            html.H4("💸 Budget Shift Suggestions"),
            html.Ul([
                html.Li(f"Increase ad spend during peak months: {', '.join(peak_months)}"),
                html.Li(f"Allocate more budget to top ROAS product: {top_products.idxmax()}")
            ])
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            html.H4("🧪 A/B Testing Suggestions"),
            html.Ul([
                html.Li(f"Test pricing strategies for products with high variance: {', '.join(testable_products)}"),
                html.Li(f"A/B test emails for {len(repeat_ids)} repeat vs new customers")
            ])
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'})
    ], style={'textAlign': 'left', 'padding': '0 80px'})
])

@app.callback(
    [Output('metrics', 'children'),
     Output('monthly-sales', 'figure')],
    [Input('product-filter', 'value')]
)
def update_dashboard(selected_products):
    df = shopify_data.copy()
    if selected_products:
        df = df[df['product_id'].isin(selected_products)]

    total_revenue = df['total_sale'].sum()
    avg_order_value = df.groupby('order_id')['total_sale'].sum().mean()
    repeat_customers = df['customer_id'].value_counts()
    num_repeat = (repeat_customers > 2).sum()

    monthly_sales = df.set_index('order_date')['total_sale'].resample('ME').sum()
    fig = px.line(monthly_sales, title='Monthly Sales Trend', labels={'order_date': 'Month', 'total_sale': 'Total Sales'})

    metrics = html.Div([
        html.H3(f"💰 Total Revenue: ${total_revenue:,.2f}"),
        html.H4(f"📦 Avg Order Value: ${avg_order_value:.2f}"),
        html.H4(f"🔁 Repeat Customers (>2 orders): {num_repeat}")
    ])

    return metrics, fig

if __name__ == '__main__':
    app.run(debug=True)





