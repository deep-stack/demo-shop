"""The shop's Postgres database, at DATABASE_URL in the environment or in .env."""
import os

import psycopg
from psycopg.rows import dict_row

from .monitoring import load_env


def connect():
    """A connection that commits when its block ends without an error."""
    load_env()
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)


def create():
    """Nothing to do: the database is created with its schema by compose.yaml."""
