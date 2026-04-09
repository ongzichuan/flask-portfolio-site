from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret")

DB_CONFIG = {
    "host": "mysql",
    "database": os.getenv("MYSQL_DATABASE"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "port": 3306,
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_comments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, name, content, created_at
        FROM comments
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_comment(name, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (name, content) VALUES (%s, %s)",
        (name, content)
    )
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    comments = []

    try:
        init_db()

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            content = request.form.get("comment", "").strip()

            if content:
                add_comment(name or "Anonymous", content)

            return redirect(url_for("home") + "#comments")

        comments = get_comments()

    except Error as e:
        error = str(e)

    return render_template("index.html", comments=comments, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)