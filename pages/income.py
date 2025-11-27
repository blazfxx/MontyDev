import streamlit as st
import pandas as pd
from datetime import datetime
from database import init_finance_db, set_user_income, get_user_income, add_expense, get_user_expenses, delete_expense
import plotly.express as px

init_finance_db()

st.set_page_config(page_title="Financial Health", page_icon="💸", layout="wide")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("🔒 You must be logged in to view this page.")
    st.stop()

if not st.session_state.get('is_adult', False):
    st.info("This tool is designed for Adults/Professionals.")
    st.stop()

username = st.session_state['username']

st.title(f"💸 Financial Overview: {username}")
st.caption("Professional tracking of Income vs. Expenditure.")


with st.sidebar:
    st.header("⚙️ Configuration")
    current_income = get_user_income(username)
    
    new_income = st.number_input("Monthly Net Income ($)", min_value=0.0, value=float(current_income), step=100.0)
    
    if st.button("Update Income"):
        set_user_income(username, new_income)
        st.success("Income updated.")
        st.rerun()
with st.sidebar:
    st.header("All-in-one Kit")
    st.session_state.setdefault('logged_in', False)
    st.session_state.setdefault('username', None)
    st.session_state.setdefault('is_student', False)
    st.session_state.setdefault('is_adult', False)
    if st.session_state.get('logged_in'):
        st.success(f"Signed in as {st.session_state.get('username')}")
        if st.button("Sign Out", key="signout_utils"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.rerun()
    else:
        st.write("Created by **Muhammad Khan**")

expenses_raw = get_user_expenses(username)
if expenses_raw:
    df = pd.DataFrame(expenses_raw, columns=['ID', 'Category', 'Item', 'Amount', 'Date'])
    total_spent = df['Amount'].sum()
else:
    df = pd.DataFrame(columns=['ID', 'Category', 'Item', 'Amount', 'Date'])
    total_spent = 0.0

remaining = new_income - total_spent
burn_rate = (total_spent / new_income * 100) if new_income > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Monthly Income (change on sidebar :D)", f"${new_income:,.2f}")

if burn_rate > 50:
    col2.metric("Total Expenses", f"${total_spent:,.2f}", delta=f"-{burn_rate:.1f}% Used")
else:
    col2.metric("Total Expenses", f"${total_spent:,.2f}", delta=f"-{burn_rate:.1f}% Used", delta_color="inverse")
col3.metric("Remaining Budget", f"${remaining:,.2f}", delta_color="normal")

st.divider()


col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Log Transaction")
    with st.form("add_expense_form", clear_on_submit=True):
        item = st.text_input("Description", placeholder="e.g. Rent, Groceries")
        category = st.selectbox("Category", ["Housing", "Food", "Transportation", "Utilities", "Insurance", "Healthcare", "Savings/Investing", "Entertainment", "Debt Payments"])
        amount = st.number_input("Amount ($)", min_value=0.01, step=1.00)
        date_picker = st.date_input("Date", datetime.today())
        
        if st.form_submit_button("Add Record"):
            add_expense(username, category, item, amount, str(date_picker))
            st.success("Saved.")
            st.rerun()

    st.subheader("AI Analyst Verdict")
    if new_income > 0:
        if burn_rate > 100:
            st.error("🚨 CRITICAL: You are spending more than you earn. You are in debt.")
        elif burn_rate > 85:
            st.warning("⚠️ WARNING: You are living paycheck to paycheck. Reduce discretionary spending immediately.")
        elif burn_rate < 50:
            st.success("✅ EXCELLENT: You are saving over 50% of your income. Consider investing the surplus.")
        else:
            st.info("ℹ️ STATUS: Your spending is within normal limits, but keep an eye on the Food category.")
    else:
        st.write("Set your income in the sidebar to get analysis.")

with col_right:
    st.subheader("Spending Analysis")
    
    if not df.empty:
        category_data = df.groupby("Category", as_index=False)["Amount"].sum()

        view_tab1, view_tab2 = st.tabs(["Pie Chart", "Bar Chart"])

        with view_tab1:
            fig = px.pie(
                category_data, 
                values='Amount', 
                names='Category',
                title='Where is your money going?',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        with view_tab2:
            st.bar_chart(category_data.set_index("Category"))

    else:
        st.info("No transactions logged yet.")