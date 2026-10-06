
import os
from itertools import combinations
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)

def load_data():
    sales = pd.read_csv(os.path.join(DATA, "sales.csv"))
    products = pd.read_csv(os.path.join(DATA, "products.csv"))
    customers = pd.read_csv(os.path.join(DATA, "customers.csv"))
    sales["date"] = pd.to_datetime(sales["date"])
    return sales, products, customers

def build_warehouse(sales, products, customers):
    # Star-schema style dimensions and fact table
    dim_product = products[["product_id","product_name","category","unit_price"]].copy()
    dim_customer = customers.copy()
    dim_date = pd.DataFrame({"date": sales["date"].drop_duplicates().sort_values()})
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["day"] = dim_date["date"].dt.day
    fact_sales = sales[["sale_id","transaction_id","date","customer_id","product_id",
                        "quantity","unit_price","discount_percent","total_amount"]].copy()

    dim_product.to_csv(os.path.join(OUT,"dim_product.csv"), index=False)
    dim_customer.to_csv(os.path.join(OUT,"dim_customer.csv"), index=False)
    dim_date.to_csv(os.path.join(OUT,"dim_date.csv"), index=False)
    fact_sales.to_csv(os.path.join(OUT,"fact_sales.csv"), index=False)
    return fact_sales, dim_product, dim_customer, dim_date

def top_products(fact, products):
    result = fact.groupby("product_id")["quantity"].sum().reset_index()
    result = result.merge(products[["product_id","product_name","category"]], on="product_id")
    result = result.sort_values("quantity", ascending=False)
    result.to_csv(os.path.join(OUT,"top_products.csv"), index=False)

    plt.figure(figsize=(10,5))
    top = result.head(10).sort_values("quantity")
    plt.barh(top["product_name"], top["quantity"])
    plt.title("Top 10 Products by Quantity Sold")
    plt.xlabel("Quantity Sold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT,"top_products.png"))
    plt.close()
    return result

def category_analysis(fact, products):
    result = fact.merge(products[["product_id","category"]], on="product_id")
    result = result.groupby("category").agg(
        quantity_sold=("quantity","sum"),
        revenue=("total_amount","sum")
    ).reset_index().sort_values("revenue", ascending=False)
    result.to_csv(os.path.join(OUT,"category_analysis.csv"), index=False)

    plt.figure(figsize=(9,5))
    plt.bar(result["category"], result["revenue"])
    plt.title("Revenue by Product Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT,"category_revenue.png"))
    plt.close()
    return result

def monthly_analysis(fact):
    result = fact.groupby(fact["date"].dt.to_period("M")).agg(
        quantity_sold=("quantity","sum"),
        revenue=("total_amount","sum")
    ).reset_index()
    result["date"] = result["date"].astype(str)
    result.to_csv(os.path.join(OUT,"monthly_analysis.csv"), index=False)

    plt.figure(figsize=(10,5))
    plt.plot(result["date"], result["revenue"], marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT,"monthly_revenue.png"))
    plt.close()
    return result

def apriori(transactions, min_support=0.08):
    """Simple Apriori implementation. Returns itemsets with support."""
    total = len(transactions)
    counts = defaultdict(int)
    for t in transactions:
        for item in t:
            counts[frozenset([item])] += 1

    current = {k:v/total for k,v in counts.items() if v/total >= min_support}
    all_freq = dict(current)
    k = 2

    while current:
        prev_sets = list(current.keys())
        candidates = set()
        for i in range(len(prev_sets)):
            for j in range(i+1, len(prev_sets)):
                union = prev_sets[i] | prev_sets[j]
                if len(union) == k:
                    # Apriori pruning: all (k-1) subsets must be frequent
                    valid = all(frozenset(s) in current for s in combinations(union, k-1))
                    if valid:
                        candidates.add(frozenset(union))

        next_counts = defaultdict(int)
        for t in transactions:
            for c in candidates:
                if c.issubset(t):
                    next_counts[c] += 1

        current = {c:n/total for c,n in next_counts.items()
                   if n/total >= min_support}
        all_freq.update(current)
        k += 1
    return all_freq

def association_rules(freq, min_confidence=0.35):
    rules = []
    for itemset, support in freq.items():
        if len(itemset) < 2:
            continue
        items = list(itemset)
        for r in range(1, len(items)):
            for left_tuple in combinations(items, r):
                left = frozenset(left_tuple)
                right = itemset - left
                left_support = freq.get(left, 0)
                if left_support == 0:
                    continue
                confidence = support / left_support
                right_support = freq.get(right, 0)
                lift = confidence / right_support if right_support else 0
                if confidence >= min_confidence:
                    rules.append({
                        "antecedent": ", ".join(sorted(left)),
                        "consequent": ", ".join(sorted(right)),
                        "support": round(support, 4),
                        "confidence": round(confidence, 4),
                        "lift": round(lift, 4)
                    })
    return pd.DataFrame(rules).sort_values(
        ["lift","confidence"], ascending=False
    ) if rules else pd.DataFrame()

def market_basket_mining(sales, products):
    merged = sales.merge(products[["product_id","product_name"]], on="product_id")
    transactions = []
    for _, group in merged.groupby("transaction_id"):
        transactions.append(set(group["product_name"]))

    freq = apriori(transactions, min_support=0.08)
    rules = association_rules(freq, min_confidence=0.35)
    if rules.empty:
        print("No association rules found. Try lower thresholds.")
        return rules
    rules.to_csv(os.path.join(OUT,"association_rules.csv"), index=False)
    return rules

def run_all():
    sales, products, customers = load_data()
    fact, dim_product, dim_customer, dim_date = build_warehouse(sales, products, customers)

    tp = top_products(fact, products)
    ca = category_analysis(fact, products)
    ma = monthly_analysis(fact)
    rules = market_basket_mining(sales, products)

    print("\n=== SUPERMARKET PRODUCT ANALYZER ===")
    print("\nTop 10 Products:")
    print(tp.head(10)[["product_name","category","quantity"]].to_string(index=False))
    print("\nCategory Analysis:")
    print(ca.to_string(index=False))
    print("\nMonthly Analysis:")
    print(ma.to_string(index=False))
    if not rules.empty:
        print("\nTop Association Rules:")
        print(rules.head(10).to_string(index=False))
    print(f"\nOutput files saved in: {OUT}")

if __name__ == "__main__":
    run_all()
