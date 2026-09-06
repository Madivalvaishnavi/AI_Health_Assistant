import sqlite3


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return sqlite3.connect("health.db")


# ============================================================
# CREATE DATABASE AND TABLES
# ============================================================

connection = get_connection()
cursor = connection.cursor()


# ============================================================
# MEDICINES TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    time TEXT NOT NULL,
    active INTEGER DEFAULT 1
)
""")


# ============================================================
# ADD ACTIVE COLUMN TO OLD DATABASE
# ============================================================

cursor.execute("PRAGMA table_info(medicines)")
medicine_columns = [column[1] for column in cursor.fetchall()]

if "active" not in medicine_columns:

    cursor.execute("""
    ALTER TABLE medicines
    ADD COLUMN active INTEGER DEFAULT 1
    """)


# ============================================================
# MEDICATION ADHERENCE TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS medication_adherence(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    UNIQUE(medicine_id, date),
    FOREIGN KEY (medicine_id)
    REFERENCES medicines(id)
)
""")


# ============================================================
# FITNESS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS fitness(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    steps INTEGER,
    calories INTEGER,
    water REAL
)
""")


# ============================================================
# USERS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")


# ============================================================
# HEALTH GOALS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_goals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    steps_goal INTEGER,
    water_goal REAL,
    calories_goal INTEGER
)
""")


# ============================================================
# CAREGIVERS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS caregivers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caregiver_name TEXT,
    caregiver_contact TEXT
)
""")


# ============================================================
# SAVE CHANGES
# ============================================================

connection.commit()
connection.close()

print("Database Created Successfully")


# ============================================================
# VIEW FITNESS DATA
# ============================================================

def view_fitness():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM fitness
    """)

    data = cursor.fetchall()

    connection.close()

    return data


# ============================================================
# DELETE MEDICINE
# ============================================================
# This permanently removes the medicine and
# all of its medication adherence history.

def delete_medicine_from_database(medicine_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Delete adherence records first
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
        print("Database Delete Error:", e)

        return False

    finally:

        connection.close()