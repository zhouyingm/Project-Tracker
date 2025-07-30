import streamlit as st
from pages import Job_Info as job_info
from pages import Create_WBS as create_wbs

page = st.sidebar.selectbox("Navigate to", ["Job Info", "Create WBS"])

if page == "Job Info":
    job_info.show()
elif page == "Create WBS":
    create_wbs.show()
