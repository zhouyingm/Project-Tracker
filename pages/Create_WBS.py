import streamlit as st
import sqlite3

def show():
    # --- Initialize DB ---
    conn = sqlite3.connect("jobs.db", isolation_level=None)
    c = conn.cursor()

    # --- Create Table if Not Exists ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS wbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_number TEXT,
            service_line TEXT,
            wbs_task TEXT,
            wbs_subtask TEXT,
            unit_of_measure TEXT,
            contract_vs_co TEXT,
            fpa_type TEXT,
            fpa_subtype TEXT
        )
    ''')

    # --- Page Setup ---
    st.set_page_config(page_title="Step 2: Create WBS", layout="wide")
    st.title("🧱 Step 2: Create Work Breakdown Structure (WBS)")

    with st.form("wbs_form"):
        job_number = st.text_input("Job Number (to link with Step 1)")

        service_line = st.text_input("Service Line")
        wbs_task = st.text_input("WBS Task")
        wbs_subtask = st.text_input("WBS Subtask")
        unit_of_measure = st.text_input("Unit of Measure")
        contract_vs_co = st.text_input("Contract vs CO")
        fpa_type = st.text_input("FPA Type")
        fpa_subtype = st.text_input("FPA Subtype")

        submitted = st.form_submit_button("Save WBS")

        if submitted:
            if job_number and service_line and wbs_task:
                c.execute('''
                    INSERT INTO wbs (
                        job_number, service_line, wbs_task, wbs_subtask,
                        unit_of_measure, contract_vs_co, fpa_type, fpa_subtype
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job_number, service_line, wbs_task, wbs_subtask,
                    unit_of_measure, contract_vs_co, fpa_type, fpa_subtype
                ))
                st.success("✅ WBS saved successfully.")
            else:
                st.error("Please complete all required fields.")

    # --- Optional: View Saved WBS ---
    if st.checkbox("Show saved WBS records"):
        rows = c.execute("SELECT * FROM wbs").fetchall()
        if rows:
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("No WBS records saved yet.")
