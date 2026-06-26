import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ==================== LOGIN FUNCTION ====================
def check_login(username, password):
    if username == "admin" and password == "1234":
        return True
    return False

# ==================== DATA FILE ====================
DATA_FILE = "inventory_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['Product', 'Quantity', 'Price'])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ==================== LOGIN PAGE ====================
if not st.session_state.logged_in:
    st.title("🔐 Login Required")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        if submit:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.error("❌ Wrong Username or Password!")
    st.stop()

# ==================== LOGOUT BUTTON ====================
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ==================== MAIN APP ====================
st.title("📦 Inventory Analytics System")
menu = st.sidebar.selectbox("Menu", ["📊 Dashboard", "➕ Add Product", "📋 View Data"])

df = load_data()

# ==================== DASHBOARD ====================
if menu == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    if not df.empty:
        # Search in Dashboard
        col1, col2 = st.columns([3, 1])
        with col1:
            search_dash = st.text_input("🔍 Search Product", placeholder="Type to search...")
        
        # Filter data
        if search_dash:
            df_display = df[df['Product'].str.contains(search_dash, case=False, na=False)]
        else:
            df_display = df
        
        if not df_display.empty:
            # METRICS - 4 Columns
            st.subheader("📌 Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            total_products = len(df_display)
            total_items = df_display['Quantity'].sum()
            total_value = (df_display['Quantity'] * df_display['Price']).sum()
            avg_price = df_display['Price'].mean()
            
            col1.metric("Total Products", total_products)
            col2.metric("Total Items", total_items)
            col3.metric("Total Value", f"₹{total_value:,.0f}")
            col4.metric("Avg Price", f"₹{avg_price:.2f}")
            
            st.markdown("---")
            
            # CHARTS - 2 Columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Bar Chart - Top Products")
                fig1, ax1 = plt.subplots()
                ax1.bar(df_display['Product'], df_display['Quantity'], color='skyblue')
                plt.xticks(rotation=45, ha='right')
                st.pyplot(fig1)
            
            with col2:
                st.subheader("🥧 Pie Chart - Distribution")
                fig2, ax2 = plt.subplots()
                ax2.pie(df_display['Quantity'], labels=df_display['Product'], autopct='%1.1f%%')
                st.pyplot(fig2)
            
            # LINE CHART - Full Width
            st.subheader("📉 Line Chart - Price Analysis")
            fig3, ax3 = plt.subplots()
            ax3.plot(df_display['Product'], df_display['Price'], marker='o', color='green', linewidth=2)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True)
            st.pyplot(fig3)
        else:
            st.error("❌ No products found!")
    else:
        st.info("📭 No data! Add products first.")

# ==================== ADD PRODUCT ====================
elif menu == "➕ Add Product":
    st.header("➕ Add New Product")
    with st.form("add_form"):
        name = st.text_input("Product Name")
        qty = st.number_input("Quantity", min_value=0)
        price = st.number_input("Price", min_value=0.0)
        submit = st.form_submit_button("💾 Save Product")
        
        if submit:
            if name:
                new_data = {'Product': name, 'Quantity': qty, 'Price': price}
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                save_data(df)
                st.success("✅ Added!")
                st.rerun()
            else:
                st.error("Enter product name!")

# ==================== VIEW DATA ====================
elif menu == "📋 View Data":
    st.header("📋 All Products")
    
    # Search Box
    st.subheader("🔍 Search Product")
    search_query = st.text_input("Search by product name", placeholder="Type product name (e.g., mouse, key...)")
    
    # Filter data
    if search_query:
        filtered_df = df[df['Product'].str.contains(search_query, case=False, na=False)]
        st.write(f"Found {len(filtered_df)} product(s)")
    else:
        filtered_df = df
    
    # Display data
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
        
        # Delete Section
        st.markdown("---")
        st.subheader("🗑️ Delete Product")
        
        delete_name = st.selectbox("Select product to delete", filtered_df['Product'].tolist())
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Delete", use_container_width=True):
                df = df[df['Product'] != delete_name]
                save_data(df)
                st.success(f"✅ Deleted {delete_name}")
                st.rerun()
        
        with col2:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="inventory_data.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        if search_query:
            st.error(f"❌ No products found matching '{search_query}'")
        else:
            st.info("📭 No data available!")