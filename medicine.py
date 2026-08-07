import sqlite3
from datetime import date


# ============================================================
# ADD MEDICINE
# ============================================================

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
        """
        INSERT INTO medicines
        (medicine_name, dosage, time)
        VALUES (?, ?, ?)
        """,
        (name, dosage, time)
    )

    connection.commit()
    connection.close()


# ============================================================
# VIEW MEDICINES
# ============================================================

def view_medicines():

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM medicines
    """)

    medicines = cursor.fetchall()

    connection.close()

    return medicines


# ============================================================
# MARK MEDICINE STATUS
# ============================================================

def mark_medication_status(
    medicine_id,
    status
):

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    today = date.today().isoformat()

    cursor.execute("""
    INSERT INTO medication_adherence
    (
        medicine_id,
        date,
        status
    )
    VALUES (?, ?, ?)
    """, (
        medicine_id,
        today,
        status
    ))

    connection.commit()
    connection.close()


# ============================================================
# VIEW TODAY'S ADHERENCE
# ============================================================

def view_today_adherence():

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    today = date.today().isoformat()

    cursor.execute("""
    SELECT
        medication_adherence.id,
        medicines.medicine_name,
        medicines.dosage,
        medicines.time,
        medication_adherence.status
    FROM medication_adherence
    JOIN medicines
    ON medication_adherence.medicine_id = medicines.id
    WHERE medication_adherence.date = ?
    """, (today,))

    records = cursor.fetchall()

    connection.close()

    return records


# ============================================================
# CALCULATE MEDICATION ADHERENCE
# ============================================================

def calculate_adherence():

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    today = date.today().isoformat()

    cursor.execute("""
    SELECT COUNT(*)
    FROM medication_adherence
    WHERE date = ?
    """, (today,))

    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM medication_adherence
    WHERE date = ?
    AND status = 'Taken'
    """, (today,))

    taken = cursor.fetchone()[0]

    connection.close()

    if total == 0:
        return 0

    adherence = (taken / total) * 100

    return adherence