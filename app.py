from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/submitTNA", methods=["POST"])
def submit_tna():
    # insert into SQL
    return redirect("/dashboard")

@app.route("/analytics")
def analytics():
    # fetch data
    return render_template("analytics.html")