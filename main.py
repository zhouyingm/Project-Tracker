import streamlit as st
from pages import Job_Info as job_info
from pages import Create_WBS as create_wbs
from pages import View_Data as view_data

page = st.sidebar.selectbox("Navigate to", ["Job Info", "Create WBS", "View Data"])

if page == "Job Info":
    job_info.show()
elif page == "Create WBS":
    create_wbs.show()
elif page == "View Data":
    view_data.show()
