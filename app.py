from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id

app = Flask(__name__)
app.secret_key = "dev"  # TODO: replace with a real secret-key strategy before production

with app.app_context():
    init_db()
    seed_db()


@app.context_processor
def inject_current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return {}
    return {"current_user": get_user_by_id(user_id)}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email:
        return render_template(
            "register.html", error="Name and email are required.",
            name=name, email=email,
        )

    if len(password) < 8:
        return render_template(
            "register.html", error="Password must be at least 8 characters.",
            name=name, email=email,
        )

    if get_user_by_email(email):
        return render_template(
            "register.html", error="An account with that email already exists.",
            name=name, email=email,
        )

    user_id = create_user(name, email, password)
    if user_id is None:
        return render_template(
            "register.html", error="An account with that email already exists.",
            name=name, email=email,
        )

    session["user_id"] = user_id
    return redirect(url_for("landing"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template(
            "login.html", error="Email and password are required.",
            email=email,
        )

    user = get_user_by_email(email)

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template(
            "login.html", error="Invalid email or password.",
            email=email,
        )

    session["user_id"] = user["id"]
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if session.get("user_id") is None:
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "2026-01-15",
    }
    stats = {
        "total_spent": 386.25,
        "transaction_count": 8,
        "top_category": "Food",
    }
    transactions = [
        {"date": "2026-07-02", "description": "Groceries", "category": "Food", "amount": 42.50},
        {"date": "2026-07-03", "description": "Bus pass", "category": "Transport", "amount": 15.00},
        {"date": "2026-07-05", "description": "Electricity bill", "category": "Bills", "amount": 120.00},
        {"date": "2026-07-08", "description": "Pharmacy", "category": "Health", "amount": 60.00},
    ]
    categories = [
        {"name": "Food", "total": 76.25, "pct": 20},
        {"name": "Bills", "total": 120.00, "pct": 31},
        {"name": "Transport", "total": 15.00, "pct": 4},
        {"name": "Health", "total": 60.00, "pct": 16},
    ]
    return render_template(
        "profile.html", user=user, stats=stats,
        transactions=transactions, categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
