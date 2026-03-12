from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Database connection
server = 'lms-sql-server-rt.database.windows.net'
database = 'LMSDatabase'
username = 'lmsadmin'
password = 'Password@2026q1'

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

# Home page (login page)
@app.route("/")
def home():
    return render_template("index.html")


# Login validation
@app.route("/login", methods=["POST"])
def login():

    userid = request.form["username"]
    password_input = request.form["password"]

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    query = """
    SELECT * FROM Users
    WHERE username=? AND password=?
    """

    cursor.execute(query, userid, password_input)

    user = cursor.fetchone()

    conn.close()

    if user:
        return redirect("/dashboard")
    else:
        return "Invalid username or password"


# Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Courses page
@app.route("/courses")
def courses():
    return render_template("courses.html")


# Video player page
@app.route("/player")
def player():
    return render_template("player.html")


# Training Needs page
@app.route("/tna")
def tna():
    return render_template("tna.html")


# Submit TNA form
@app.route("/submitTNA", methods=["POST"])
def submit_tna():

    employee_name = request.form["employee_name"]
    department = request.form["department"]
    skill_gap = request.form["skill_gap"]
    training_area = request.form["training_area"]
    experience_level = request.form["experience_level"]
    training_mode = request.form["training_mode"]
    comments = request.form["comments"]

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    query = """
    INSERT INTO TrainingNeeds
    (employee_name, department, skill_gap, training_area,
     experience_level, training_mode, comments, active)
    VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """

    cursor.execute(
        query,
        employee_name,
        department,
        skill_gap,
        training_area,
        experience_level,
        training_mode,
        comments
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# TNA Analytics
@app.route("/analytics")
def analytics():

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT employee_name, department, skill_gap,
               training_area, experience_level,
               training_mode, comments
        FROM TrainingNeeds
        WHERE active=1
        ORDER BY employee_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return render_template("analytics.html", rows=rows)


# Run app
if __name__ == "__main__":
    app.run()