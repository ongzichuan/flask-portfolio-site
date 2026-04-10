from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import mysql.connector
import os
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret")

# ── Flask-Login ───────────────────────────────────────────────
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

DB_CONFIG = {
    "host": "mysql",
    "database": os.getenv("MYSQL_DATABASE"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "port": 3306,
}

# ── User class ────────────────────────────────────────────────
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# ── DB helpers ────────────────────────────────────────────────
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(256) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def get_comments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, content, created_at FROM comments ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_comment(name, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (name, content) VALUES (%s, %s)", (name, content))
    conn.commit()
    cursor.close()
    conn.close()

# ── Flask-Login user loader ───────────────────────────────────
@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row["id"], row["username"])
    return None

# ── Routes ────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    comments = []
    try:
        init_db()
        if request.method == "POST":
            # Task B: server-side protection
            if not current_user.is_authenticated:
                return redirect(url_for("login"))
            name = request.form.get("name", "").strip()
            content = request.form.get("comment", "").strip()
            if content:
                add_comment(name or "Anonymous", content)
            return redirect(url_for("home") + "#comments")
        comments = get_comments()
    except Error as e:
        error = str(e)

    return render_template("index.html", comments=comments, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    error = False
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        row = get_user_by_username(username)
        if row is None or not check_password_hash(row["password_hash"], password):
            error = True
        else:
            login_user(User(row["id"], row["username"]))
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
