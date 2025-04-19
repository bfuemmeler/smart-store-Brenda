import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to SQLite
conn = sqlite3.connect('C:/Projects/smart-store-Brenda/data/dw/smart_sales.db')

# SQL query extracting the numeric month
query = """
SELECT 
    p.Category,
    strftime('%m', s.SaleDate) AS month_num,
    s.SaleAmount
FROM sale s
JOIN product p ON s.ProductID = p.ProductID
"""

df = pd.read_sql_query(query, conn)
conn.close()

# Map numeric month to month name
month_map = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
}
df['month'] = df['month_num'].map(month_map)

# Aggregate
result = df.groupby(['Category', 'month'])['SaleAmount'].sum().reset_index()

# Order months properly
month_order = list(month_map.values())
df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
result['month'] = pd.Categorical(result['month'], categories=month_order, ordered=True)

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(data=result, x='Category', y='SaleAmount', hue='month')
plt.xticks(rotation=45)
plt.title('Sales by Category and Month')
plt.tight_layout()
plt.show()