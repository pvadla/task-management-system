import sqlite3
from models.task import Task

class DatabaseManager:
    def __init__(self, db_name="tasks.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT,
                            due_date TEXT,
                            priority TEXT,
                            category TEXT,
                            status TEXT)''')
        self.connection.commit()

    def create_task(self, task: Task):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO tasks (title, description, due_date, priority, category, status)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (task.title, task.description, task.due_date.strftime("%Y-%m-%d"),
                        task.priority, task.category, task.status))
        self.connection.commit()

    def get_all_tasks(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            task = Task(*row[1:-1], status=row[-1])  # excluding ID
            tasks.append(task)
        return tasks

    def update_task(self, task_id, updated_task: Task):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE tasks SET title=?, description=?, due_date=?, 
                          priority=?, category=?, status=? WHERE id=?''',
                       (updated_task.title, updated_task.description, updated_task.due_date.strftime("%Y-%m-%d"),
                        updated_task.priority, updated_task.category, updated_task.status, task_id))
        self.connection.commit()

    def delete_task(self, task_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.connection.commit()
