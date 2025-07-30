import streamlit as st
import sqlite3
import pandas as pd

def show():
    # --- Initialize DB ---
    conn = sqlite3.connect("jobs.db", isolation_level=None)
    c = conn.cursor()

    # --- Create Tables if Not Exists ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_number TEXT PRIMARY KEY,
            branch_number TEXT,
            job_name TEXT,
            salesforce_id TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS wbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_number TEXT,
            service_line TEXT,
            wbs_task TEXT,
            wbs_subtask TEXT,
            qty REAL,
            unit_of_measure TEXT,
            contract_vs_co TEXT,
            fpa_type TEXT,
            fpa_subtype TEXT,
            budgeted_revenue REAL,
            budgeted_hours REAL,
            budgeted_cost REAL
        )
    ''')

    # --- Page Setup ---
    st.set_page_config(page_title="Create/Edit WBS", layout="wide")
    st.title("🧱 Creating/Editing a WBS")
    
    # --- Instructions Box ---
    with st.container():
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <strong>Instructions:</strong> Please create a WBS for your project. Distribute your total budgeted cost, 
        budgeted hours for the project throughout all WBS line items. The budgeted revenue, budgeted hours, 
        and budgeted cost should line up with your estimator's bid and the revenue should match your signed contract amount.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Notes on WBS →", type="secondary"):
                st.info("WBS Guidelines:\n\n1. Each WBS item should have clear deliverables\n2. Budget should align with contract amounts\n3. Hours should reflect realistic estimates\n4. Use consistent service lines and tasks")

    # --- Job Selection ---
    st.subheader("📁 Select Job")
    
    # Get all jobs for dropdown
    jobs = c.execute("SELECT job_number, job_name FROM jobs ORDER BY job_number").fetchall()
    
    if not jobs:
        st.warning("⚠️ No jobs found. Please add jobs in the Job Info tab first.")
        return
    
    # Create job selection dropdown
    job_options = [f"{job[0]} - {job[1]}" for job in jobs]
    selected_job_display = st.selectbox("Select a job to edit WBS:", job_options, index=0)
    
    # Extract job number from selected option
    selected_job_number = selected_job_display.split(" - ")[0]
    
    # Display selected job info
    job_info = c.execute("SELECT * FROM jobs WHERE job_number = ?", (selected_job_number,)).fetchone()
    if job_info:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Job Number", job_info[0])
        with col2:
            st.metric("Branch Number", job_info[1])
        with col3:
            st.metric("Job Name", job_info[2])
        with col4:
            st.metric("Salesforce ID", job_info[3] if job_info[3] else "N/A")

    # --- WBS Data Management ---
    st.subheader("📋 WBS Line Items")
    
    # Get existing WBS data for the selected job
    try:
        wbs_data = c.execute("""
            SELECT service_line, wbs_task, wbs_subtask, qty, unit_of_measure, 
                   contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost
            FROM wbs 
            WHERE job_number = ?
            ORDER BY rowid
        """, (selected_job_number,)).fetchall()
    except sqlite3.OperationalError as e:
        if "no such table" in str(e).lower():
            st.info("📝 No WBS table found. Starting with empty table.")
            wbs_data = []
        elif "no such column" in str(e).lower():
            st.warning("⚠️ Database schema mismatch. Please delete jobs.db and restart the app.")
            st.info("This will recreate the database with the correct schema.")
            return
        else:
            st.error(f"Database error: {str(e)}")
            wbs_data = []
    
    columns = [
        "Service Line", "WBS Task", "WBS Subtask", "QTY", "Unit of Measure",
        "Contract vs CO", "FPA Type", "FPA Subtype", "Budgeted Revenue", "Budgeted Hours", "Budgeted Cost"
    ]
    
    # Prepare DataFrame for editing
    if wbs_data:
        df = pd.DataFrame(wbs_data, columns=columns)
    else:
        df = pd.DataFrame(columns=columns)
    
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Contract vs CO": st.column_config.SelectboxColumnConfig(options=["Contract", "CO"]),
            "FPA Type": st.column_config.SelectboxColumnConfig(options=["Services", "Materials", "Equipment"]),
            "FPA Subtype": st.column_config.SelectboxColumnConfig(options=["Labor", "Management", "Other"]),
        },
        key="wbs_editor"
    )
    
    # Display totals
    if not edited_df.empty:
        total_revenue = edited_df["Budgeted Revenue"].fillna(0).sum()
        total_hours = edited_df["Budgeted Hours"].fillna(0).sum()
        total_cost = edited_df["Budgeted Cost"].fillna(0).sum()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budgeted Revenue", f"${total_revenue:,.2f}")
        with col2:
            st.metric("Total Budgeted Hours", f"{total_hours:,.0f}")
        with col3:
            st.metric("Total Budgeted Cost", f"${total_cost:,.2f}")
    
    # Save button
    if st.button("💾 Save & Complete", type="primary"):
        try:
            # Remove all existing WBS for this job
            c.execute("DELETE FROM wbs WHERE job_number = ?", (selected_job_number,))
            # Insert new/edited WBS items
            for _, row in edited_df.iterrows():
                # Skip empty rows
                if not row[["Service Line", "WBS Task", "WBS Subtask"]].isnull().all():
                    c.execute('''
                        INSERT INTO wbs (
                            job_number, service_line, wbs_task, wbs_subtask, qty,
                            unit_of_measure, contract_vs_co, fpa_type, fpa_subtype,
                            budgeted_revenue, budgeted_hours, budgeted_cost
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        selected_job_number,
                        row["Service Line"], row["WBS Task"], row["WBS Subtask"],
                        row["QTY"] if pd.notnull(row["QTY"]) else 0,
                        row["Unit of Measure"], row["Contract vs CO"], row["FPA Type"], row["FPA Subtype"],
                        row["Budgeted Revenue"] if pd.notnull(row["Budgeted Revenue"]) else 0,
                        row["Budgeted Hours"] if pd.notnull(row["Budgeted Hours"]) else 0,
                        row["Budgeted Cost"] if pd.notnull(row["Budgeted Cost"]) else 0
                    ))
            st.success("✅ WBS saved successfully!")
            st.experimental_rerun()
        except sqlite3.OperationalError as e:
            st.error(f"❌ Error saving WBS: {str(e)}")
            st.info("Please check that the database schema is correct.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
    
    conn.close()
