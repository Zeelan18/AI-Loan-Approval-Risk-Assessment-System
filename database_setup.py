import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(
    "database/loan_predictions.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    gender TEXT,
    married TEXT,
    dependents TEXT,
    education TEXT,
    self_employed TEXT,
    applicant_income REAL,
    coapplicant_income REAL,
    loan_amount REAL,
    credit_history REAL,
    property_area TEXT,
    prediction TEXT,
    probability REAL,
    risk TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")