-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
    job_number TEXT PRIMARY KEY,
    branch_number TEXT,
    job_name TEXT,
    salesforce_id TEXT
);

-- Create wbs table
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
);

-- Insert sample jobs
INSERT OR IGNORE INTO jobs VALUES ("20725", "0508", "SCVWA Filters", "100000");
INSERT OR IGNORE INTO jobs VALUES ("20726", "0508", "SCVWA Filters", "100001");
INSERT OR IGNORE INTO jobs VALUES ("20727", "0509", "Industrial Coating", "100002");
INSERT OR IGNORE INTO jobs VALUES ("20728", "0510", "Pipeline Protection", "100003");
INSERT OR IGNORE INTO jobs VALUES ("20729", "0511", "Tank Coating", "100004");

-- Insert sample WBS data for job 20725
INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20725", "Coatings", "1st Fl Coating", "1st Fl Small Pipe", 5000.0, "Linear Ft", "Contract", "Services", "Labor", 20000.0, 100.0, 10000.0);

INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20725", "Coatings", "2nd Fl Coating", "2nd Fl Storm Pipe", 300.0, "Linear Ft", "CO", "Services", "Labor", 10000.0, 65.0, 6500.0);

INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20725", "Coatings", "3rd Fl Coating", "3rd Fl Large Pipe", 800.0, "Linear Ft", "Contract", "Services", "Labor", 15000.0, 80.0, 8000.0);

INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20725", "Materials", "Surface Prep", "Cleaning", 1.0, "Lot", "Contract", "Materials", "Other", 5000.0, 20.0, 3000.0);

INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20725", "Equipment", "Scaffolding", "Setup", 1.0, "Lot", "Contract", "Equipment", "Other", 8000.0, 40.0, 4000.0);

-- Insert sample WBS data for job 20726
INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20726", "Coatings", "Primary Coating", "Main Structure", 2000.0, "Sq Ft", "Contract", "Services", "Labor", 25000.0, 120.0, 12000.0);

INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20726", "Coatings", "Secondary Coating", "Support Beams", 500.0, "Sq Ft", "CO", "Services", "Labor", 12000.0, 60.0, 6000.0);

INSERT INTO wbs (job_number, service_line, wbs_task, wbs_subtask, qty, unit_of_measure, contract_vs_co, fpa_type, fpa_subtype, budgeted_revenue, budgeted_hours, budgeted_cost) 
VALUES ("20726", "Materials", "Primer", "Application", 1.0, "Lot", "Contract", "Materials", "Other", 3000.0, 15.0, 2000.0); 