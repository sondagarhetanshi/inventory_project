import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Inventory Analytics System", layout="wide")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame(columns=[
        'Product Name', 'Category', 'Quantity', 'Cost Price', 'Selling Price', 'Date Added'
    ])

# Login credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

# Login Function
def check_login(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

# Logout Function
def logout():
    st.session_state.logged_in = False
    st.rerun()

# ============== LOGIN PAGE ==============
if not st.session_state.logged_in:
    st.title(" Login Page")
    st.markdown("### Please login to continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("####  Inventory System Login")
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            login_button = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
            
            if login_button:
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.success("✅ Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
        
        st.markdown("---")
        st.info("💡 **Demo Credentials:**\n- Username: `admin`\n- Password: `admin123`")

# ============== MAIN APP (After Login) ==============
else:
    # Custom CSS
    st.markdown("""
        <style>
        .metric-card {
            background-color: #1E1E2E;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #31333F;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("📦 Inventory System")
        st.markdown("---")
        st.markdown("**Created by: Hetanshi Sondagar**")
        st.markdown("---")
        st.success(f"✅ Welcome, **{VALID_USERNAME}**!")
        st.markdown("---")
        
        menu = st.selectbox(
            "Menu",
            [" Dashboard", "➕ Add Product", "️ Edit/Delete Products", "💰 Profit Analysis", "📑 Reports"]
        )
        
        st.markdown("---")
        if st.button(" Logout", type="secondary", use_container_width=True):
            logout()

    # Function to save data
    def save_to_csv():
        if not st.session_state.products.empty:
            st.session_state.products.to_csv('inventory_data.csv', index=False)

    # Function to load data
    def load_from_csv():
        if os.path.exists('inventory_data.csv'):
            df = pd.read_csv('inventory_data.csv')
            # Handle backward compatibility: if old 'Price' column exists but no 'Cost Price'/'Selling Price'
            if 'Price' in df.columns and 'Cost Price' not in df.columns:
                df['Cost Price'] = df['Price']
                df['Selling Price'] = df['Price']  # Assume selling price = cost price for old data
                df = df.drop(columns=['Price'])
            st.session_state.products = df

    # Load existing data
    load_from_csv()

    # Helper function to ensure required columns exist
    def ensure_profit_columns(df):
        if df.empty:
            return df
        if 'Cost Price' not in df.columns:
            df['Cost Price'] = 0.0
        if 'Selling Price' not in df.columns:
            df['Selling Price'] = 0.0
        if 'Profit' not in df.columns:
            df['Profit'] = (df['Selling Price'] - df['Cost Price']) * df['Quantity']
        if 'Profit %' not in df.columns:
            df['Profit %'] = ((df['Selling Price'] - df['Cost Price']) / df['Cost Price'].replace(0, 1) * 100).round(2)
        return df

    # ============== DASHBOARD ==============
    if menu == "📊 Dashboard":
        st.title("📊 Inventory Analytics Dashboard")
        st.markdown("### Overview")
        
        # Search
        search = st.text_input(" Search Product", placeholder="Type to search...")
        
        # Filter products
        df = st.session_state.products.copy()
        if search:
            df = df[df['Product Name'].str.contains(search, case=False, na=False)]
        
        # Ensure profit columns exist
        df = ensure_profit_columns(df)
        
        # Key Metrics
        st.markdown("### 📈 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Products", len(df))
        with col2:
            st.metric("Total Items", df['Quantity'].sum() if not df.empty else 0)
        with col3:
            total_investment = (df['Cost Price'] * df['Quantity']).sum() if not df.empty else 0
            st.metric("Total Investment", f"₹{total_investment:,.0f}")
        with col4:
            total_sales = (df['Selling Price'] * df['Quantity']).sum() if not df.empty else 0
            st.metric("Total Sales Value", f"{total_sales:,.0f}")
        
        # Profit Metrics
        st.markdown("### 💰 Profit/Loss Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_profit = df['Profit'].sum() if not df.empty else 0
            st.metric("Total Profit", f"₹{total_profit:,.0f}")
        with col2:
            avg_profit_pct = df['Profit %'].mean() if not df.empty else 0
            st.metric("Avg Profit %", f"{avg_profit_pct:.2f}%")
        with col3:
            profit_margin = (total_profit / total_investment * 100) if total_investment > 0 else 0
            st.metric("Profit Margin", f"{profit_margin:.2f}%")
        
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
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Profit by Product")
                fig_profit = px.bar(
                    df, 
                    x='Product Name', 
                    y='Profit',
                    color='Profit',
                    color_continuous_scale='RdYlGn',
                    title='Profit per Product'
                )
                st.plotly_chart(fig_profit, use_container_width=True)
            
            with col2:
                st.markdown("### 🥧 Sales Distribution")
                fig_pie = px.pie(df, values='Selling Price', names='Product Name')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Monthly Revenue Chart
            st.markdown("### 📈 Monthly Revenue")
            months = ['Jan', 'Feb', 'Mar', 'Apr']
            revenue = [105000, 15000, 19000, 8000]
            fig_line = px.line(x=months, y=revenue, markers=True)
            fig_line.update_layout(xaxis_title='Month', yaxis_title='Revenue (₹)')
            st.plotly_chart(fig_line, use_container_width=True)

    # ============== ADD PRODUCT ==============
    elif menu == "➕ Add Product":
        st.title("➕ Add New Product")
        
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Product Name *")
                category = st.selectbox("Category", ["Electronics", "Furniture", "Accessories", "Other"])
                quantity = st.number_input("Quantity *", min_value=0, step=1)
            
            with col2:
                cost_price = st.number_input("Cost Price (₹) *", min_value=0.0, step=0.01, help="Aapne ketle price ma kharidiyo")
                selling_price = st.number_input("Selling Price (₹) *", min_value=0.0, step=0.01, help="Ketle price ma vechiyo")
                date_added = st.date_input("Date Added", datetime.now())
            
            submitted = st.form_submit_button("💾 Save Product", type="primary")
            
            if submitted:
                if name and quantity >= 0 and cost_price >= 0 and selling_price >= 0:
                    new_product = pd.DataFrame({
                        'Product Name': [name],
                        'Category': [category],
                        'Quantity': [quantity],
                        'Cost Price': [cost_price],
                        'Selling Price': [selling_price],
                        'Date Added': [date_added]
                    })
                    
                    st.session_state.products = pd.concat([
                        st.session_state.products, 
                        new_product
                    ], ignore_index=True)
                    
                    save_to_csv()
                    
                    profit = (selling_price - cost_price) * quantity
                    profit_pct = ((selling_price - cost_price) / cost_price * 100) if cost_price > 0 else 0
                    
                    if profit >= 0:
                        st.success(f"✅ Product '{name}' added successfully!")
                        st.info(f"💰 Profit: ₹{profit:,.2f} ({profit_pct:.2f}%)")
                    else:
                        st.warning(f"⚠️ Product '{name}' added but you're in LOSS!")
                        st.error(f"💸 Loss: ₹{abs(profit):,.2f} ({profit_pct:.2f}%)")
                    
                    st.balloons()
                else:
                    st.error("❌ Please fill all required fields correctly!")

    # ============== EDIT/DELETE PRODUCTS ==============
    elif menu == "✏️ Edit/Delete Products":
        st.title("✏️ Manage Products")
        
        if st.session_state.products.empty:
            st.warning("No products available. Add some products first!")
        else:
            st.markdown("### Current Inventory")
            
            # Calculate profit for display
            display_df = ensure_profit_columns(st.session_state.products.copy())
            
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### Delete Product")
            
            product_to_delete = st.selectbox(
                "Select product to delete",
                st.session_state.products['Product Name'].tolist()
            )
            
            if st.button("🗑️ Delete Product", type="primary"):
                st.session_state.products = st.session_state.products[
                    st.session_state.products['Product Name'] != product_to_delete
                ]
                save_to_csv()
                st.success(f"Product '{product_to_delete}' deleted successfully!")
                st.rerun()

    # ============== PROFIT ANALYSIS ==============
    elif menu == "💰 Profit Analysis":
        st.title("💰 Profit/Loss Analysis")
        
        if st.session_state.products.empty:
            st.warning("No data available for analysis!")
        else:
            # Calculate profit for all products
            df = ensure_profit_columns(st.session_state.products.copy())
            
            st.markdown("### 📊 Detailed Profit Analysis")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_cost = (df['Cost Price'] * df['Quantity']).sum()
                st.metric("Total Cost", f"₹{total_cost:,.0f}")
            
            with col2:
                total_sales = (df['Selling Price'] * df['Quantity']).sum()
                st.metric("Total Sales", f"₹{total_sales:,.0f}")
            
            with col3:
                total_profit = df['Profit'].sum()
                delta_color = "normal" if total_profit >= 0 else "inverse"
                st.metric("Total Profit/Loss", f"₹{total_profit:,.0f}", 
                         delta=f"{total_profit/total_cost*100:.2f}%" if total_cost > 0 else "0%")
            
            with col4:
                profitable_items = len(df[df['Profit'] > 0])
                st.metric("Profitable Items", f"{profitable_items}/{len(df)}")
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Profit by Product")
                fig_bar = px.bar(
                    df, 
                    x='Product Name', 
                    y='Profit',
                    color='Profit',
                    color_continuous_scale='RdYlGn',
                    title='Profit/Loss per Product'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                st.markdown("### 📈 Profit Percentage")
                fig_line = px.line(
                    df, 
                    x='Product Name', 
                    y='Profit %',
                    markers=True,
                    title='Profit % per Product'
                )
                fig_line.update_traces(line_color='#FF6B6B', marker_size=10)
                st.plotly_chart(fig_line, use_container_width=True)
            
            # Detailed table
            st.markdown("### 📋 Detailed Profit Table")
            st.dataframe(df, use_container_width=True)
            
            # Top profitable products
            st.markdown("### 🏆 Top Profitable Products")
            top_profit = df.nlargest(5, 'Profit')
            st.dataframe(top_profit, use_container_width=True)
            
            # Loss making products
            loss_products = df[df['Profit'] < 0]
            if not loss_products.empty:
                st.markdown("### ⚠️ Loss Making Products")
                st.dataframe(loss_products, use_container_width=True)

    # ============== REPORTS ==============
    elif menu == "📑 Reports":
        st.title(" Reports & Export")
        
        if st.session_state.products.empty:
            st.warning("No data available for reports!")
        else:
            # Calculate profit for export
            export_df = ensure_profit_columns(st.session_state.products.copy())
            
            st.markdown("### Download Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV (with Profit)",
                    data=csv,
                    file_name=f"inventory_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    type="primary"
                )
            
            with col2:
                if st.button("📊 Generate Summary Report"):
                    st.markdown("### Summary Statistics")
                    st.write(export_df.describe())
            
            st.markdown("---")
            st.markdown("### Category-wise Summary")
            if not export_df.empty:
                category_summary = export_df.groupby('Category').agg({
                    'Quantity': 'sum',
                    'Cost Price': 'mean',
                    'Selling Price': 'mean',
                    'Profit': 'sum'
                }).reset_index()
                category_summary.columns = ['Category', 'Total Quantity', 'Avg Cost Price', 'Avg Selling Price', 'Total Profit']
                st.dataframe(category_summary, use_container_width=True)
