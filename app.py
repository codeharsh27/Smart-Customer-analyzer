import streamlit as st
import sqlite3
import pandas as pd
import uuid # For generating unique IDs
from database import TicketDB
from analyzer import TicketAnalyzer

# --- SETUP & CONFIG ---
st.set_page_config(page_title="Ticket Analyzer", layout="wide")
st.title("🤖 Smart Customer Support Analyzer")

# Initialize Logic Classes
db = TicketDB()
analyzer = TicketAnalyzer()

# --- SIDEBAR: INPUT & ACTIONS ---
st.sidebar.header("📝 Submit New Ticket")

# 1. The Input Form
with st.sidebar.form("ticket_form"):
    customer_name = st.text_input("Customer Name", placeholder="e.g. John Doe")
    issue_content = st.text_area("Issue Description", placeholder="e.g. I can't login to the portal...")
    submitted = st.form_submit_button("🚀 Submit Ticket")

    if submitted:
        if customer_name and issue_content:
            # A. Analyze it live
            cat, prio = analyzer.analyze_ticket(issue_content)
            
            # B. Save to DB
            db.connect()
            db.create_table()
            new_id = f"TICKET-{str(uuid.uuid4())[:8].upper()}"
            
            record = {
                "id": new_id,
                "customer": customer_name,
                "content": issue_content,
                "status": "new",
                "category": cat,
                "priority": prio
            }
            db.insert_ticket(record)
            db.close()
            
            # C. Show Success Message
            st.success(f"Ticket Created! ID: {new_id}")
            st.info(f"Analysis Result: [{cat.upper()}] with {prio.upper()} Priority")
        else:
            st.error("Please fill in both fields.")

st.sidebar.markdown("---")

# 2. Reload Button (Still useful for bulk updates)
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# --- MAIN PAGE: DASHBOARD ---

# We reuse the logic to display data
conn = sqlite3.connect("tickets.db")

# 1. High Level Metrics
# We handle the case where DB might be empty first
try:
    total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
except:
    total = 0

if total == 0:
    st.warning("No data found! Use the sidebar to add a ticket.")
else:
    col1, col2, col3 = st.columns(3)
    urgent = conn.execute("SELECT COUNT(*) FROM tickets WHERE priority='high'").fetchone()[0]
    col1.metric("Total Tickets", total)
    col2.metric("Urgent Issues", urgent, delta_color="inverse")

    # 2. Charts
    st.subheader("📊 Analytics Overview")
    c1, c2 = st.columns(2)

    df_priority = pd.read_sql("SELECT priority, COUNT(*) as count FROM tickets GROUP BY priority", conn)
    # Basic check to avoid error if empty
    if not df_priority.empty:
        c1.bar_chart(df_priority.set_index("priority"))

    df_category = pd.read_sql("SELECT category, COUNT(*) as count FROM tickets GROUP BY category", conn)
    if not df_category.empty:
        c2.bar_chart(df_category.set_index("category"))

    # 3. Interactive Data Explorer
    st.subheader("🔎 Ticket Explorer")
    
    # Simple search filter
    search_term = st.text_input("Search for keywords (e.g. 'billing')")
    
    query = "SELECT * FROM tickets"
    params = []
    
    if search_term:
        query += " WHERE content LIKE ?"
        params.append(f"%{search_term}%")
        
    df_tickets = pd.read_sql(query, conn, params=params)
    st.dataframe(df_tickets, use_container_width=True, hide_index=True)

conn.close()
