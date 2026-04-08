import sqlite3
from pathlib import Path

from ..config import DATABASE_PATH

DB_PATH = Path(DATABASE_PATH)


# DB connection
def get_connection():
    return sqlite3.connect(DB_PATH)


# CREATE TABLE iss_data


def create_table():
    # conn = get_connection()
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS iss_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            latitude REAL,
            longitude REAL,
            time TEXT,
            speed REAL
            )               """
        )


def insert_data(timestamp, latitude, longitude, time, speed):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO iss_data (timestamp, latitude, longitude, time, speed)
            VALUES (?, ?, ?, ?, ?)
            """,
            (timestamp, latitude, longitude, time, speed),
        )


def add_datetime_column():
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""ALTER TABLE iss_data ADD COLUMN time TEXT""")
        except sqlite3.OperationalError:
            pass
