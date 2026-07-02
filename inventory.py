import streamlit as st
import pandas as pd
import os

DATA_FILE = "inventory_data.csv"


# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Product Name",
            "Category",
            "Quantity",
            "Price"
        ])


# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)


def inventory_page():

    st.title("📦 Inventory Management")

    df = load_data()

    menu = st.selectbox(
        "Choose Action",
        ["Add Product", "Edit Product", "Delete Product"]
    )

    # ---------------- ADD PRODUCT ----------------
    if menu == "Add Product":

        st.subheader("➕ Add New Product")

        name = st.text_input("Product Name")
        category = st.text_input("Category")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, step=0.5)

        if st.button("Add Product"):

            new_data = pd.DataFrame([{
                "Product Name": name,
                "Category": category,
                "Quantity": quantity,
                "Price": price
            }])

            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)

            st.success("Product Added Successfully ✅")


    # ---------------- EDIT PRODUCT ----------------
    elif menu == "Edit Product":

        st.subheader("✏️ Edit Product")

        product_list = df["Product Name"].tolist()

        if product_list:

            selected = st.selectbox("Select Product", product_list)

            product_index = df[df["Product Name"] == selected].index[0]

            name = st.text_input("Product Name", df.loc[product_index, "Product Name"])
            category = st.text_input("Category", df.loc[product_index, "Category"])
            quantity = st.number_input("Quantity", value=int(df.loc[product_index, "Quantity"]))
            price = st.number_input("Price", value=float(df.loc[product_index, "Price"]))

            if st.button("Update Product"):

                df.loc[product_index, "Product Name"] = name
                df.loc[product_index, "Category"] = category
                df.loc[product_index, "Quantity"] = quantity
                df.loc[product_index, "Price"] = price

                save_data(df)

                st.success("Product Updated Successfully ✏️")

        else:
            st.warning("No products available to edit")


    # ---------------- DELETE PRODUCT ----------------
    elif menu == "Delete Product":

        st.subheader("🗑️ Delete Product")

        product_list = df["Product Name"].tolist()

        if product_list:

            selected = st.selectbox("Select Product", product_list)

            if st.button("Delete"):

                df = df[df["Product Name"] != selected]
                save_data(df)

                st.success("Product Deleted Successfully 🗑️")

        else:
            st.warning("No products available to delete")
