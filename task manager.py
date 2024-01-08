import json
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Task list
        self.tasks = []

        # Entry for task input
        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        # Buttons
        add_button = tk.Button(root, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=1, padx=5)

        complete_button = tk.Button(root, text="Complete Task", command=self.complete_task)
        complete_button.grid(row=1, column=0, pady=5)

        delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        delete_button.grid(row=1, column=1, pady=5)

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=40)
        self.task_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Menu Bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Tasks", command=self.save_tasks)
        file_menu.add_command(label="Load Tasks", command=self.load_tasks)

        # Populate the listbox with existing tasks
        self.update_task_listbox()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            priority = simpledialog.askstring("Priority", "Enter task priority (Low/Medium/High):").capitalize()
            due_date = simpledialog.askstring("Due Date", "Enter task due date (YYYY-MM-DD):")
            
            task = {"text": task_text, "priority": priority, "due_date": due_date, "completed": False}
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index]["completed"] = True
            self.update_task_listbox()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[Completed]" if task["completed"] else ""
            self.task_listbox.insert(tk.END, f"{status} {task['text']} (Priority: {task['priority']}, Due Date: {task['due_date']})")

    def save_tasks(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.tasks, file)
            messagebox.showinfo("Save Successful", "Tasks saved successfully.")

    def load_tasks(self):
        file_path = tk.filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                self.tasks = json.load(file)
            self.update_task_listbox()
            messagebox.showinfo("Load Successful", "Tasks loaded successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
