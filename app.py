import streamlit as st
from data import inventory, orders
from analysis import run_analysis
from visual import run_visuals

# Page settings
st.set_page_config(page_title="Inventory Dashboard", layout="wide")

st.title("📊 Smart Inventory Analytics Dashboard")
st.write("Welcome! aa project pandas + streamlit thi banavyo chhe 🚀")

# ======================
# SHOW DATA SECTION
# ======================
st.sidebar.header("Options")

show_inventory = st.sidebar.checkbox("Show Inventory Data")
show_orders = st.sidebar.checkbox("Show Orders Data")

if show_inventory:
    st.subheader("📦 Inventory Data")
    st.dataframe(inventory)

if show_orders:
    st.subheader("🧾 Orders Data")
    st.dataframe(orders)

# ======================
# ANALYSIS SECTION
# ======================
st.subheader("📈 Analysis")

run_analysis(inventory, orders)

# ======================
# VISUALIZATION SECTION
# ======================
st.subheader("📊 Charts")

run_visuals(inventory, orders)
import streamlit as st
from data import inventory, orders
from analysis import run_analysis
from visual import run_visuals
import pandas as pd

st.set_page_config(page_title="Inventory Dashboard", layout="wide")

st.title("📊 Smart Inventory Dashboard (Level 6)")

# =========================
# MERGE DATA
# =========================
merged = pd.merge(orders, inventory, on="ProductID")
merged["Revenue"] = merged["Quantity"] * merged["Price"]

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

month_filter = st.sidebar.multiselect(
    "Select Month",
    merged["Month"].unique(),
    default=merged["Month"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    merged["Category"].unique(),
    default=merged["Category"].unique()
)

# Apply filters
filtered = merged[
    (merged["Month"].isin(month_filter)) &
    (merged["Category"].isin(category_filter))
]

# =========================
# KPI CARDS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"{filtered['Revenue'].sum():,.0f}")
col2.metric("Total Orders", len(filtered))
col3.metric("Total Products", filtered["ProductName"].nunique())

# =========================
# TABLE
# =========================
st.subheader("📦 Filtered Data")
st.dataframe(filtered)

# =========================
# ANALYSIS
# =========================
st.subheader("📈 Analysis")

top_products = filtered.groupby("ProductName")["Quantity"].sum()

st.write("Top Products")
st.bar_chart(top_products)

monthly = filtered.groupby("Month")["Revenue"].sum()

st.write("Monthly Sales")
st.line_chart(monthly)

# =========================
# CATEGORY PIE DATA
# =========================
st.write("Category Revenue")

category = filtered.groupby("Category")["Revenue"].sum()
st.bar_chart(category)

st.success("Dashboard Ready 🚀")
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Inventory Pro Dashboard", layout="wide")

st.title("📊 Inventory Analytics Pro (Level 7) 🚀")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload CSV (Orders Data)", type=["csv"])

if uploaded_file:
    orders = pd.read_csv(uploaded_file)
else:
    # fallback demo data
    orders = pd.DataFrame({
        "OrderID": [1,2,3,4,5],
        "ProductID": [101,102,103,102,104],
        "Quantity": [2,10,5,20,3],
        "Month": ["Jan","Jan","Feb","Feb","Mar"]
    })

inventory = pd.DataFrame({
    "ProductID": [101,102,103,104,105],
    "ProductName": ["Laptop","Mouse","Keyboard","Chair","Table"],
    "Category": ["Electronic","Electronic","Electronic","Furniture","Furniture"],
    "Stock": [50,200,150,80,40],
    "Price": [50000,500,1000,3000,5000]
})

# =========================
# MERGE DATA
# =========================
merged = pd.merge(orders, inventory, on="ProductID")
merged["Revenue"] = merged["Quantity"] * merged["Price"]

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"{merged['Revenue'].sum():,.0f}")
col2.metric("Total Orders", len(merged))
col3.metric("Products", merged["ProductName"].nunique())

# =========================
# TABLE
# =========================
st.subheader("📦 Data Preview")
st.dataframe(merged)

# =========================
# CHARTS
# =========================
st.subheader("📊 Top Products")
st.bar_chart(merged.groupby("ProductName")["Quantity"].sum())

st.subheader("📈 Monthly Sales")
st.line_chart(merged.groupby("Month")["Revenue"].sum())

st.subheader("🏷 Category Revenue")
st.bar_chart(merged.groupby("Category")["Revenue"].sum())

# =========================
# DOWNLOAD EXCEL REPORT
# =========================
def convert_df(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')
    return output.getvalue()

excel_data = convert_df(merged)

st.download_button(
    label="📥 Download Excel Report",
    data=excel_data,
    file_name="inventory_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("Dashboard Ready 🚀")
from ai_model import predict_sales
st.subheader("🤖 AI Prediction")

if st.button("Predict Next Month Sales"):
    result = predict_sales()
    st.success(f"Predicted Sales: ₹ {result:,.0f}")
import streamlit as st
from auth import register, login
from database import create_db

create_db()

st.title("🔐 Inventory System Login")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ======================
# REGISTER
# ======================
if choice == "Register":
    st.subheader("Create New Account")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Register"):
        register(user, pwd)
        st.success("Account Created Successfully!")

# ======================
# LOGIN
# ======================
if choice == "Login":
    st.subheader("Login to Dashboard")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(user, pwd):
            st.success("Login Successful 🚀")

            st.subheader("📊 Inventory Dashboard")

            st.info("Now you are inside secure system!")

        else:
            st.error("Invalid Credentials ❌")