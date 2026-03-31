import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def connect(database: str | None = None):
    return mysql.connector.connect(
        host=os.getenv("HOST", "localhost"),
        user=os.getenv("USER", "root"),
        password=os.getenv("PASSWORD"),
        database=database or os.getenv("DATABASE", "mao_records"),
        port=int(os.getenv("PORT", 3306)),
    )
