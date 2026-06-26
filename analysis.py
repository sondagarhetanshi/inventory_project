import pandas as pd

def run_analysis(inventory, orders):

    merged = pd.merge(orders, inventory, on="ProductID")
    merged["Revenue"] = merged["Quantity"] * merged["Price"]

    print("\n===== ANALYSIS =====")

    print("Total Revenue:", merged["Revenue"].sum())

    top_products = merged.groupby("ProductName")["Quantity"].sum()
    print("\nTop Products:")
    print(top_products.sort_values(ascending=False))

    print("\nMonthly Revenue:")
    print(merged.groupby("Month")["Revenue"].sum())

    print("\nBest Product:", top_products.idxmax())