import sqlite3


# ============================================================
# REGISTER USER
# ============================================================

def register_user(username, password):

    connection = sqlite3.connect("health.db")

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


# ============================================================
# LOGIN USER
# ============================================================

def login_user(username, password):

    connection = sqlite3.connect("health.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# ============================================================
# RESET PASSWORD
# ============================================================

def reset_password(username, new_password):

    connection = sqlite3.connect("health.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (new_password, username)
    )

    connection.commit()

    success = cursor.rowcount > 0

    connection.close()

    return success