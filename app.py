from flask import Flask, render_template, request, redirect, url_for, session
from collections import defaultdict
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Lưu users và chi tiêu theo từng user
users = {"admin": "123"}
expenses = defaultdict(list)

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("index"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_template("register.html", error="⚠️ Tài khoản đã tồn tại!")

        users[username] = password
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        return render_template("login.html", error="⚠️ Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/index", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user_expenses = expenses[username]

    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = int(request.form["amount"])
        note = request.form.get("note", "")

        user_expenses.append({
            "date": date or datetime.date.today().isoformat(),
            "category": category,
            "amount": amount,
            "note": note
        })

    # Tính tổng theo danh mục cho biểu đồ
    category_totals = {}
    for item in user_expenses:
        category_totals[item["category"]] = category_totals.get(item["category"], 0) + item["amount"]

    return render_template(
        "index.html",
        username=username,
        expenses=user_expenses,
        category_totals=category_totals
    )

    
