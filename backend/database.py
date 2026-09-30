"""SQLite persistence for number plate detection history."""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "plate_history.db"


def get_connection():
    """Create a connection to the local SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the detection history table if it does not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS detection_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                plate_text TEXT,
                detection_confidence REAL NOT NULL,
                ocr_confidence REAL NOT NULL,
                ocr_status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_detection(
    filename,
    plate_text,
    detection_confidence,
    ocr_confidence,
    ocr_status,
):
    """Save one detected plate and its OCR result."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO detection_history (
                filename,
                plate_text,
                detection_confidence,
                ocr_confidence,
                ocr_status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                filename,
                plate_text,
                detection_confidence,
                ocr_confidence,
                ocr_status,
            ),
        )

        return cursor.lastrowid


def get_detection_history(limit=50):
    """Return the newest detection records first."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                filename,
                plate_text,
                detection_confidence,
                ocr_confidence,
                ocr_status,
                created_at
            FROM detection_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]