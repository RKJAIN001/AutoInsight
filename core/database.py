import sqlite3
import os
import bcrypt
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "autoinsight.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_database():
    """Creates the users and files tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()

def create_user(username, password):
    """
    Registers a new user. Returns (success: bool, message: str).
    Password is hashed with bcrypt before storage - never stored in plain text.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username already exists."

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, password_hash.decode("utf-8"), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return True, "Account created successfully."

def verify_user(username, password):
    """
    Checks login credentials. Returns (success: bool, user_id_or_message).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "No account found with that username."

    user_id, stored_hash = row
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True, user_id
    else:
        return False, "Incorrect password."

def save_user_file_record(user_id, filename, filepath):
    """Records that a user uploaded a file, and where it's stored on disk."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_files (user_id, filename, filepath, uploaded_at) VALUES (?, ?, ?, ?)",
        (user_id, filename, filepath, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_user_files(user_id):
    """Returns a list of (file_id, filename, filepath, uploaded_at) for a given user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT file_id, filename, filepath, uploaded_at FROM user_files WHERE user_id = ? ORDER BY uploaded_at DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_user_file(file_id, user_id):
    """
    Deletes a file record from the database and removes the file from disk.
    Checks user_id matches, so a user can only delete their own files.
    Returns (success: bool, message: str).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT filepath FROM user_files WHERE file_id = ? AND user_id = ?",
        (file_id, user_id)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False, "File not found or does not belong to this user."

    filepath = row[0]

    cursor.execute("DELETE FROM user_files WHERE file_id = ? AND user_id = ?", (file_id, user_id))
    conn.commit()
    conn.close()

    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError as e:
            return True, f"Database record deleted, but could not remove file from disk: {e}"

    return True, "File deleted successfully."