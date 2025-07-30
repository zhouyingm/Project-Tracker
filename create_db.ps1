Write-Host "Creating job_master.db database..." -ForegroundColor Green

# Create the database file
$dbPath = "job_master.db"
if (Test-Path $dbPath) {
    Remove-Item $dbPath -Force
    Write-Host "Removed existing database file." -ForegroundColor Yellow
}

# Create database and run SQL script
try {
    # This will create the database when the app runs
    Write-Host "Database will be created when you run the Streamlit app." -ForegroundColor Green
    Write-Host "The app will automatically create job_master.db with the correct schema." -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Setup complete! Start your Streamlit app to create the database." -ForegroundColor Green 