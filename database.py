import sqlite3

# ============================================================
# CREATE DATABASE AND TABLES
# ============================================================

connection = sqlite3.connect("health.db")
cursor = connection.cursor()


# ============================================================
# MEDICINES TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT,
    dosage TEXT,
    time TEXT
)
""")


# ============================================================
# MEDICATION ADHERENCE TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS medication_adherence(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
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
# FUNCTION TO VIEW FITNESS DATA
# ============================================================

def view_fitness():

    connection = sqlite3.connect("health.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM fitness
    """)

    data = cursor.fetchall()

    connection.close()

    return data