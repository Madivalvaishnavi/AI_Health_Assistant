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
# SAVE CHANGES
# ============================================================

connection.commit()

connection.close()


print("Database Created Successfully")


# ============================================================
# FUNCTION TO VIEW FITNESS DATA
# ============================================================

def view_fitness():

    connection = sqlite3.connect(
        "health.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM fitness
    """)

    data = cursor.fetchall()

    connection.close()

    return data