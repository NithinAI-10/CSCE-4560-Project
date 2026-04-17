from flask import Flask, render_template, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

DB_NAME = "store.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            delivery_address TEXT NOT NULL,
            payment_status TEXT NOT NULL DEFAULT 'paid',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)

    conn.commit()
    conn.close()


def valid_email(email):
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email) is not None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print("REGISTER DATA:", data)

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    verify_password = data.get("verify_password", "")

    if not full_name or not email or not password or not verify_password:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    if not valid_email(email):
        return jsonify({"success": False, "message": "Invalid email address."}), 400

    if password != verify_password:
        return jsonify({"success": False, "message": "Passwords do not match."}), 400

    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters."}), 400

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash)
            VALUES (?, ?, ?)
        """, (full_name, email, password_hash))

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Account created successfully."}), 201

    except sqlite3.IntegrityError as e:
        print("REGISTER INTEGRITY ERROR:", e)
        return jsonify({"success": False, "message": "Email already exists."}), 400

    except Exception as e:
        print("REGISTER SERVER ERROR:", e)
        return jsonify({"success": False, "message": "Server error."}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, email, password_hash
            FROM users
            WHERE email = ?
        """, (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({"success": False, "message": "Invalid email or password."}), 401

        if not check_password_hash(user["password_hash"], password):
            return jsonify({"success": False, "message": "Invalid email or password."}), 401

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"]
            }
        }), 200

    except Exception:
        return jsonify({"success": False, "message": "Server error."}), 500


@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()

    user_id = data.get("user_id")
    delivery_address = data.get("delivery_address", "").strip()
    items = data.get("items", [])

    if not user_id or not delivery_address or not items:
        return jsonify({
            "success": False,
            "message": "User, delivery address, and items are required."
        }), 400

    try:
        total_amount = 0.0
        for item in items:
            quantity = int(item.get("quantity", 0))
            price = float(item.get("price", 0))
            total_amount += quantity * price

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, delivery_address, payment_status)
            VALUES (?, ?, ?, ?)
        """, (user_id, total_amount, delivery_address, "paid"))

        order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_name, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                item.get("product_name", "Unknown Item"),
                int(item.get("quantity", 1)),
                float(item.get("price", 0))
            ))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Order placed successfully.",
            "order_id": order_id,
            "total_amount": total_amount
        }), 201

    except Exception:
        return jsonify({"success": False, "message": "Server error."}), 500


@app.route("/orders/<int:user_id>", methods=["GET"])
def get_orders(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, total_amount, delivery_address, payment_status, created_at
            FROM orders
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        orders = cursor.fetchall()

        result = []
        for order in orders:
            cursor.execute("""
                SELECT product_name, quantity, price
                FROM order_items
                WHERE order_id = ?
            """, (order["id"],))
            items = cursor.fetchall()

            result.append({
                "order_id": order["id"],
                "total_amount": order["total_amount"],
                "delivery_address": order["delivery_address"],
                "payment_status": order["payment_status"],
                "created_at": order["created_at"],
                "items": [
                    {
                        "product_name": item["product_name"],
                        "quantity": item["quantity"],
                        "price": item["price"]
                    } for item in items
                ]
            })

        conn.close()
        return jsonify({"success": True, "orders": result}), 200

    except Exception:
        return jsonify({"success": False, "message": "Server error."}), 500

init_db()

if __name__ == "__main__":
    app.run(debug=True)
