import pandas as pd
import os


FILE_NAME = "inventory_data.csv"


def load_data():
    """
    Load inventory data from CSV.
    """

    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)

    return pd.DataFrame(
        columns=[
            "Product Name",
            "Category",
            "Quantity",
            "Price",
            "Date Added"
        ]
    )


def save_data(df):
    """
    Save inventory data to CSV.
    """

    df.to_csv(FILE_NAME, index=False)


def total_products(df):
    return len(df)


def total_quantity(df):
    if df.empty:
        return 0
    return int(df["Quantity"].sum())


def total_inventory_value(df):
    if df.empty:
        return 0

    return float((df["Quantity"] * df["Price"]).sum())


def low_stock(df, limit=10):
    if df.empty:
        return df

    return df[df["Quantity"] < limit]


def category_summary(df):

    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("Category")
        .agg(
            Total_Quantity=("Quantity", "sum"),
            Average_Price=("Price", "mean")
        )
        .reset_index()
    )

    return summary
