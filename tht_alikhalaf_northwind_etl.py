from fastapi import FastAPI
import json
import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="tht0_db_northwind",
    user="postgres",
    password="[!!!INSERT YOUR PASSWORD HERE!!!]"
)

# Create a cursor object
cur = conn.cursor()

# Execute a query to check the connection
cur.execute("SELECT version()")

# Fetch the result of the query
version = cur.fetchone()

# Print the result to confirm that the connection is working
print("Connection to DB successful!")


# Total revenue per category for the last 30 days
revenue_by_category = """
with category_level_data as (
    select
        order_details.order_id
        ,orders.order_date
        ,order_details.product_id
        ,products.product_name
        ,products.category_id
        ,categories.category_name
        ,(order_details.quantity * order_details.unit_price * (1  - order_details.discount))::decimal(10,2) as revenue
        ,order_details.quantity
        ,order_details.unit_price
        ,order_details.discount
    from order_details
        left join orders on order_details.order_id = orders.order_id
        left join products on order_details.product_id = products.product_id
        left join categories on products.category_id = categories.category_id
    where
        order_date between (select max(orders.order_date) from orders) - interval '30 days' and (select max(orders.order_date) from orders)
    order by
        order_details.order_id
        ,orders.order_date desc
)

select
    category_name as "Product Category"
    ,sum(revenue) as "Revenue from Category"
from category_level_data
group by
    category_name
order by
    "Revenue from Category" desc
"""

# Top 5 customers based on total spend in the last 90 days
top_five_customers = """
with customer_level_data as (
    select
        order_details.order_id
        ,orders.order_date
        ,(order_details.quantity * order_details.unit_price * (1  - order_details.discount))::decimal(10,2) as revenue
        ,orders.customer_id
    from order_details
        left join orders on order_details.order_id = orders.order_id
        left join customers on orders.customer_id = customers.customer_id
    where
        order_date between (select max(orders.order_date) from orders) - interval '90 days' and (select max(orders.order_date) from orders)
    order by
        orders.order_date desc
        ,order_details.order_id
)

select
    customer_level_data.customer_id
    ,customers.company_name as "Company"
    ,sum(customer_level_data.revenue) as "Total Spend"
from customer_level_data
    left join customers on customer_level_data.customer_id = customers.customer_id 
group by
    customer_level_data.customer_id
    ,customers.company_name
order by
    "Total Spend" desc
limit 5
"""

# Average order value for each month of the current year
average_monthly_order_value = """
with order_level_data as (
    select
        order_details.order_id
        ,orders.order_date
        ,to_char(orders.order_date, 'yyyy-mm') as order_month
        ,to_char(orders.order_date, 'yyyy-Mon') as order_month_name
        ,sum((order_details.quantity * order_details.unit_price * (1  - order_details.discount)))::decimal(10,2) as revenue_from_order
    from order_details
        left join orders on order_details.order_id = orders.order_id
    where
        order_date between to_date(concat(to_char((select max(orders.order_date) from orders),'yyyy'),'0101'),'yyyymmdd') and (select max(orders.order_date) from orders)
    group by
        order_details.order_id
        ,orders.order_date
    order by
        orders.order_date desc
        ,order_details.order_id
)

select
    order_month_name as "Period"    
    ,avg(order_level_data.revenue_from_order)::decimal(10,2) as "Average Order Value"
from order_level_data
group by
    "Period"
    ,order_month
order by
    order_month asc
"""

df_revenue_by_category = pd.read_sql_query(revenue_by_category, conn)
df_top_five_customers = pd.read_sql_query(top_five_customers, conn)
df_average_monthly_order_value = pd.read_sql_query(average_monthly_order_value, conn)

app = FastAPI()

@app.get("/api/revenue_by_category")
def get_revenue_by_category():
    return json.loads(df_revenue_by_category.to_json(orient="records"))

@app.get("/api/top_five_customers")
def get_top_five_customers():
    return json.loads(df_top_five_customers.to_json(orient="records"))

@app.get("/api/average_monthly_order_value")
def get_average_monthly_order_value():
    return json.loads(df_average_monthly_order_value.to_json(orient="records"))

fig1 = px.bar(df_revenue_by_category, x='Product Category', y='Revenue from Category', title = 'Total Revenue by Category - Last 30 Days')
fig2 = px.bar(df_top_five_customers, x='Total Spend', y='Company', orientation = 'h', title = 'Top 5 Customers by Total Spend - Last 90 Days')
fig2.update_yaxes(autorange="reversed")
fig3 = px.line(df_average_monthly_order_value, x='Period', y='Average Order Value', markers=True, title = 'Average Order Value Each Month of The Year')
fig3.update_yaxes(range=[0, 5000])
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)

# Close the cursor and connection
cur.close()
conn.close()