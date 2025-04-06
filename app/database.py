"""Database module for the AI Travel Assistant."""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
import json

# Ensure data directory exists
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "demo_travel_app.db"

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    try:
        # Create conversations table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            session_id TEXT PRIMARY KEY,
            history TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
    finally:
        conn.close()

def save_conversation(session_id: str, history: List[Dict[str, Any]]):
    """Save or update a conversation history."""
    conn = get_db_connection()
    try:
        conn.execute("""
        INSERT INTO conversations (session_id, history) VALUES (?, ?)
        ON CONFLICT(session_id) DO UPDATE SET 
            history = excluded.history,
            updated_at = CURRENT_TIMESTAMP
        """, (session_id, json.dumps(history)))
        conn.commit()
    finally:
        conn.close()

def get_conversation(session_id: str) -> List[Dict[str, Any]]:
    """Retrieve a conversation history by session_id."""
    conn = get_db_connection()
    try:
        result = conn.execute(
            "SELECT history FROM conversations WHERE session_id = ?",
            (session_id,)
        ).fetchone()
        return json.loads(result['history']) if result else []
    finally:
        conn.close()

# Initialize the database when the module is imported
init_db()
