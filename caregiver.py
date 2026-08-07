import sqlite3


# ============================================================
# ADD CAREGIVER
# ============================================================

def add_caregiver(name, contact):

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO caregivers
        (caregiver_name, caregiver_contact)
        VALUES (?, ?)
        """,
        (name, contact)
    )

    connection.commit()
    connection.close()


# ============================================================
# VIEW CAREGIVERS
# ============================================================

def view_caregivers():

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM caregivers
        """
    )

    caregivers = cursor.fetchall()

    connection.close()

    return caregivers