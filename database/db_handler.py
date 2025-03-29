import sqlite3
from typing import List, Dict, Any
import os

class DatabaseHandler:
    def __init__(self, db_path: str = "bugs.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with schema"""
        with sqlite3.connect(self.db_path) as conn:
            with open('database/schema.sql', 'r') as schema_file:
                conn.executescript(schema_file.read())

    def add_code_sample(self, file_name: str, code_content: str, has_bugs: bool) -> int:
        """Add a new code sample to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO code_samples (file_name, code_content, has_bugs) VALUES (?, ?, ?)",
                (file_name, code_content, has_bugs)
            )
            return cursor.lastrowid

    def add_bug(self, code_sample_id: int, bug_type: str, description: str, 
                line_number: int, severity: str) -> int:
        """Add a new bug to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO bugs (code_sample_id, bug_type, description, 
                line_number, severity) VALUES (?, ?, ?, ?, ?)""",
                (code_sample_id, bug_type, description, line_number, severity)
            )
            return cursor.lastrowid

    def add_fix(self, bug_id: int, fixed_code: str, fix_description: str):
        """Add a fix for a bug"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fixes (bug_id, fixed_code, fix_description) VALUES (?, ?, ?)",
                (bug_id, fixed_code, fix_description)
            )

    def get_code_samples(self) -> List[Dict[str, Any]]:
        """Get all code samples with their bugs"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cs.*, b.*, f.*
                FROM code_samples cs
                LEFT JOIN bugs b ON cs.id = b.code_sample_id
                LEFT JOIN fixes f ON b.id = f.bug_id
            """)
            return [dict(row) for row in cursor.fetchall()]

    def get_bugs_by_type(self, bug_type: str) -> List[Dict[str, Any]]:
        """Get all bugs of a specific type"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.*, f.*
                FROM bugs b
                LEFT JOIN fixes f ON b.id = f.bug_id
                WHERE b.bug_type = ?
            """, (bug_type,))
            return [dict(row) for row in cursor.fetchall()] 