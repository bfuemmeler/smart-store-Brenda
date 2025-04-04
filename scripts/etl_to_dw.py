import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("data/dw")
DB_PATH = pathlib.Path ("smart_sales.db")
DB_PATH = DW_DIR.joinpath("smart_sales.db").resolve()
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

DB_PATH = DB_PATH.resolve()
print(f"Absolute Database Path: {DB_PATH}")  

DW_DIR.mkdir(parents=True, exist_ok=True)
if not DB_PATH.exists():
    DB_PATH.touch()
    print(f"Created database file at: {DB_PATH}")

print(f"Using Database Path: {DB_PATH}")

# ✅ Try connecting to SQLite
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version();")  # Test connection
    print("Database connected successfully!", cursor.fetchone())
    
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

def create_schema(cursor: sqlite3.Cursor) -> None:
        """Create tables in the data warehouse if they don't exist."""
cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            CustomerID INTEGER PRIMARY KEY,
            Name TEXT,
            Region TEXT,
            JoinDate TEXT,
            LoyaltyPoints INTEGER,
            PreferredContactMethod TEXT,
            StandardDateTime TEXT
        )
    """)
    
cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            ProductID INTEGER PRIMARY KEY,
            ProductName TEXT,
            Category TEXT,
            UnitPrice REAL,
            StockQuantity REAL,
            Supplier TEXT
        )
    """)
    
cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            TransactionID INTEGER PRIMARY KEY,
            SaleDate TEXT,
            CustomerID INTEGER,
            ProductID INTEGER,
            StoreID INTEGER,
            CampaignID INTEGER,
            SaleAmount REAL,
            BonusPoints REAL,
            PaymentType TEXT,
            FOREIGN KEY (CustomerID) REFERENCES customer (CustomerID),
            FOREIGN KEY (ProductID) REFERENCES product (ProductID)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("C:\Projects\smart-store-Brenda\data\prepared\customers_data_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("C:\Projects\smart-store-Brenda\data\prepared\products_data_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("C:\Projects\smart-store-Brenda\data\prepared\sales_data_prepared.csv"))

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()