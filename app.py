import streamlit as st
import sqlite3
import pandas as pd
import uuid
import json
import os
from database import TicketDB
from analyzer import TicketAnalyzer

# --- Configuration ---
st.set_page_config(page_title="Ticket Analyzer Dashboard", layout="wide")
st.title("Customer Support Ticket Analyzer")

# --- Initialization ---
db = TicketDB()
analyzer = TicketAnalyzer()

def initialize_database():
    """Checks database state and seeds initial data if empty."""
    db.connect()
    db.create_table()
    
    try:
        count = db.cursor.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        if count == 0 and os.path.exists("data/tickets.json"):
            with open("data/tickets.json", 'r') as f:
                tickets = json.load(f)
            
            for t in tickets:
                content = t.get("content", "")
                if "category" not in t or "priority" not in t:
                    cat, prio = analyzer.analyze_ticket(content)
                    t['category'] = cat
                    t['priority'] = prio
                db.insert_ticket(t)
            st.info(f"Initialized database with {len(tickets)} sample records.")
    except Exception as e:
        st.error(f"Database initialization error: {e}")
    finally:
        db.close()

initialize_database()

# --- Sidebar: Data Entry ---
st.sidebar.header("Submit Ticket")

with st.sidebar.form("ticket_form"):
    customer_name = st.text_input("Customer Name")
    issue_content = st.text_area("Description")
    submitted = st.form_submit_button("Submit")

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
            
            st.success(f"Ticket {new_id} created successfully.")
            st.rerun()
        else:
            st.error("All fields are required.")

# --- Main Dashboard ---
conn = sqlite3.connect("tickets.db")

# Metrics Section
try:
    total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
except sqlite3.OperationalError:
    total = 0

if total > 0:
    col1, col2 = st.columns(2)
    urgent = conn.execute("SELECT COUNT(*) FROM tickets WHERE priority='high'").fetchone()[0]
    col1.metric("Total Tickets", total)
    col2.metric("High Priority", urgent)

    st.divider()

    # Visualizations
    st.subheader("Analytics Overview")
    c1, c2 = st.columns(2)

    df_priority = pd.read_sql("SELECT priority, COUNT(*) as count FROM tickets GROUP BY priority", conn)
    if not df_priority.empty:
        c1.write("**Priority Distribution**")
        c1.bar_chart(df_priority.set_index("priority"))

    df_category = pd.read_sql("SELECT category, COUNT(*) as count FROM tickets GROUP BY category", conn)
    if not df_category.empty:
        c2.write("**Category Distribution**")
        c2.bar_chart(df_category.set_index("category"))

    st.divider()

    # Data Table
    st.subheader("Ticket Explorer")
    search_term = st.text_input("Search Tickets", placeholder="Enter keywords...")
    
    query = "SELECT id, customer, priority, category, status, content FROM tickets"
    params = []
    
    if search_term:
        query += " WHERE content LIKE ?"
        params.append(f"%{search_term}%")
        
    df_tickets = pd.read_sql(query, conn, params=params)
    st.dataframe(df_tickets, use_container_width=True, hide_index=True)

else:
    st.info("No tickets found. Submit a new ticket from the sidebar to begin.")

conn.close()
