import sqlite3

def add_medicine(name, dosage, time):
    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT,
            dosage TEXT,
            time TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO medicines (medicine_name, dosage, time) VALUES (?, ?, ?)",
        (name, dosage, time)
    )

    connection.commit()
    connection.close()


def view_medicines():
    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT,
            dosage TEXT,
            time TEXT
        )
    """)

    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    connection.close()

    return medicines