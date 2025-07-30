import streamlit as st
import sqlite3
import pandas as pd  # ✅ Put this at the top

def show():
    # --- Initialize Database ---
    import os
    db_path = os.path.join(os.getcwd(), "job_master.db")
    conn = sqlite3.connect(db_path, isolation_level=None)
    c = conn.cursor()

    # --- Create Table if Not Exists ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_number TEXT PRIMARY KEY,
            branch_number TEXT,
            job_name TEXT,
            salesforce_id TEXT
        )
    ''')

    # --- Streamlit Page Setup ---
    st.set_page_config(page_title="Step 1: Job Info", layout="centered")
    st.title("📁 Step 1: Enter Job Information")

    # --- Input Fields ---
    with st.form("job_form"):
        job_number = st.text_input("Job Number")
        branch_number = st.text_input("Branch Number")
        job_name = st.text_input("Job Name")
        salesforce_id = st.text_input("Salesforce ID (optional)")

        submitted = st.form_submit_button("Save Job Info")

        if submitted:
            if job_number and branch_number and job_name:
                try:
                    c.execute("INSERT INTO jobs VALUES (?, ?, ?, ?)",
                              (job_number, branch_number, job_name, salesforce_id))
                    st.success("✅ Job saved successfully.")
                except sqlite3.IntegrityError:
                    st.warning("⚠️ Job already exists.")
            else:
                st.error("Please fill in all required fields.")

    # --- Optional: View current saved jobs ---
    if st.checkbox("Show saved jobs"):  # ✅ this should be inside the `show()` function
        jobs = c.execute("SELECT * FROM jobs").fetchall()
        if jobs:
            df = pd.DataFrame(jobs, columns=["Job Number", "Branch Number", "Job Name", "Salesforce ID"])
            st.dataframe(df.style.hide(axis="index"), use_container_width=True)
        else:
            st.info("No jobs saved yet.")
