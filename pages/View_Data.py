import streamlit as st
import sqlite3
import pandas as pd

def show():
    # --- Initialize Database ---
    import os
    db_path = os.path.join(os.getcwd(), "job_master.db")
    conn = sqlite3.connect(db_path, isolation_level=None)
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
    st.set_page_config(page_title="View Data", layout="wide")
    st.title("📊 View Jobs & WBS Data")
    st.markdown("---")

    # --- Get all jobs for dropdown ---
    jobs = c.execute("SELECT job_number, job_name FROM jobs ORDER BY job_number").fetchall()
    
    if not jobs:
        st.warning("⚠️ No jobs found. Please add jobs in the Job Info tab first.")
        return

    # --- Create job selection dropdown ---
    job_options = [f"{job[0]} - {job[1]}" for job in jobs]
    selected_job_display = st.selectbox("Select a job to view:", job_options, index=0)
    
    # Extract job number from selected option
    selected_job_number = selected_job_display.split(" - ")[0]

    # --- Display Job Information ---
    st.subheader("📁 Job Information")
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

    # --- Display WBS Data for Selected Job ---
    st.subheader("🧱 WBS Data")
    
    # Check if wbs table exists
    try:
        # Get WBS data for the selected job
        wbs_data = c.execute("""
            SELECT service_line, wbs_task, wbs_subtask, qty, unit_of_measure, 
                   contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, 
                   budgeted_hours, budgeted_cost
            FROM wbs 
            WHERE job_number = ?
            ORDER BY service_line, wbs_task, wbs_subtask
        """, (selected_job_number,)).fetchall()
    except sqlite3.OperationalError as e:
        if "no such table" in str(e).lower():
            st.info("📝 No WBS table found. Please add WBS data in the Create WBS tab first.")
            wbs_data = []
        else:
            st.error(f"Database error: {str(e)}")
            wbs_data = []
    
    if wbs_data:
        # Create DataFrame for better display
        df_wbs = pd.DataFrame(wbs_data, columns=[
            "Service Line", "WBS Task", "WBS Subtask", "QTY", "Unit of Measure",
            "Contract vs CO", "FPA Type", "FPA Subtype", "Budgeted Revenue", 
            "Budgeted Hours", "Budgeted Cost"
        ])
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total WBS Items", len(wbs_data))
        with col2:
            unique_service_lines = df_wbs["Service Line"].nunique()
            st.metric("Service Lines", unique_service_lines)
        with col3:
            unique_tasks = df_wbs["WBS Task"].nunique()
            st.metric("WBS Tasks", unique_tasks)
        
        # Display the WBS data
        st.dataframe(df_wbs, use_container_width=True)
        
        # --- Filtering Options ---
        st.subheader("🔍 Filter WBS Data")
        
        # Service Line Filter
        service_lines = ["All"] + sorted(df_wbs["Service Line"].unique().tolist())
        selected_service_line = st.selectbox("Filter by Service Line:", service_lines)
        
        # WBS Task Filter
        if selected_service_line != "All":
            filtered_df = df_wbs[df_wbs["Service Line"] == selected_service_line]
            wbs_tasks = ["All"] + sorted(filtered_df["WBS Task"].unique().tolist())
        else:
            wbs_tasks = ["All"] + sorted(df_wbs["WBS Task"].unique().tolist())
        
        selected_wbs_task = st.selectbox("Filter by WBS Task:", wbs_tasks)
        
        # Apply filters
        filtered_data = df_wbs.copy()
        if selected_service_line != "All":
            filtered_data = filtered_data[filtered_data["Service Line"] == selected_service_line]
        if selected_wbs_task != "All":
            filtered_data = filtered_data[filtered_data["WBS Task"] == selected_wbs_task]
        
        if not filtered_data.empty:
            st.subheader("📋 Filtered Results")
            st.dataframe(filtered_data, use_container_width=True)
            
            # Export functionality
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"wbs_data_{selected_job_number}_{selected_service_line}_{selected_wbs_task}.csv",
                mime="text/csv"
            )
        else:
            st.info("No data matches the selected filters.")
            
    else:
        st.info(f"📝 No WBS data found for job {selected_job_number}. Add WBS data in the Create WBS tab.")

    # --- Summary Statistics ---
    st.subheader("📈 Summary Statistics")
    
    # Get all WBS data for summary
    try:
        all_wbs = c.execute("SELECT * FROM wbs").fetchall()
    except sqlite3.OperationalError as e:
        if "no such table" in str(e).lower():
            st.info("📝 No WBS table found. Please add WBS data in the Create WBS tab first.")
            all_wbs = []
        else:
            st.error(f"Database error: {str(e)}")
            all_wbs = []
    if all_wbs:
        df_all_wbs = pd.DataFrame(all_wbs, columns=[
            "ID", "Job Number", "Service Line", "WBS Task", "WBS Subtask", "QTY",
            "Unit of Measure", "Contract vs CO", "FPA Type", "FPA Subtype",
            "Budgeted Revenue", "Budgeted Hours", "Budgeted Cost"
        ])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Jobs with WBS", df_all_wbs["Job Number"].nunique())
        with col2:
            st.metric("Total WBS Items", len(df_all_wbs))
        with col3:
            st.metric("Unique Service Lines", df_all_wbs["Service Line"].nunique())
        with col4:
            st.metric("Unique WBS Tasks", df_all_wbs["WBS Task"].nunique())
        
        # Top service lines
        st.subheader("🏆 Top Service Lines")
        service_line_counts = df_all_wbs["Service Line"].value_counts().head(5)
        st.bar_chart(service_line_counts)
        
        # Top WBS tasks
        st.subheader("📋 Top WBS Tasks")
        wbs_task_counts = df_all_wbs["WBS Task"].value_counts().head(5)
        st.bar_chart(wbs_task_counts)
    else:
        st.info("No WBS data available for summary statistics.")

    conn.close()
