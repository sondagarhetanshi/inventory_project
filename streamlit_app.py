import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Login Function
def check_login(username, password):
    if username == "admin" and password == "1234":
        return True
    return False

# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login Page
if not st.session_state.logged_in:
    st.title("🔐 Login Page")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.error("❌ Wrong Username/Password!")
    st.stop()

# Logout Button
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# Main App (Login ke baad)
st.title("📦 Inventory Analytics System")
st.sidebar.success("Welcome Admin! ✅")

# Charts ka code...
data = {'Product': ['Mouse', 'Keyboard', 'Chair', 'Laptop', 'Table'],
        'Quantity': [45, 5, 3, 2, 2]}
df = pd.DataFrame(data)

st.subheader("📈 Top Products")
fig1, ax1 = plt.subplots()
ax1.bar(df['Product'], df['Quantity'])
st.pyplot(fig1)

st.subheader("🥧 Product Distribution")
fig2, ax2 = plt.subplots()
ax2.pie(df['Quantity'], labels=df['Product'], autopct='%1.1f%%')
st.pyplot(fig2)

st.subheader("📉 Monthly Revenue")
rev_data = {'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
            'Revenue': [105000, 15000, 19000, 7500]}
df2 = pd.DataFrame(rev_data)
fig3, ax3 = plt.subplots()
ax3.plot(df2['Month'], df2['Revenue'], marker='o')
st.pyplot(fig3)

st.success("💰 Total Revenue: 146,500")