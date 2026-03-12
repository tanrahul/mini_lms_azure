import azure.functions as func
import pyodbc

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:

        # Read values from HTML form
        username = req.form.get("username")
        password = req.form.get("password")

        if not username or not password:
            return func.HttpResponse(
                "Username or password missing",
                status_code=400
            )

        # Azure SQL connection details
        conn = pyodbc.connect(
          "Driver={ODBC Driver 18 for SQL Server};"
          "SERVER=tcp:lms-sql-server-rt.database.windows.net,1433;"
          "Database=LMSDatabase;"
          "Uid=lmsadmin;"
          "Pwd=Password@2026q1;"
          "Encrypt=yes;"
          "TrustServerCertificate=no;"
          "Connection Timeout=30;"
        )

        cursor = conn.cursor()

        query = """
        SELECT username
        FROM Users
        WHERE username=? AND password=?
        """

        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return func.HttpResponse(
                 "",
                status_code=302,
                 headers={
                     "Location": "http://localhost:5500/dashboard.html"
                 }
             )

        else:
            return func.HttpResponse(
                "Invalid username or password",
                status_code=401
            )

    except Exception as e:
        return func.HttpResponse(
            f"Error occurred: {str(e)}",
            status_code=500
        )