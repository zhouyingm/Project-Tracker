import sqlite3
import os

def create_sample_database():
    """Create a sample job_master.db with sample data"""
    
    # Connect to database (will create if doesn't exist)
    db_path = os.path.join(os.getcwd(), "job_master.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create jobs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_number TEXT PRIMARY KEY,
            branch_number TEXT,
            job_name TEXT,
            salesforce_id TEXT
        )
    ''')
    
    # Create wbs table
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
    
    # Insert sample jobs
    sample_jobs = [
        ("20725", "0508", "SCVWA Filters", "100000"),
        ("20726", "0508", "SCVWA Filters", "100001"),
        ("20727", "0509", "Industrial Coating", "100002"),
        ("20728", "0510", "Pipeline Protection", "100003"),
        ("20729", "0511", "Tank Coating", "100004")
    ]
    
    for job in sample_jobs:
        try:
            c.execute("INSERT INTO jobs VALUES (?, ?, ?, ?)", job)
        except sqlite3.IntegrityError:
            print(f"Job {job[0]} already exists, skipping...")
    
    # Insert sample WBS data for job 20725
    sample_wbs = [
        ("20725", "Coatings", "1st Fl Coating", "1st Fl Small Pipe", 5000.0, "Linear Ft", "Contract", "Services", "Labor", 20000.0, 100.0, 10000.0),
        ("20725", "Coatings", "2nd Fl Coating", "2nd Fl Storm Pipe", 300.0, "Linear Ft", "CO", "Services", "Labor", 10000.0, 65.0, 6500.0),
        ("20725", "Coatings", "3rd Fl Coating", "3rd Fl Large Pipe", 800.0, "Linear Ft", "Contract", "Services", "Labor", 15000.0, 80.0, 8000.0),
        ("20725", "Materials", "Surface Prep", "Cleaning", 1.0, "Lot", "Contract", "Materials", "Other", 5000.0, 20.0, 3000.0),
        ("20725", "Equipment", "Scaffolding", "Setup", 1.0, "Lot", "Contract", "Equipment", "Other", 8000.0, 40.0, 4000.0)
    ]
    
    for wbs_item in sample_wbs:
        c.execute('''
            INSERT INTO wbs (
                job_number, service_line, wbs_task, wbs_subtask, qty,
                unit_of_measure, contract_vs_co, fpa_type, fpa_subtype,
                budgeted_revenue, budgeted_hours, budgeted_cost
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', wbs_item)
    
    # Insert sample WBS data for job 20726
    sample_wbs_20726 = [
        ("20726", "Coatings", "Primary Coating", "Main Structure", 2000.0, "Sq Ft", "Contract", "Services", "Labor", 25000.0, 120.0, 12000.0),
        ("20726", "Coatings", "Secondary Coating", "Support Beams", 500.0, "Sq Ft", "CO", "Services", "Labor", 12000.0, 60.0, 6000.0),
        ("20726", "Materials", "Primer", "Application", 1.0, "Lot", "Contract", "Materials", "Other", 3000.0, 15.0, 2000.0)
    ]
    
    for wbs_item in sample_wbs_20726:
        c.execute('''
            INSERT INTO wbs (
                job_number, service_line, wbs_task, wbs_subtask, qty,
                unit_of_measure, contract_vs_co, fpa_type, fpa_subtype,
                budgeted_revenue, budgeted_hours, budgeted_cost
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', wbs_item)
    
    # Commit changes and close
    conn.commit()
    conn.close()
    
    print("✅ Sample database 'job_master.db' created successfully!")
    print("📊 Sample data includes:")
    print("   - 5 sample jobs")
    print("   - WBS data for jobs 20725 and 20726")
    print("   - Various service lines, tasks, and budget information")

if __name__ == "__main__":
    create_sample_database() 