import pandas as pd
import numpy as np

# Input and output file paths
input_file = r"c:/PROJECTS/smart-store-Brenda\data\raw\products_data.csv"
cleaned_file = r"c:/PROJECTS/smart-store-Brenda\data\prepared\products_data_prepared.csv"

# Expected schema: {column_name: data_type}
expected_schema = {
    "ProductID": "int64",
    "ProductName": "object",   # 'object' is the dtype for strings in pandas
    "Category": "object",
    "UnitPrice": "float64",
    "StockQuantity": "int64",
    "Supplier": "object"
}

# Load CSV
df = pd.read_csv(input_file)

# ✅ Step 1: Verify Number of Columns
if len(df.columns) != len(expected_schema):
    print(f"❌ Warning: Column count mismatch! Expected {len(expected_schema)}, found {len(df.columns)}")

# ✅ Step 2: Verify Column Names and Data Types
for column, expected_type in expected_schema.items():
    if column not in df.columns:
        print(f"❌ Warning: Missing column '{column}'")
    else:
        actual_type = df[column].dtype
        if actual_type != expected_type:
            print(f"❌ Warning: Type mismatch in '{column}'. Expected: {expected_type}, Found: {actual_type}")

print("✅ Schema validation complete.")

# ✅ Step 3: Remove Duplicates
initial_count = len(df)
df.drop_duplicates(inplace=True)
duplicates_removed = initial_count - len(df)
print(f"✅ Removed {duplicates_removed} duplicate rows.")

# ✅ Step 4: Detect & Remove Extreme Values (Outliers)
def remove_outliers(df, column):
    """Removes extreme values using the Interquartile Range (IQR) method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    if not outliers.empty:
        print(f"⚠️ Outliers detected in '{column}':\n{outliers}\n")
    
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Apply outlier removal to numeric columns
numeric_columns = ["ProductID", "UnitPrice", "StockQuantity"]  # Specify numeric columns to check
for col in numeric_columns:
    df = remove_outliers(df, col)

# ✅ Step 5: Save the Cleaned Data
df.to_csv(cleaned_file, index=False)
print(f"🚀 Data cleaned and saved to {cleaned_file}")
