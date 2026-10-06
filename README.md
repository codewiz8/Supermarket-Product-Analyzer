# Supermarket Product Analyzer
## Data Warehousing and Data Mining Mini Project

### Objective
To analyze supermarket sales data using data warehousing concepts and data mining techniques. The project identifies popular products, category-wise revenue, monthly sales trends, and product combinations that are frequently purchased together.

### Technologies
- Python 3
- Pandas
- Matplotlib
- CSV dataset
- Apriori algorithm (implemented in the project)

### Project Structure
```
Supermarket_Product_Analyzer/
├── supermarket_analyzer.py
├── data/
│   ├── sales.csv
│   ├── products.csv
│   └── customers.csv
├── output/
└── README.md
```

### Data Warehouse
A star-schema style warehouse is generated automatically:
- `fact_sales` — transaction measures
- `dim_product` — product and category information
- `dim_customer` — customer information
- `dim_date` — date-related attributes

### Data Mining
The project implements:
1. Frequent itemset mining using Apriori
2. Association rule generation
3. Support
4. Confidence
5. Lift

### Mac Installation
Open Terminal in the project folder:

```bash
python3 -m pip install pandas matplotlib
```

### Run
```bash
python3 supermarket_analyzer.py
```

### Generated Output
The program creates:
- `dim_product.csv`
- `dim_customer.csv`
- `dim_date.csv`
- `fact_sales.csv`
- `top_products.csv`
- `category_analysis.csv`
- `monthly_analysis.csv`
- `association_rules.csv`
- PNG charts for the analysis

### Mini Project Modules
1. Data collection
2. Data preprocessing
3. Data warehouse construction
4. OLAP-style analysis
5. Product performance analysis
6. Market basket analysis
7. Association-rule mining
8. Visualization
9. Result generation

### Conclusion
The Supermarket Product Analyzer demonstrates how data warehousing can organize transactional supermarket data and how data mining can discover useful purchasing patterns. The results can support product placement, promotions, cross-selling, inventory planning, and sales decisions.
