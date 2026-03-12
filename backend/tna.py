import sqlite3

def save_tna(data):

    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO TrainingNeeds (employee, skill) VALUES (?,?)",
        (data["employee"], data["skill"])
    )

    conn.commit()
    conn.close()

    return {"message": "TNA Saved"}