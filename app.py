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
