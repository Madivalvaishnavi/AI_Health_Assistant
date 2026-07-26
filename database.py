import sqlite3
connection = sqlite3.connect("health.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
id INTEGER PRIMARY KEY AUTOINCREMENT,
medicine_name TEXT,
dosage TEXT,
time TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS fitness(
id INTEGER PRIMARY KEY AUTOINCREMENT,
steps INTEGER,
calories INTEGER,
water REAL
)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT)
""")
connection.commit()
connection.close()
print("Database Created Successfully")

def view_fitness():
    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM fitness")

    fitness_data = cursor.fetchall()

    connection.close()

    return fitness_data