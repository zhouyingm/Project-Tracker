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
    wbs_data = c.execute("""
        SELECT id, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, 
               contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost
        FROM wbs 
        WHERE job_number = ?
        ORDER BY id
    """, (selected_job_number,)).fetchall()
    
    # Initialize session state for WBS data
    if 'wbs_items' not in st.session_state:
        st.session_state.wbs_items = []
    
    # Convert existing data to session state format
    if not st.session_state.wbs_items and wbs_data:
        st.session_state.wbs_items = [
            {
                'id': row[0],
                'service_line': row[1],
                'wbs_task': row[2],
                'wbs_subtask': row[3],
                'qty': row[4] if row[4] else 0,
                'unit_of_measure': row[5],
                'contract_vs_co': row[6],
                'fpa_type': row[7],
                'fpa_subtype': row[8],
                'budgeted_revenue': row[9] if row[9] else 0,
                'budgeted_hours': row[10] if row[10] else 0,
                'budgeted_cost': row[11] if row[11] else 0
            }
            for row in wbs_data
        ]
    
    # Add new WBS item
    if st.button("➕ Add a WBS Line Item", type="primary"):
        st.session_state.wbs_items.append({
            'id': None,
            'service_line': '',
            'wbs_task': '',
            'wbs_subtask': '',
            'qty': 0,
            'unit_of_measure': '',
            'contract_vs_co': '',
            'fpa_type': '',
            'fpa_subtype': '',
            'budgeted_revenue': 0,
            'budgeted_hours': 0,
            'budgeted_cost': 0
        })
        st.rerun()
    
    # Display WBS items in a table format
    if st.session_state.wbs_items:
        # Create DataFrame for display
        df = pd.DataFrame(st.session_state.wbs_items)
        
        # Calculate totals
        total_revenue = df['budgeted_revenue'].sum()
        total_hours = df['budgeted_hours'].sum()
        total_cost = df['budgeted_cost'].sum()
        
        # Display the WBS table
        st.dataframe(
            df[['service_line', 'wbs_task', 'wbs_subtask', 'qty', 'unit_of_measure', 
                'contract_vs_co', 'fpa_type', 'fpa_subtype', 'budgeted_revenue', 
                'budgeted_hours', 'budgeted_cost']].fillna(''),
            use_container_width=True,
            hide_index=True
        )
        
        # Display totals
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budgeted Revenue", f"${total_revenue:,.2f}")
        with col2:
            st.metric("Total Budgeted Hours", f"{total_hours:,.0f}")
        with col3:
            st.metric("Total Budgeted Cost", f"${total_cost:,.2f}")
        
        # Edit WBS items
        st.subheader("✏️ Edit WBS Items")
        
        for i, item in enumerate(st.session_state.wbs_items):
            with st.expander(f"Edit WBS Item {i+1}: {item['service_line']} - {item['wbs_task']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    item['service_line'] = st.text_input("Service Line", item['service_line'], key=f"sl_{i}")
                    item['wbs_task'] = st.text_input("WBS Task", item['wbs_task'], key=f"wt_{i}")
                    item['wbs_subtask'] = st.text_input("WBS Subtask", item['wbs_subtask'], key=f"ws_{i}")
                    item['qty'] = st.number_input("Quantity", min_value=0.0, value=float(item['qty']), key=f"qty_{i}")
                    item['unit_of_measure'] = st.text_input("Unit of Measure", item['unit_of_measure'], key=f"um_{i}")
                
                with col2:
                    item['contract_vs_co'] = st.selectbox(
                        "Contract vs CO", 
                        ["Contract", "CO"], 
                        index=0 if item['contract_vs_co'] == "Contract" else 1,
                        key=f"cvc_{i}"
                    )
                    item['fpa_type'] = st.selectbox(
                        "FPA Type", 
                        ["Services", "Materials", "Equipment"], 
                        index=0 if item['fpa_type'] == "Services" else (1 if item['fpa_type'] == "Materials" else 2),
                        key=f"fpat_{i}"
                    )
                    item['fpa_subtype'] = st.selectbox(
                        "FPA Subtype", 
                        ["Labor", "Management", "Other"], 
                        index=0 if item['fpa_subtype'] == "Labor" else (1 if item['fpa_subtype'] == "Management" else 2),
                        key=f"fpas_{i}"
                    )
                    item['budgeted_revenue'] = st.number_input("Budgeted Revenue ($)", min_value=0.0, value=float(item['budgeted_revenue']), key=f"rev_{i}")
                    item['budgeted_hours'] = st.number_input("Budgeted Hours", min_value=0.0, value=float(item['budgeted_hours']), key=f"hrs_{i}")
                    item['budgeted_cost'] = st.number_input("Budgeted Cost ($)", min_value=0.0, value=float(item['budgeted_cost']), key=f"cost_{i}")
                
                # Delete button
                if st.button(f"🗑️ Delete Item {i+1}", key=f"del_{i}"):
                    st.session_state.wbs_items.pop(i)
                    st.rerun()
        
        # Save button
        if st.button("💾 Save & Complete", type="primary"):
            # Clear existing WBS data for this job
            c.execute("DELETE FROM wbs WHERE job_number = ?", (selected_job_number,))
            
            # Insert new/updated WBS data
            for item in st.session_state.wbs_items:
                c.execute('''
                    INSERT INTO wbs (
                        job_number, service_line, wbs_task, wbs_subtask, qty,
                        unit_of_measure, contract_vs_co, fpa_type, fpa_subtype,
                        budgeted_revenue, budgeted_hours, budgeted_cost
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    selected_job_number, item['service_line'], item['wbs_task'], 
                    item['wbs_subtask'], item['qty'], item['unit_of_measure'],
                    item['contract_vs_co'], item['fpa_type'], item['fpa_subtype'],
                    item['budgeted_revenue'], item['budgeted_hours'], item['budgeted_cost']
                ))
            
            st.success("✅ WBS saved successfully!")
            st.session_state.wbs_items = []  # Clear session state
            st.rerun()
    
    else:
        st.info("📝 No WBS items yet. Click 'Add a WBS Line Item' to get started.")

    conn.close()
