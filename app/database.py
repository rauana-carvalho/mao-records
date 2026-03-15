import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def connect():
    connection = mysql.connector.connect(
        host=os.getenv("HOST", "localhost"),
        user=os.getenv("USER", "root"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE", "maos_records"),
        port=int(os.getenv("PORT", 3306))
    )
    return connection