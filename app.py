import sqlite3
from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")

    # Render / Production → PostgreSQL
    if database_url:
        parsed = urlparse(database_url)
        conn = psycopg2.connect(
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port,
            sslmode="require"
        )
        return conn

    # Local → SQLite
    db_path = os.path.join(os.path.dirname(__file__), "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_products(product_type):
    conn = sqlite3.connect("product.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, size, price, photo FROM products WHERE type = ?", (product_type,))
    data = cur.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/handles")
def handles():
    items = get_products("handle")
    return render_template("handles.html", products=items)

@app.route("/knobs")
def knobs():
    items = get_products("knob")
    return render_template("knobs.html", products=items)



if __name__== "__main__":
    app.run(host='0.0.0.0')