import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DATABASE", "weapon_db")

    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("schema.sql") as f:
        sql = f.read()

    for stmt in sql.split(";"):
        if stmt.strip():
            cursor.execute(stmt)

    conn.commit()
    cursor.close()
    conn.close()
