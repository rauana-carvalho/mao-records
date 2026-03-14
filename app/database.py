import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("./.env").with_name(".env"))

def connect():
    connection = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE", "maos_records"),
        port=os.getenv("PORT", 3306)
    )

    return connection
