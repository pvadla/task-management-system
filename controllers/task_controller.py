from services.task_service import TaskService

class TaskController:
    def __init__(self, service: TaskService, view):
        self.service = service
        self.view = view  # Reference to the UI for triggering updates

    def add_task(self, title, description, due_date, priority, category):
        try:
            self.service.add_task(title, description, due_date, priority, category)
            self.view.refresh_tasks()  # Update UI
        except ValueError as e:
            self.view.show_error(str(e))

    def update_task(self, task_id, updated_data):
        try:
            self.service.update_task(task_id, updated_data)
            self.view.refresh_tasks()
        except ValueError as e:
            self.view.show_error(str(e))

    def delete_task(self, task_id):
        self.service.delete_task(task_id)
        self.view.refresh_tasks()

    def get_filtered_tasks(self, filters=None):
        return self.service.get_tasks(filter_by=filters)
