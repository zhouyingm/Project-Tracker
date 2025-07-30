import sqlite3
from pathlib import Path

# Create database if it doesn't exist
DB_PATH = Path("project_tracker.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_number TEXT PRIMARY KEY,
            branch_number TEXT,
            job_name TEXT,
            salesforce_id TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_number TEXT,
            wbs_id TEXT,
            wbs_name TEXT,
            FOREIGN KEY(job_number) REFERENCES jobs(job_number)
        )
    """)
    conn.commit()
    conn.close()

init_db()

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Project Tracker", layout="wide")

# --- Title ---
st.title("📁 BrandSafway Project Management")

# --- Job Form ---
st.header("Step 1: Project Info")
job_number = st.text_input("Job Number")
branch_number = st.text_input("Branch Number")
job_name = st.text_input("Job Name")
salesforce_id = st.text_input("Salesforce ID (optional)")

# --- Step 2: Create WBS ---
st.header("Step 2: Create Work Breakdown Structure (WBS)")

num_rows = st.number_input("Number of WBS entries", min_value=1, max_value=20, value=3)

wbs_data = []
for i in range(int(num_rows)):
    col1, col2 = st.columns(2)
    wbs_id = col1.text_input(f"WBS ID {i+1}", key=f"id_{i}")
    wbs_name = col2.text_input(f"Name {i+1}", key=f"name_{i}")
    if wbs_id and wbs_name:
        wbs_data.append({"WBS ID": wbs_id, "Name": wbs_name})

# --- Step 3: Upload Cost File ---
st.header("Step 3: Upload Cost Excel File")
uploaded_file = st.file_uploader("Upload .xlsx file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    st.dataframe(df)

# --- Final Step ---
if st.button("Save to Database"):
    if not job_number or not branch_number:
        st.error("Please enter at least Job Number and Branch Number.")
    elif not wbs_data:
        st.error("Please enter at least one WBS entry.")
    else:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Save job info
            cursor.execute("""
                INSERT OR REPLACE INTO jobs (job_number, branch_number, job_name, salesforce_id)
                VALUES (?, ?, ?, ?)
            """, (job_number, branch_number, job_name, salesforce_id))

            # Save WBS entries
            for wbs in wbs_data:
                cursor.execute("""
                    INSERT INTO wbs (job_number, wbs_id, wbs_name)
                    VALUES (?, ?, ?)
                """, (job_number, wbs["WBS ID"], wbs["Name"]))

            conn.commit()
            conn.close()
            st.success(f"✅ Job {job_number} and {len(wbs_data)} WBS entries saved to database.")
        except Exception as e:
            st.error(f"❌ Failed to save: {e}")

