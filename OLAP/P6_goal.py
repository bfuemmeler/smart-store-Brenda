"""
Module 7: Custom BI Project
Using data from smart_sales.db

This script uses our precomputed cubed data set to get the information 
we need to answer a specific business goal. 

GOAL: Segmenting Customers for Marketing

ACTION: We want to identify customer trends with certain product categories to 
make informed decisions around marketing strategies.

PROCESS: 
Total Spend
Purchase frequency
Recency (last purchase date)
Product category preferences

"""
import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite
conn = sqlite3.connect('C:/Projects/smart-store-Brenda/data/dw/smart_sales.db')

query = """
SELECT 
    c.CustomerID,
    MAX(s.SaleDate) AS last_purchase,
    COUNT(s.TransactionID) AS frequency,
    SUM(s.SaleAmount) AS total_spent
FROM sale s
JOIN customer c ON s.CustomerID = c.CustomerID
GROUP BY c.CustomerID
"""

# Calculate RFM Features
df = pd.read_sql_query(query, conn)
df['last_purchase'] = pd.to_datetime(df['last_purchase'])
df['Recency'] = (pd.to_datetime('today') - df['last_purchase']).dt.days
df = df[['CustomerID', 'Recency', 'frequency', 'total_spent']].rename(
    columns={'frequency': 'Frequency', 'total_spent': 'Monetary'}
)

# Preprocess Data
features = df[['Recency', 'Frequency', 'Monetary']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# Apply KMeans Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
df['Segment'] = kmeans.fit_predict(X_scaled)

# Visualize the Segments
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Recency', y='Monetary', hue='Segment', palette='tab10')
plt.title('Customer Segments by Recency and Monetary Value')
plt.show()

# Pair plot of the RFM features colored by the customer segments
sns.pairplot(df, hue='Segment', vars=['Recency', 'Frequency', 'Monetary'], palette='tab10')
plt.suptitle('Pair Plot of RFM Variables by Segment', y=1.02)
plt.show()

rfm_avg = df.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()

# Bar plot to show the average RFM for each segment
rfm_avg.plot(kind='bar', x='Segment', figsize=(10, 6))
plt.title('Average RFM for Each Customer Segment')
plt.ylabel('Average Value')
plt.xticks(rotation=0)
plt.show()

from mpl_toolkits.mplot3d import Axes3D

# 3D Scatter Plot for Recency, Frequency, and Monetary values colored by Segment
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
scatter = ax.scatter(df['Recency'], df['Frequency'], df['Monetary'], c=df['Segment'], cmap='tab10')

ax.set_xlabel('Recency')
ax.set_ylabel('Frequency')
ax.set_zlabel('Monetary')

plt.title('3D Scatter Plot of RFM Segmentation')
plt.legend(*scatter.legend_elements(), title="Segments")
plt.show()