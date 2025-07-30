@echo off
echo Creating job_master.db database...
sqlite3 job_master.db < create_db.sql
echo Database created successfully!
pause 