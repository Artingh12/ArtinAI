import sqlite3


DATABASE_NAME = "database/artin.db"


def connect():
    return sqlite3.connect(DATABASE_NAME)


def create_database():

    connection = connect()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            memory TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_message(user_id, role, content):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (user_id, role, content)
        VALUES (?, ?, ?)
        """,
        (user_id, role, content)
    )

    connection.commit()
    connection.close()


def get_messages(user_id):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (user_id,)
    )

    messages = cursor.fetchall()

    connection.close()

    return messages


def save_memory(user_id, memory):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories (user_id, memory)
        VALUES (?, ?)
        """,
        (user_id, memory)
    )

    connection.commit()
    connection.close()


def get_memories(user_id):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, memory
        FROM memories
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (user_id,)
    )

    memories = cursor.fetchall()

    connection.close()

    return memories
def update_memory(memory_id, new_memory):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE memories
        SET memory = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (new_memory, memory_id)
    )

    connection.commit()
    connection.close()
def delete_memory(memory_id):

    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM memories
        WHERE id = ?
        """,
        (memory_id,)
    )

    connection.commit()

    connection.close()