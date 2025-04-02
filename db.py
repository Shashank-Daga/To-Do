import sqlite3


def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        task TEXT NOT NULL,
                        due_time TEXT)''')
    conn.commit()
    conn.close()


def add_task(task, due_time):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, due_time) VALUES (?, ?)", (task, due_time))
    conn.commit()
    conn.close()


def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(old_task, new_task):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task = ? WHERE task = ?", (new_task, old_task))
    conn.commit()
    conn.close()


def delete_task(task):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
    conn.commit()
    conn.close()


# Run this script once to create the database
if __name__ == "__main__":
    init_db()
