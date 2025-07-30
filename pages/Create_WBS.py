import streamlit as st
import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("project_tracker.db")
c = conn.cursor()

# Create WBS table if not exists
c.execute("""
    CREATE TABLE IF NOT EXISTS wbs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_number TEXT,
        wbs_no INTEGER,
        service_line TEXT,
        wbs_task TEXT,
        wbs_subtask TEXT,
        quantity INTEGER,
        unit_of_measure TEXT,
        contract_vs_co TEXT,
        fpa_type TEXT,
        fpa_subtype TEXT,
        budgeted_revenue REAL,
        budgeted_hours INTEGER,
        budgeted_cost REAL
    )
""")
conn.commit()

st.set_page_config(page_title="Create WBS")
st.title("🧱 Create Work Breakdown Structure (WBS)")

# Get job number from user
job_number = st.text_input("Enter Job Number")

st.markdown("---")
st.subheader("Enter WBS Items")

# Number of entries
num_rows = st.number_input("How many WBS line items?", min_value=1, max_value=20, value=3)
wbs_rows = []

for i in range(int(num_rows)):
    st.markdown(f"**WBS Line {i+1}**")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    with col1:
        wbs_no = st.number_input(f"WBS No. {i+1}", key=f"wbs_no_{i}", min_value=1)
        service_line = st.text_input(f"Service Line {i+1}", key=f"sl_{i}")
        wbs_task = st.text_input(f"WBS Task {i+1}", key=f"task_{i}")
        wbs_subtask = st.text_input(f"WBS Subtask {i+1}", key=f"subtask_{i}")

    with col2:
        quantity = st.number_input(f"Quantity {i+1}", key=f"qty_{i}", min_value=0)
        unit_of_measure = st.text_input(f"Unit of Measure {i+1}", key=f"uom_{i}")
        contract_vs_co = st.text_input(f"Contract vs CO {i+1}", key=f"cvsco_{i}")

    with col3:
        fpa_type = st.text_input(f"FPA Type {i+1}", key=f"fpatype_{i}")
        fpa_subtype = st.text_input(f"FPA Subtype {i+1}", key=f"fpasubtype_{i}")

    with col4:
        budgeted_revenue = st.number_input(f"Budgeted Revenue {i+1}", key=f"rev_{i}", min_value=0.0, format="%.2f")
        budgeted_hours = st.number_input(f"Budgeted Hours {i+1}", key=f"hrs_{i}", min_value=0)
        budgeted_cost = st.number_input(f"Budgeted Cost {i+1}", key=f"cost_{i}", min_value=0.0, format="%.2f")

    wbs_rows.append((job_number, wbs_no, service_line, wbs_task, wbs_subtask, quantity,
                     unit_of_measure, contract_vs_co, fpa_type, fpa_subtype,
                     budgeted_revenue, budgeted_hours, budgeted_cost))

# Save to database
if st.button("💾 Save WBS to Database"):
    c.executemany("""
        INSERT INTO wbs (
            job_number, wbs_no, service_line, wbs_task, wbs_subtask,
            quantity, unit_of_measure, contract_vs_co,
            fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, wbs_rows)
    conn.commit()
    st.success("WBS items saved successfully!")

# Option to view current saved WBS
if st.checkbox("📋 Show Saved WBS Entries"):
    df = pd.read_sql("SELECT * FROM wbs WHERE job_number = ?", conn, params=(job_number,))
    st.dataframe(df)

