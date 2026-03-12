import azure.functions as func
import pyodbc


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:

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

        # Fetch active TNA records
        cursor.execute("""
        SELECT employee_name,
               department,
               skill_gap,
               training_area,
               experience_level,
               training_mode,
               comments,
               created_date
        FROM TrainingNeeds
        WHERE active = 1
        ORDER BY created_date DESC
        """)

        rows = cursor.fetchall()

        # Build HTML table
        html = """
        <html>
        <head>
        <title>TNA Analytics Dashboard</title>

        <style>

        body{
        font-family: Arial;
        background:#f4f6f9;
        padding:40px;
        }

        h2{
        text-align:center;
        }

        table{
        width:100%;
        border-collapse:collapse;
        background:white;
        }

        th{
        background:#0078d4;
        color:white;
        padding:12px;
        }

        td{
        padding:10px;
        border-bottom:1px solid #ddd;
        }

        tr:hover{
        background:#f2f2f2;
        }

        </style>

        </head>

        <body>

        <h2>Training Needs Analytics</h2>

        <table>

        <tr>
        <th>Employee</th>
        <th>Department</th>
        <th>Skill Gap</th>
        <th>Training Area</th>
        <th>Experience Level</th>
        <th>Training Mode</th>
        <th>Comments</th>
        <th>Submitted Date</th>
        </tr>
        """

        for r in rows:

            html += f"""
            <tr>
            <td>{r.employee_name}</td>
            <td>{r.department}</td>
            <td>{r.skill_gap}</td>
            <td>{r.training_area}</td>
            <td>{r.experience_level}</td>
            <td>{r.training_mode}</td>
            <td>{r.comments}</td>
            <td>{r.created_date}</td>
            </tr>
            """

        html += """
        </table>
        </body>
        </html>
        """

        return func.HttpResponse(html, mimetype="text/html")

    except Exception as e:

        return func.HttpResponse(
            f"Error occurred: {str(e)}",
            status_code=500
        )