import sqlite3
import json
import datetime

DB_NAME = "spider_history.db"

def init_db():
    """Creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # We store the entire audit result as a big JSON text blob
    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            full_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(url, score, data_dict):
    """Saves a new scan to the history."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Convert the dictionary to a string so we can save it
    data_str = json.dumps(data_dict)
    
    c.execute("INSERT INTO scans (url, score, full_data) VALUES (?, ?, ?)", 
              (url, score, data_str))
    conn.commit()
    conn.close()

def get_recent_scans(limit=10):
    """Fetches the last X scans for the sidebar."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, url, score, timestamp FROM scans ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_scan_by_id(scan_id):
    """Loads a specific old report."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT full_data FROM scans WHERE id=?", (scan_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0]) # Convert string back to Python Dictionary
    return None