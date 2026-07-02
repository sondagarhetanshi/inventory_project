import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Inventory Analytics System", layout="wide")

# Initialize session state
if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame(columns=[
        'Product Name', 'Category', 'Quantity', 'Price', 'Date Added'
    ])

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E1E2E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #31333F;
    }
    .alert-box {
        background-color: #FF4B4B;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📦 Inventory System")
    menu = st.selectbox(
        "Menu",
        ["Dashboard", "Add Product", "Edit/Delete Products", "Reports"]
    )
    
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# Function to save data
def save_to_csv():
    if not st.session_state.products.empty:
        st.session_state.products.to_csv('inventory_data.csv', index=False)

# Function to load data
def load_from_csv():
    if os.path.exists('inventory_data.csv'):
        st.session_state.products = pd.read_csv('inventory_data.csv')

# Load existing data
load_from_csv()

# ============== DASHBOARD ==============
if menu == "Dashboard":
    st.title("📊 Inventory Analytics System")
    st.markdown("### Dashboard Overview")
    
    # Search
    search = st.text_input("🔍 Search Product", placeholder="Type to search...")
    
    # Filter products
    df = st.session_state.products.copy()
    if search:
        df = df[df['Product Name'].str.contains(search, case=False, na=False)]
    
    # Key Metrics
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", len(df))
    with col2:
        st.metric("Total Items", df['Quantity'].sum() if not df.empty else 0)
    with col3:
        total_value = (df['Quantity'] * df['Price']).sum() if not df.empty else 0
        st.metric("Total Value", f"₹{total_value:,.0f}")
    with col4:
        avg_price = df['Price'].mean() if not df.empty else 0
        st.metric("Avg Price", f"₹{avg_price:,.2f}")
    
    # Low Stock Alerts
    st.markdown("### ⚠️ Low Stock Alerts")
    low_stock = df[df['Quantity'] < 10] if not df.empty else pd.DataFrame()
    if not low_stock.empty:
        for _, row in low_stock.iterrows():
            st.error(f"🔴 {row['Product Name']} - Only {row['Quantity']} units left!")
    else:
        st.success("✅ All products have sufficient stock")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Bar Chart - Top Products")
        if not df.empty:
            top_products = df.nlargest(5, 'Quantity')
            fig_bar = px.bar(top_products, x='Product Name', y='Quantity',
                           color='Quantity', color_continuous_scale='Blues')
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("### 🥧 Pie Chart - Distribution")
        if not df.empty:
            fig_pie = px.pie(df, values='Quantity', names='Product Name')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Monthly Revenue Chart
    st.markdown("### 📈 Monthly Revenue")
    if not df.empty:
        months = ['Jan', 'Feb', 'Mar', 'Apr']
        revenue = [105000, 15000, 19000, 8000]
        fig_line = px.line(x=months, y=revenue, markers=True)
        fig_line.update_layout(xaxis_title='Month', yaxis_title='Revenue (₹)')
        st.plotly_chart(fig_line, use_container_width=True)

# ============== ADD PRODUCT ==============
elif menu == "Add Product":
    st.title("➕ Add New Product")
    
    with st.form("add_product_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Product Name *")
            category = st.selectbox("Category", ["Electronics", "Furniture", "Accessories", "Other"])
            quantity = st.number_input("Quantity *", min_value=0, step=1)
        
        with col2:
            price = st.number_input("Price (₹) *", min_value=0.0, step=0.01)
            date_added = st.date_input("Date Added", datetime.now())
        
        submitted = st.form_submit_button("💾 Save Product", type="primary")
        
        if submitted:
            if name and quantity >= 0 and price >= 0:
                new_product = pd.DataFrame({
                    'Product Name': [name],
                    'Category': [category],
                    'Quantity': [quantity],
                    'Price': [price],
                    'Date Added': [date_added]
                })
                
                st.session_state.products = pd.concat([
                    st.session_state.products, 
                    new_product
                ], ignore_index=True)
                
                save_to_csv()
                st.success(f"✅ Product '{name}' added successfully!")
                st.balloons()
            else:
                st.error("❌ Please fill all required fields correctly!")

# ============== EDIT/DELETE PRODUCTS ==============
st.markdown("## ✏️ Edit Product")

product_list = st.session_state.products["Product Name"].tolist()

selected_product = st.selectbox(
    "Select Product to Edit",
    product_list,
    key="edit_product"
)

if selected_product:
    index = st.session_state.products[
        st.session_state.products["Product Name"] == selected_product
    ].index[0]

    row = st.session_state.products.loc[index]

    new_name = st.text_input("Product Name", row["Product Name"])
    new_category = st.text_input("Category", row["Category"])
    new_quantity = st.number_input(
        "Quantity",
        min_value=0,
        value=int(row["Quantity"])
    )

    new_cost = st.number_input(
        "Cost Price",
        min_value=0.0,
        value=float(row["Cost Price"])
    )

    new_sell = st.number_input(
        "Selling Price",
        min_value=0.0,
        value=float(row["Selling Price"])
    )

    if st.button("💾 Update Product"):

        st.session_state.products.loc[index, "Product Name"] = new_name
        st.session_state.products.loc[index, "Category"] = new_category
        st.session_state.products.loc[index, "Quantity"] = new_quantity
        st.session_state.products.loc[index, "Cost Price"] = new_cost
        st.session_state.products.loc[index, "Selling Price"] = new_sell

        save_to_csv()

        st.success("✅ Product Updated Successfully")
        st.rerun()
# ============== REPORTS ==============
elif menu == "Reports":
    st.title("📑 Reports & Export")
    
    if st.session_state.products.empty:
        st.warning("No data available for reports!")
    else:
        # Export options
        st.markdown("### Download Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = st.session_state.products.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"inventory_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                type="primary"
            )
        
        with col2:
            if st.button("📊 Generate Summary Report"):
                st.markdown("### Summary Statistics")
                st.write(st.session_state.products.describe())
        
        st.markdown("---")
        st.markdown("### Category-wise Summary")
        if not st.session_state.products.empty:
            category_summary = st.session_state.products.groupby('Category').agg({
                'Quantity': 'sum',
                'Price': 'mean'
            }).reset_index()
            st.dataframe(category_summary, use_container_width=True)
