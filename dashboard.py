import streamlit as st
import plotly.express as px
from utils import (
    total_products,
    total_quantity,
    total_inventory_value,
    low_stock,
)

def dashboard_page(df):

    st.title("📊 Inventory Dashboard")

    search = st.text_input("🔍 Search Product")

    if search:
        df = df[df["Product Name"].str.contains(search, case=False, na=False)]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total Products", total_products(df))

    with col2:
        st.metric("📦 Total Quantity", total_quantity(df))

    with col3:
        st.metric(
            "💰 Inventory Value",
            f"₹{total_inventory_value(df):,.2f}"
        )

    st.markdown("---")

    st.subheader("⚠️ Low Stock Products")

    low = low_stock(df)

    if low.empty:
        st.success("All products have sufficient stock.")
    else:
        st.dataframe(low, use_container_width=True)

    st.markdown("---")

    if not df.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                df,
                x="Product Name",
                y="Quantity",
                color="Category",
                title="Stock Quantity"
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            fig2 = px.pie(
                df,
                values="Quantity",
                names="Category",
                title="Category Distribution"
            )

            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("No Products Found.")
