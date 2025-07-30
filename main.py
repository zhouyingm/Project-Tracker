import streamlit as st
import job_info
import create_wbs

page = st.sidebar.selectbox("Navigate to", ["Job Info", "Create WBS"])

if page == "Job Info":
    job_info.show()
elif page == "Create WBS":
    create_wbs.show()
