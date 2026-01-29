# -------------------------
# Imports
# -------------------------
from flask import Flask, render_template, request, redirect, session
import sqlite3

from ml.predict import predict_churn
from analytics.retention_engine import retention_strategy

# -------------------------
# Create Flask App
# -------------------------
app = Flask(__name__)
app.secret_key = "secret123"   # for sessions

# -------------------------
# Dashboard (Single Page App)
# -------------------------
@app.route("/")
def dashboard():
    user = session.get("user")
    return render_template("dashboard.html", user=user)

# -------------------------
# Predict Page
# -------------------------
@app.route("/predict")
def predict():
    return render_template("predict.html")

# -------------------------
# Retention Engine (POST)
# -------------------------
@app.route("/retention", methods=["POST"])
def retention():
    tenure = int(request.form["tenure"])
    monthly = float(request.form["monthly"])
    total = float(request.form["total"])
    calls = int(request.form["calls"])

    probability, risk = predict_churn(
        tenure, monthly, total, calls
    )

    actions = retention_strategy(risk)

    return render_template(
        "retention.html",
        probability=probability,
        risk=risk,
        actions=actions
    )

# -------------------------
# Business Insights
# -------------------------
@app.route("/insights")
def insights():
    # Later this will come from DB
    high = 3
    medium = 4
    low = 5

    return render_template(
        "insights.html",
        high=high,
        medium=medium,
        low=low
    )

# -------------------------
# Register (Modal submits here)
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
    except:
        conn.close()
        return "User already exists"

    conn.close()
    session["user"] = username
    return redirect("/")

# -------------------------
# Login (Modal submits here)
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = username
        return redirect("/")
    else:
        return "Invalid credentials"

# -------------------------
# Logout
# -------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
