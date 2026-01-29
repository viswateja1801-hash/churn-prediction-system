@app.route("/retention", methods=["POST"])
def retention():
    name = request.form["name"]
    age = int(request.form["age"])
    tenure = int(request.form["tenure"])
    monthly = float(request.form["monthly"])
    total = float(request.form["total"])
    calls = int(request.form["calls"])

    probability, risk = predict_churn(
        tenure, monthly, total, calls
    )

    actions = retention_strategy(risk)

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers (name, age, tenure, monthly, total, risk)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, tenure, monthly, total, risk))

    conn.commit()
    conn.close()

    return render_template(
        "retention.html",
        probability=probability,
        risk=risk,
        actions=actions
    )
