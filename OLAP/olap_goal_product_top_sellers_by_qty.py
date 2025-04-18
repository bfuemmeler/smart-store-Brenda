"""
Module 6: OLAP Goal Script (uses cubed results)

This script uses our precomputed cubed data set to get the information 
we need to answer a specific business goal. 

GOAL: Identify products with highest number of units sold. This helps determine which products
are the best sellers in terms of volume. This drives inventory management and marketing strategies.

ACTION: This can help inform inventory decisions, optimize promotions, 
and understand purchasing patterns.

PROCESS: 
Group transactions by ProductName and StoreID


"""

import pandas as pd
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# DB path
DB_PATH = Path("data/dw/smart_sales.db")

# Connect to SQLite DB
conn = sqlite3.connect(DB_PATH)

# Join sale and product tables to get ProductName
query = """
SELECT 
    p.ProductName,
    s.StoreID
FROM sale s
JOIN product p ON s.ProductID = p.ProductID
"""

sales_df = pd.read_sql_query(query, conn)
conn.close()

# Create pivot table: rows = ProductName, cols = StoreID
pivot_table = sales_df.pivot_table(
    index="ProductName",
    columns="StoreID",
    aggfunc="size",
    fill_value=0
)

# Display pivot
print(pivot_table)

# Save pivot to CSV
pivot_table.to_csv("data/olap_cubing_outputs/pivot_transactions_productname_store.csv")

# Plot heatmap
plt.figure(figsize=(14, max(6, 0.5 * len(pivot_table))))  # adjust height based on # of products
sns.heatmap(
    pivot_table,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    linewidths=.5,
    linecolor="gray"
)

plt.title("Transaction Volume by Product Name and Store", fontsize=14)
plt.xlabel("StoreID")
plt.ylabel("ProductName")
plt.tight_layout()

# Save heatmap
plt.savefig("data/olap_cubing_outputs/heatmap_productname_store.png")
plt.show()