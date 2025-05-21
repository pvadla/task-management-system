from datetime import datetime

class Task:
    def __init__(self, title, description, due_date, priority, category, status="Pending"):
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.priority = priority  # e.g., High, Medium, Low
        self.category = category  # e.g., Work, Personal
        self.status = status      # Pending or Completed

    def mark_complete(self):
        self.status = "Completed"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "category": self.category,
            "status": self.status
        }

    def __str__(self):
        return f"{self.title} ({self.priority}) - Due: {self.due_date.strftime('%Y-%m-%d')}"
