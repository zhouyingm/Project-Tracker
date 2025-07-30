import pyodbc

# Create the connection using Windows credentials
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=dwh.beis.com;'
    r'DATABASE=APS_ADHOC_JOBCOST;'
    r'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Fix the SQL syntax: "TOP 10 *" instead of "TOP 10*,"
cursor.execute("SELECT TOP 10 * FROM JOB_COST_DETAIL")  # This will throw an error because * and status overlap

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
