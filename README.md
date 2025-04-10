## Module 3 smart-sales-docs

## 1. Get Started

### Verify You've Created a Local Project Virtual Environment

Create a virtual environment:
```shell
python -m venv .venv
```

Verify a new folder named .venv is available. You must be able to see hidden files and folders on your machine. 

### Activate the Virtual Environment (Always)

Every time you open a new terminal and work on the project, be sure to activate the project virtual environment. 

In Windows / PowerShell:

```shell
.\.venv\Scripts\activate
```
### Verify You've Installed All Required Packages (As Needed)

With the virtual environment activated, install the most current versions of the required packages which should be listed in your requirements.txt:

```shell
python -m pip install --upgrade -r requirements.txt
```
-----

## 2. Implement and Test General DataScrubber Class

### Run the Test Script

In your VS Code terminal, with your local project virtual environment **active** (and all necessary packages installed),
run the test script with the following command. 

In Windows / PowerShell:

```shell
py tests\test_data_scrubber.py
```

The first time you run it, all tests will not pass correctly. 

### Finish DataScrubber Until All Tests Pass Successfully

Edit your scripts\data_scrubber.py file to complete the TODO actions. Verify by running the test script. 
Once all tests pass, you are ready to use the Data Scrubber in your data_prep.py (or other data preparation script). 

-----

## 3. Complete all Data Preparation

For this step, use pandas and the DataScrubber class as needed to clean and prepare each of the raw data files. 

We have an example data_prep.py file provided that illustrates common cleaning tasks and how to use the DataScrubber class. 

Right now, all files are cleaned in a single scripts/data_prep.py file, but you may find it better to have smaller files, maybe one per raw data table. 

Given the examples and the work done previously, read, clean, and preprocess all your raw data files and save the prepared versions in the data/prepared folder. 

We recommand a naming scheme - following this will make future assignments a bit easier as we will use these file names and locations, 
however, you are welcome to vary the names. Your future scripts will need to correctly reflect your folder and file naming conventions. 
Changing is harder and better for learning. If new, please follow our folder and file naming conventions exactly.

If your file is in the scripts folder, with a name of data_prep.py, you can run it with the appropriate command from a VS Code terminal open in the root project folder:

In Windows / PowerShell:

```shell
py scripts\data_prep.py
```
### P4 Create and Populate DW
# Plan Data Warehouse
  Design Schema- Star
  Fact Table- Sales
  Dimension Tables- Products and Customers
  Upload CSV files to DB for SQLite
  Create smart_sales.db file within data/dw
# Define, Create, Populate DW Schema
  Create etl_to_dw.py script
  Implement script, debug & run

# Validate Data Warehouse
# Document & Submit Work

### P5 Cross-Platform Reporting with Power BI
## 1 Install SQLite ODBC Driver and configure DSN to link Power BI to database
## 2 In Power BI: Get Data > Select ODBC > Choose SQLite DSN, load customer, product & sales tables
## 3 In Power BI: Open Transform Data > Advanced Editor > add SQL code
    "SELECT customer.CustomerID, customer.Name, SUM(sale.SaleAmount) AS total_revenue FROM customer INNER JOIN sale ON customer.CustomerID = sale.CustomerID GROUP BY customer.CustomerID, customer.Name#(lf)"
    Name the table Top Customers
## 4 Load & review results

## 5 Slice, Dice Drilldown
# Add a date range slicer
    Add the Slicer visual, drag SaleDate column into Slicer
    With Date Field selected, it should let you toggle the Between dates to filter the range
    ![alt text](image-1.png)
      ***Use ChatGPT notes to change field from TEXT to DATE so the slicer will allow "between"
# Create a matrix visual for sales by product & region
    Add the Matrix visual, drag Product into Rows, drag Region into Columns, Drag SaleAmount into Values
    ![alt text](image.png)
# Enable drill-through to explore sales by year, quarter, month
    Add new visual and select Drillthrough. Drag SaleDate to Field
    Drag Year, Quarter, Month to Drillthrough fields
    ![alt text](image-3.png)

## 6 Create Interactive Visualizations
# Create bar chart for Top Customers
  Add visual for Stacked Bar Chart. Choose Top Customers data 
  ![alt text](image-2.png)

# Create line chart for Sales Trends
  Add visual for Line Chart. I chose Category, Sale Amount & Quarter
  ![alt text](image-4.png)

# Add a slicer for product categories
  Add visual for Slicer. I used Category and Product Name
  ![alt text](image-5.png)

## Screenshot of Power BI Model View
![alt text](image-7.png)

## Screenshot of Query Results
![alt text](image-8.png)

## Screenshot of Final Dashboard/Charts
![alt text](image-6.png)

In VS Code, activate .venv   .\.venv\Scripts\activate
git add .
git commit -m "update ReadMe, add PowerBI screenshots"
git push


