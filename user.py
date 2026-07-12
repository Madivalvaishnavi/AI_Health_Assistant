import sqlite3

# Register a new user
def register_user(username, password):

    # Check if fields are empty
    if not username.strip() or not password.strip():
        return "empty"

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        connection.commit()
        return "success"

    except sqlite3.IntegrityError:
        return "exists"

    finally:
        connection.close()


# Login existing user
def login_user(username, password):

    connection = sqlite3.connect("health.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user