import sqlite3
from datetime import date


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return sqlite3.connect("health.db")


# ============================================================
# CREATE MEDICATION TABLE
# ============================================================

def create_medicine_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        time TEXT NOT NULL,
        active INTEGER DEFAULT 1
    )
    """)

    # Check whether active column already exists
    cursor.execute("PRAGMA table_info(medicines)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add active column to older databases
    if "active" not in columns:
        cursor.execute("""
        ALTER TABLE medicines
        ADD COLUMN active INTEGER DEFAULT 1
        """)

    connection.commit()
    connection.close()


# ============================================================
# CREATE MEDICATION ADHERENCE TABLE
# ============================================================

def create_adherence_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medication_adherence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        UNIQUE(medicine_id, date)
    )
    """)

    connection.commit()
    connection.close()


# ============================================================
# INITIALIZE MEDICATION TABLES
# ============================================================

def initialize_medication_tables():

    create_medicine_table()
    create_adherence_table()


# ============================================================
# ADD MEDICINE
# ============================================================

def add_medicine(name, dosage, time):

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO medicines
    (medicine_name, dosage, time, active)
    VALUES (?, ?, ?, 1)
    """, (name, dosage, time))

    connection.commit()
    connection.close()


# ============================================================
# VIEW ACTIVE MEDICINES
# ============================================================

def view_medicines():

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, medicine_name, dosage, time
    FROM medicines
    WHERE active = 1
    ORDER BY time
    """)

    medicines = cursor.fetchall()

    connection.close()

    return medicines


# ============================================================
# DELETE MEDICINE
# ============================================================
# Permanently deletes the medicine and its adherence history.

def delete_medicine(medicine_id):

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Delete adherence history first
        cursor.execute("""
        DELETE FROM medication_adherence
        WHERE medicine_id = ?
        """, (medicine_id,))

        # Delete medicine
        cursor.execute("""
        DELETE FROM medicines
        WHERE id = ?
        """, (medicine_id,))

        deleted = cursor.rowcount

        connection.commit()

        return deleted > 0

    except Exception as e:

        connection.rollback()
        print("Delete Error:", e)

        return False

    finally:

        connection.close()


# ============================================================
# COMPLETE MEDICINE
# ============================================================
# Marks medicine as completed.
# Medicine disappears from active list,
# but adherence history remains.

def complete_medicine(medicine_id):

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
        UPDATE medicines
        SET active = 0
        WHERE id = ?
        """, (medicine_id,))

        updated = cursor.rowcount

        connection.commit()

        return updated > 0

    except Exception as e:

        connection.rollback()
        print("Complete Error:", e)

        return False

    finally:

        connection.close()


# ============================================================
# MARK MEDICATION STATUS
# ============================================================

def mark_medication_status(medicine_id, status):

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    today = date.today().isoformat()

    try:

        # Check whether today's record already exists
        cursor.execute("""
        SELECT id
        FROM medication_adherence
        WHERE medicine_id = ?
        AND date = ?
        """, (medicine_id, today))

        existing_record = cursor.fetchone()

        if existing_record:

            cursor.execute("""
            UPDATE medication_adherence
            SET status = ?
            WHERE medicine_id = ?
            AND date = ?
            """, (status, medicine_id, today))

        else:

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

        return True

    except Exception as e:

        connection.rollback()
        print("Medication Status Error:", e)

        return False

    finally:

        connection.close()


# ============================================================
# VIEW TODAY'S ADHERENCE
# ============================================================

def view_today_adherence():

    initialize_medication_tables()

    connection = get_connection()
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
    AND medicines.active = 1
    ORDER BY medicines.time
    """, (today,))

    records = cursor.fetchall()

    connection.close()

    return records


# ============================================================
# CALCULATE TODAY'S MEDICATION ADHERENCE
# ============================================================

def calculate_adherence():

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    today = date.today().isoformat()

    # Total active medicines
    cursor.execute("""
    SELECT COUNT(*)
    FROM medicines
    WHERE active = 1
    """)

    total = cursor.fetchone()[0]

    # Taken medicines
    cursor.execute("""
    SELECT COUNT(*)
    FROM medication_adherence
    JOIN medicines
    ON medication_adherence.medicine_id = medicines.id
    WHERE medication_adherence.date = ?
    AND medication_adherence.status = 'Taken'
    AND medicines.active = 1
    """, (today,))

    taken = cursor.fetchone()[0]

    connection.close()

    if total == 0:
        return 0

    adherence = (taken / total) * 100

    return round(adherence, 2)


# ============================================================
# GET ADHERENCE SUMMARY
# ============================================================

def get_adherence_summary():

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    today = date.today().isoformat()

    # Total active medicines
    cursor.execute("""
    SELECT COUNT(*)
    FROM medicines
    WHERE active = 1
    """)

    total = cursor.fetchone()[0]

    # Taken
    cursor.execute("""
    SELECT COUNT(*)
    FROM medication_adherence
    JOIN medicines
    ON medication_adherence.medicine_id = medicines.id
    WHERE medication_adherence.date = ?
    AND medication_adherence.status = 'Taken'
    AND medicines.active = 1
    """, (today,))

    taken = cursor.fetchone()[0]

    # Missed
    cursor.execute("""
    SELECT COUNT(*)
    FROM medication_adherence
    JOIN medicines
    ON medication_adherence.medicine_id = medicines.id
    WHERE medication_adherence.date = ?
    AND medication_adherence.status = 'Missed'
    AND medicines.active = 1
    """, (today,))

    missed = cursor.fetchone()[0]

    pending = total - taken - missed

    connection.close()

    if total == 0:
        adherence = 0
    else:
        adherence = (taken / total) * 100

    return {
        "total": total,
        "taken": taken,
        "missed": missed,
        "pending": pending,
        "adherence": round(adherence, 2)
    }


# ============================================================
# VIEW MEDICATION HISTORY
# ============================================================

def view_medication_history():

    initialize_medication_tables()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        medication_adherence.id,
        medicines.medicine_name,
        medicines.dosage,
        medicines.time,
        medication_adherence.date,
        medication_adherence.status
    FROM medication_adherence
    JOIN medicines
    ON medication_adherence.medicine_id = medicines.id
    ORDER BY medication_adherence.date DESC
    """ )

    history = cursor.fetchall()

    connection.close()

    return history