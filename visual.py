import matplotlib.pyplot as plt
import pandas as pd

def run_visuals(inventory, orders):

    merged = pd.merge(orders, inventory, on="ProductID")
    merged["Revenue"] = merged["Quantity"] * merged["Price"]

    # Top products
    top_products = merged.groupby("ProductName")["Quantity"].sum()

    plt.figure()
    plt.bar(top_products.index, top_products.values)
    plt.title("Top Selling Products")
    plt.show()

    # Monthly sales
    monthly = merged.groupby("Month")["Revenue"].sum()

    plt.figure()
    plt.plot(monthly.index, monthly.values, marker="o")
    plt.title("Monthly Sales")
    plt.show()

    # Category pie
    category = merged.groupby("Category")["Revenue"].sum()

    plt.figure()
    plt.pie(category.values, labels=category.index, autopct="%1.1f%%")
    plt.title("Category Revenue")
    plt.show()