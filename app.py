import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(
    page_title="Inventory Analytics Pro",
    page_icon="📦",
    layout="wide"
)

# ---------------- Session ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "products" not in st.session_state:
    st.session_state.products = pd.DataFrame(
        columns=[
            "Product Name",
            "Category",
            "Quantity",
            "Price",
            "Date Added"
        ]
    )

USERNAME = "admin"
PASSWORD = "admin123"

# ---------------- CSS ----------------
st.markdown("""
<style>
.main{
    background:#0E1117;
}

h1,h2,h3{
    color:white;
}

.stButton>button{
    width:100%;
    border-radius:10px;
}

div[data-testid="metric-container"]{
    background:#262730;
    border-radius:10px;
    padding:15px;
}
</style>
""",unsafe_allow_html=True)

# ---------------- CSV ----------------

def save_data():
    st.session_state.products.to_csv(
        "inventory_data.csv",
        index=False
    )

def load_data():
    if os.path.exists("inventory_data.csv"):
        st.session_state.products=pd.read_csv(
            "inventory_data.csv"
        )

load_data()
# ---------------- Login ----------------

if not st.session_state.logged_in:

    st.title("🔐 Inventory Analytics Pro")

    st.markdown("### Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True
            st.success("✅ Login Successful")
            st.rerun()

        else:

            st.error("❌ Invalid Username or Password")

    st.stop()

# ---------------- Sidebar ----------------

with st.sidebar:

    st.title("📦 Inventory Pro")

    st.success("Logged in as Admin")

    menu = st.radio(
        "Select Menu",
        [
            "Dashboard",
            "Add Product",
            "Edit/Delete Product",
            "Reports"
        ]
    )

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.rerun()
        # ================= DASHBOARD =================

if menu == "Dashboard":

    st.title("📊 Inventory Dashboard")

    search = st.text_input("🔍 Search Product")

    df = st.session_state.products.copy()

    if search:
        df = df[df["Product Name"].str.contains(search, case=False, na=False)]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total Products", len(df))

    with col2:
        total_qty = df["Quantity"].sum() if not df.empty else 0
        st.metric("📦 Total Quantity", int(total_qty))

    with col3:
        total_value = (df["Quantity"] * df["Price"]).sum() if not df.empty else 0
        st.metric("💰 Inventory Value", f"₹{total_value:,.0f}")

    st.markdown("---")

    st.subheader("⚠️ Low Stock")

    if not df.empty:
        low = df[df["Quantity"] < 10]

        if low.empty:
            st.success("✅ No Low Stock Products")

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
                title="Product Quantity"
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

        st.info("No Products Available. Please Add Products.")
        # ================= ADD PRODUCT =================

elif menu == "Add Product":

    st.title("➕ Add New Product")

    with st.form("add_product", clear_on_submit=True):

        name = st.text_input("Product Name")

        category = st.selectbox(
            "Category",
            ["Electronics", "Furniture", "Accessories", "Other"]
        )

        quantity = st.number_input(
            "Quantity",
            min_value=0,
            step=1
        )

        price = st.number_input(
            "Price (₹)",
            min_value=0.0,
            step=1.0
        )

        date = st.date_input("Date Added")

        submit = st.form_submit_button("💾 Save Product")

        if submit:

            new_data = pd.DataFrame({

                "Product Name":[name],
                "Category":[category],
                "Quantity":[quantity],
                "Price":[price],
                "Date Added":[date]

            })

            st.session_state.products = pd.concat(
                [st.session_state.products, new_data],
                ignore_index=True
            )

            save_data()

            st.success("✅ Product Added Successfully")
            st.balloons()
            # ================= EDIT / DELETE PRODUCT =================

elif menu == "Edit/Delete Product":

    st.title("✏️ Edit / Delete Product")

    if st.session_state.products.empty:

        st.warning("No products available.")

    else:

        product = st.selectbox(
            "Select Product",
            st.session_state.products["Product Name"]
        )

        index = st.session_state.products[
            st.session_state.products["Product Name"] == product
        ].index[0]

        row = st.session_state.products.loc[index]

        new_name = st.text_input(
            "Product Name",
            value=row["Product Name"]
        )

        new_category = st.selectbox(
            "Category",
            ["Electronics","Furniture","Accessories","Other"],
            index=["Electronics","Furniture","Accessories","Other"].index(row["Category"])
        )

        new_quantity = st.number_input(
            "Quantity",
            value=int(row["Quantity"]),
            min_value=0
        )

        new_price = st.number_input(
            "Price",
            value=float(row["Price"]),
            min_value=0.0
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Update Product"):

                st.session_state.products.loc[index,"Product Name"] = new_name
                st.session_state.products.loc[index,"Category"] = new_category
                st.session_state.products.loc[index,"Quantity"] = new_quantity
                st.session_state.products.loc[index,"Price"] = new_price

                save_data()

                st.success("✅ Product Updated")
                st.rerun()

        with col2:

            if st.button("🗑 Delete Product"):

                st.session_state.products = st.session_state.products.drop(index).reset_index(drop=True)

                save_data()

                st.success("✅ Product Deleted")
                st.rerun()
                # ================= REPORTS =================

elif menu == "Reports":

    st.title("📑 Inventory Reports")

    if st.session_state.products.empty:

        st.warning("No Products Available!")

    else:

        df = st.session_state.products.copy()

        # ===== Metrics =====
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📦 Total Products", len(df))

        with col2:
            st.metric("📦 Total Quantity", int(df["Quantity"].sum()))

        with col3:
            total_value = (df["Quantity"] * df["Price"]).sum()
            st.metric("💰 Total Inventory Value", f"₹{total_value:,.2f}")

        st.markdown("---")

        # ===== Category Summary =====
        st.subheader("📊 Category Summary")

        category = df.groupby("Category").agg({
            "Quantity":"sum",
            "Price":"mean"
        }).reset_index()

        category.columns=[
            "Category",
            "Total Quantity",
            "Average Price"
        ]

        st.dataframe(category, use_container_width=True)

        st.markdown("---")

        # ===== Complete Inventory =====
        st.subheader("📋 Inventory Data")

        st.dataframe(df, use_container_width=True)

        st.markdown("---")

        # ===== CSV Download =====

        csv = df.to_csv(index=False)

        st.download_button(
            "📥 Download CSV",
            csv,
            "inventory_report.csv",
            "text/csv"
        )
        import streamlit as st
import pandas as pd

from dashboard import dashboard_page
from inventory import inventory_page

DATA_FILE = "inventory_data.csv"


# Load data
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=[
            "Product Name",
            "Category",
            "Quantity",
            "Price"
        ])


def main():

    st.set_page_config(
        page_title="Inventory Analytics System",
        layout="wide"
    )

    st.sidebar.title("📦 Inventory System")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Inventory Management"]
    )

    df = load_data()

    if menu == "Dashboard":
        dashboard_page(df)

    elif menu == "Inventory Management":
        inventory_page()


if __name__ == "__main__":
    main()
