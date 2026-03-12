import azure.functions as func
import pyodbc


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:

        # Read values from TNA form
        employee_name = req.form.get("employee_name")
        department = req.form.get("department")
        skill_gap = req.form.get("skill_gap")
        training_area = req.form.get("training_area")
        experience_level = req.form.get("experience_level")
        training_mode = req.form.get("training_mode")
        comments = req.form.get("comments")

        # Connect to Azure SQL
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=tcp:lms-sql-server-rt.database.windows.net,1433;"
            "DATABASE=LMSDatabase;"
            "UID=lmsadmin;"
            "PWD=Password@2026q1;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
        )

        cursor = conn.cursor()

        # Insert TNA record
        query = """
        INSERT INTO TrainingNeeds
        (employee_name, department, skill_gap, training_area,
        experience_level, training_mode, comments, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            employee_name,
            department,
            skill_gap,
            training_area,
            experience_level,
            training_mode,
            comments,
            1
        )

        conn.commit()

        # Redirect back to dashboard
        return func.HttpResponse(
            "",
            status_code=302,
            headers={"Location": "http://localhost:5500/dashboard.html"}
        )

    except Exception as e:

        return func.HttpResponse(
            f"Error occurred: {str(e)}",
            status_code=500
        )