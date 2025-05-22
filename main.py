import tkinter as tk
from tkinter import ttk, messagebox
from controllers.task_controller import TaskController
from services.task_service import TaskService
from data.database import DatabaseManager

class TaskView:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("800x600")

        # Init service/controller
        self.db = DatabaseManager()
        self.service = TaskService(self.db)
        self.controller = TaskController(self.service, self)

        self.setup_ui()

    def setup_ui(self):
        self.create_menu()
        self.create_filters()
        self.create_task_list()
        self.create_status_bar()

        self.refresh_tasks()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Add Task", command=self.open_add_task_form)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def create_filters(self):
        filter_frame = ttk.Frame(self.root, padding=10)
        filter_frame.pack(fill=tk.X)

        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT)
        self.category_filter = ttk.Combobox(filter_frame, values=["All", "Work", "Personal"], state="readonly")
        self.category_filter.current(0)
        self.category_filter.pack(side=tk.LEFT, padx=5)

        ttk.Button(filter_frame, text="Refresh", command=self.refresh_tasks).pack(side=tk.RIGHT)

    def create_task_list(self):
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.task_frame = ttk.Frame(self.canvas)

        self.task_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def refresh_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        tasks = self.controller.get_filtered_tasks()
        for task in tasks:
            card = ttk.Frame(self.task_frame, padding=10, relief=tk.RIDGE)
            card.pack(fill=tk.X, padx=10, pady=5)

            ttk.Label(card, text=task.title, font=('Helvetica', 12, 'bold')).pack(anchor="w")
            ttk.Label(card, text=f"Due: {task.due_date.strftime('%Y-%m-%d')} | Priority: {task.priority}").pack(anchor="w")
            ttk.Label(card, text=task.description, wraplength=600).pack(anchor="w")

        self.status_var.set(f"{len(tasks)} task(s) loaded")

    def open_add_task_form(self):
        messagebox.showinfo("Add Task", "Form to be implemented...")

    def show_error(self, msg):
        messagebox.showerror("Error", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskView(root)
    root.mainloop()
