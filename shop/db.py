"""The shop's SQLite database."""
import sqlite3
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "shop.db"
SCHEMA = Path(__file__).resolve().parent.parent / "db" / "schema.sql"


def connect():
    conn = sqlite3.connect(PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create():
    with connect() as conn:
        conn.executescript(SCHEMA.read_text())
