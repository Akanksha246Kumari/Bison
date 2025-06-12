import sqlite3
import json

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('maintenance_reports.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Creates the reports table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_data TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_report(report_data):
    """Saves a maintenance report to the database.
    
    Args:
        report_data (dict): A dictionary containing the report details.
    """
    conn = get_db_connection()
    # Store the whole report as a JSON string for flexibility
    report_data_json = json.dumps(report_data)
    conn.execute('INSERT INTO reports (report_data) VALUES (?)', (report_data_json,))
    conn.commit()
    conn.close()

def get_all_reports():
    """Retrieves all reports from the database."""
    conn = get_db_connection()
    reports_cursor = conn.execute('SELECT * FROM reports ORDER BY timestamp DESC').fetchall()
    conn.close()
    
    reports = []
    for row in reports_cursor:
        report = dict(row)
        report['report_data'] = json.loads(report['report_data'])
        reports.append(report)
        
    return reports

if __name__ == '__main__':
    # Initialize the database and table when the script is run directly
    create_table()
    print("Database and table created successfully.")
