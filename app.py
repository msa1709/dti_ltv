from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("dti.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dti_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income REAL,
            expenses REAL,
            dti REAL,
            status TEXT,
            property_value REAL,
            loan_amount REAL,
            ltv REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate_dti():
    data = request.get_json()

    income = float(data["income"])
    expenses = float(data["expenses"])

    dti = round((expenses / income) * 100, 2)

    if dti <= 50:
        status = "✅ Qualified"
        show_ltv = True
    else:
        status = "❌ Not Qualified"
        show_ltv = False

    conn = sqlite3.connect("dti.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO dti_records (income, expenses, dti, status)
        VALUES (?, ?, ?, ?)
    """, (income, expenses, dti, status))
    conn.commit()
    conn.close()

    return jsonify({
        "dti": dti,
        "status": status,
        "show_ltv": show_ltv
    })

@app.route("/calculate_ltv", methods=["POST"])
def calculate_ltv():
    data = request.get_json()

    property_value = float(data["property_value"])
    loan_amount = float(data["loan_amount"])

    ltv = round((loan_amount / property_value) * 100, 2)

    conn = sqlite3.connect("dti.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE dti_records
        SET property_value=?, loan_amount=?, ltv=?
        WHERE id=(SELECT MAX(id) FROM dti_records)
    """, (property_value, loan_amount, ltv))
    conn.commit()
    conn.close()

    return jsonify({
        "ltv": ltv,
        "status": "✅ Acceptable LTV" if ltv <= 80 else "❌ High LTV"
    })

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
