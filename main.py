import json
import os
from datetime import datetime


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    return json.load(file)
            except:
                return []
        return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        title = input("Enter Task Title: ").strip()
        priority = input("Priority (High/Medium/Low): ").capitalize()
        due_date = input("Due Date (YYYY-MM-DD): ")

        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "priority": priority,
            "due_date": due_date,
            "status": "Pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.tasks.append(task)
        self.save_tasks()
        print("✅ Task Added Successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No Tasks Available.")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<5}{'Task':<25}{'Priority':<10}{'Status':<12}{'Due Date'}")
        print("=" * 70)

        for task in self.tasks:
            print(
                f"{task['id']:<5}"
                f"{task['title']:<25}"
                f"{task['priority']:<10}"
                f"{task['status']:<12}"
                f"{task['due_date']}"
            )

    def complete_task(self):
        task_id = int(input("Enter Task ID to Complete: "))

        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "Completed"
                self.save_tasks()
                print("🎉 Task Completed!")
                return

        print("Task Not Found.")

    def delete_task(self):
        task_id = int(input("Enter Task ID to Delete: "))

        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print("🗑️ Task Deleted Successfully!")
                return

        print("Task Not Found.")

    def dashboard(self):
        total = len(self.tasks)
        completed = len(
            [task for task in self.tasks if task["status"] == "Completed"]
        )
        pending = total - completed

        print("\n📊 TASK DASHBOARD")
        print("-" * 25)
        print(f"Total Tasks     : {total}")
        print(f"Completed Tasks : {completed}")
        print(f"Pending Tasks   : {pending}")

    def run(self):
        while True:
            print("\n===== SMART TO-DO MANAGER =====")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Complete Task")
            print("4. Delete Task")
            print("5. Dashboard")
            print("6. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_task()

            elif choice == "2":
                self.view_tasks()

            elif choice == "3":
                self.complete_task()

            elif choice == "4":
                self.delete_task()

            elif choice == "5":
                self.dashboard()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid Choice. Try Again.")


if __name__ == "__main__":
    app = TaskManager()
    app.run()