# Project Tracker

A Streamlit-based project management application for tracking jobs and Work Breakdown Structure (WBS) data.

## Features

- **Job Information Management**: Add and manage job details
- **WBS Creation & Editing**: Create and edit Work Breakdown Structure items with Excel-like interface
- **Data Viewing & Filtering**: View and filter job and WBS data with export capabilities
- **Professional Interface**: Clean, modern UI with dropdown selections and data validation

## Database

The application uses `job_master.db` as the main database file, which contains:

### Tables
- **jobs**: Job information (job number, branch, name, Salesforce ID)
- **wbs**: Work Breakdown Structure items with budget data

### Sample Data
The database includes sample data for testing:
- 5 sample jobs (20725-20729)
- WBS data for jobs 20725 and 20726
- Various service lines, tasks, and budget information

## Setup

1. **Install Dependencies**:
   ```bash
   pip install streamlit pandas
   ```

2. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

3. **Database Creation**: The database will be automatically created when you first run the app.

## Usage

1. **Job Info Tab**: Add new jobs with job number, branch, name, and Salesforce ID
2. **Create WBS Tab**: Select a job and edit its WBS items in an Excel-like table
3. **View Data Tab**: View, filter, and export job and WBS data

## File Structure

```
Project-Tracker/
├── main.py                 # Main application entry point
├── job_master.db          # SQLite database (created automatically)
├── pages/
│   ├── Job_Info.py        # Job information management
│   ├── Create_WBS.py      # WBS creation and editing
│   └── View_Data.py       # Data viewing and filtering
├── create_sample_db.py    # Database creation script
├── create_db.sql          # SQL schema and sample data
└── README.md              # This file
```

## Database Schema

### Jobs Table
- `job_number` (TEXT, PRIMARY KEY)
- `branch_number` (TEXT)
- `job_name` (TEXT)
- `salesforce_id` (TEXT)

### WBS Table
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `job_number` (TEXT)
- `service_line` (TEXT)
- `wbs_task` (TEXT)
- `wbs_subtask` (TEXT)
- `qty` (REAL)
- `unit_of_measure` (TEXT)
- `contract_vs_co` (TEXT)
- `fpa_type` (TEXT)
- `fpa_subtype` (TEXT)
- `budgeted_revenue` (REAL)
- `budgeted_hours` (REAL)
- `budgeted_cost` (REAL)