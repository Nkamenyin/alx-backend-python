import sqlite3
import functools


def with_db_connection(func):
    """Decorator to automatically open and close the DB connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def transactional(func):
    """Decorator to handle transactions (commit/rollback)"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # run the SQL logic
            conn.commit()  # commit if no error
            return result
        except Exception as e:
            conn.rollback()  # rollback if error
            raise e
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)
    )


# Update user's email with automatic connection + transaction handling
update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
print("Email updated successfully")
