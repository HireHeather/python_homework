import sqlite3
import os
import pandas as pd

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "db", "lesson.db")
conn = sqlite3.connect(db_path)

df = pd.read_sql_query("""
    SELECT line_items.line_item_id, line_items.quantity, line_items.product_id,
           products.product_name, products.price
    FROM line_items
    JOIN products ON line_items.product_id = products.product_id
""", conn)

print(df.head(5))

df['total'] = df['quantity'] * df['price']
print(df.head(5))

summary = df.groupby('product_id').agg(
    order_count=('line_item_id', 'count'),
    total_sales=('total', 'sum'),
    product_name=('product_name', 'first')
)
print(summary.head(5))


summary = summary.sort_values('product_name')
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "order_summary.csv")
summary.to_csv(output_path)

