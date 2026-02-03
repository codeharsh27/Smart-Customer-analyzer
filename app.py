import streamlit as st
import sqlite3
import pandas as pd
import uuid
import json
import os
from database import TicketDB
from analyzer import TicketAnalyzer

# --- SETUP & CONFIG ---
st.set_page_config(page_title="Ticket Analyzer", layout="wide")
st.title("🤖 Smart Customer Support Analyzer")

# Initialize Logic
db = TicketDB()
analyzer = TicketAnalyzer()

# --- AUTO-LOAD DATA LOGIC ---
# We check if the DB is empty on launch. If so, we load the JSON.
def init_db():
    db.connect()
    db.create_table()
    
    # Check count
    try:
        count = db.cursor.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        if count == 0:
            # DB is empty! Load JSON.
            if os.path.exists("data/tickets.json"):
                with open("data/tickets.json", 'r') as f:
                    tickets = json.load(f)
                
                for t in tickets:
                    # Provide default content if missing
                    content = t.get("content", "")
                    
                    # Analyze if not already analyzed
                    if "category" not in t or "priority" not in t:
                        cat, prio = analyzer.analyze_ticket(content)
                        t['category'] = cat
                        t['priority'] = prio
                    
                    db.insert_ticket(t)
                st.toast(f"🎉 loaded {len(tickets)} demo tickets from JSON!")
    except Exception as e:
        st.error(f"Error initializing DB: {e}")
    finally:
        db.close()

# Run initialization once
init_db()


# --- SIDEBAR: INPUT & ACTIONS ---
st.sidebar.header("📝 Submit New Ticket")

with st.sidebar.form("ticket_form"):
    customer_name = st.text_input("Customer Name", placeholder="e.g. John Doe")
    issue_content = st.text_area("Issue Description", placeholder="e.g. I can't login...")
    submitted = st.form_submit_button("🚀 Submit Ticket")

    if submitted:
        if customer_name and issue_content:
            cat, prio = analyzer.analyze_ticket(issue_content)
            
            db.connect()
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
            
            st.success(f"Ticket Created! ID: {new_id}")
            # Rerun so the charts update immediately
            st.rerun()
        else:
            st.error("Please fill in both fields.")

# --- MAIN PAGE: DASHBOARD ---
conn = sqlite3.connect("tickets.db")

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

    st.subheader("📊 Analytics Overview")
    c1, c2 = st.columns(2)

    df_priority = pd.read_sql("SELECT priority, COUNT(*) as count FROM tickets GROUP BY priority", conn)
    if not df_priority.empty:
        c1.bar_chart(df_priority.set_index("priority"))

    df_category = pd.read_sql("SELECT category, COUNT(*) as count FROM tickets GROUP BY category", conn)
    if not df_category.empty:
        c2.bar_chart(df_category.set_index("category"))

    st.subheader("🔎 Ticket Explorer")
    search_term = st.text_input("Search for keywords")
    
    query = "SELECT * FROM tickets"
    params = []
    
    if search_term:
        query += " WHERE content LIKE ?"
        params.append(f"%{search_term}%")
        
    df_tickets = pd.read_sql(query, conn, params=params)
    st.dataframe(df_tickets, use_container_width=True, hide_index=True)

conn.close()
