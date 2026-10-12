import sqlite3

DATABASE_NAME = "students.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            course TEXT,
            address TEXT,
            enrollment_date TEXT
        )
    """)

    connection.commit()
    connection.close()