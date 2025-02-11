import os
import time
import threading

TASKS_FILE = "tasks.txt"
CATEGORIES_FILE = "categories.txt"


def load_tasks():
    """Load tasks and categories from a file."""
    tasks = {}
    if not os.path.exists(TASKS_FILE):
        return tasks  # Return empty dictionary if file doesn't exist

    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.strip()
            if " = " in line:
                task, category = line.split(" = ")
                if category not in tasks:
                    tasks[category] = []  # ✅ Ensure category exists even if empty
                tasks[category].append(task)
    return tasks


def save_tasks(tasks):
    """Save tasks to a file with categories."""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        for category, task_list in tasks.items():
            for task in task_list:
                file.write(f"{task} = {category}\n")

def add_task(task, category="General"):
    """Add a new task under a category (create category if it doesn’t exist)."""
    tasks = load_tasks()
    categories = load_categories()

    if category not in categories:
        print(f"⚠️ Category '{category}' does not exist. Creating it now...")
        create_category(category)

    if category not in tasks:
        tasks[category] = []

    tasks[category].append(f"[ ] {task}")  # Store as unchecked task
    save_tasks(tasks)
    print(f"✅ Task added under {category}: {task}")



def create_study_schedule(tasks):
    """Generate a simple study schedule based on available tasks."""
    print("\n📅 Your Study Schedule for Today:")
    for i, (category, task_list) in enumerate(tasks.items(), 1):
        print(f"\n📌 {category}:")
        for task in task_list:
            print(f"   - {task}")

def view_tasks():
    """Display tasks grouped by categories."""
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return

    print("\n📋 Task List:")
    for category, task_list in tasks.items():
        print(f"\n📌 {category}:")
        for i, task in enumerate(task_list, 1):
            print(f"   {i}. {task}")

def complete_task(task_number, category):
    """Mark a task as completed within a category."""
    tasks = load_tasks()
    if category not in tasks or task_number < 1 or task_number > len(tasks[category]):
        print("❌ Invalid task number or category.")
        return

    tasks[category][task_number - 1] = tasks[category][task_number - 1].replace("[ ]", "[✔]")  # Mark as completed
    save_tasks(tasks)
    print(f"✅ Task {task_number} in {category} marked as completed!")


def delete_task(task_number, category):
    """Delete a task from a specific category."""
    tasks = load_tasks()

    if category not in tasks or task_number < 1 or task_number > len(tasks[category]):
        print("❌ Invalid task number or category.")
        return

    removed_task = tasks[category].pop(task_number - 1)  # Remove task
    if not tasks[category]:  # If category is now empty, remove it
        del tasks[category]

    save_tasks(tasks)
    print(f"🗑️ Deleted task: {removed_task}")


def load_categories():
    """Load existing categories from the file."""
    if not os.path.exists(CATEGORIES_FILE):
        return ["General"]  # Default category

    with open(CATEGORIES_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def save_categories(categories):
    """Save category list to the file."""
    with open(CATEGORIES_FILE, "w", encoding="utf-8") as file:
        file.writelines([category + "\n" for category in categories])

def create_category(category_name):
    """Create a new category and save it."""
    categories = load_categories()
    if category_name not in categories:
        categories.append(category_name)
        save_categories(categories)
        print(f"✅ Category '{category_name}' created!")
    else:
        print("⚠️ Category already exists!")

def view_categories():
    """Display all available categories."""
    categories = load_categories()
    print("\n📂 Available Categories:")
    for category in categories:
        print(f" - {category}")

import time
import threading

stop_timer = False  # Global flag to stop the timer

def pomodoro_timer(work_time=25, break_time=5):
    """Run a Pomodoro timer that stops when ENTER is pressed."""
    global stop_timer  # Allow modification of the global flag
    stop_timer = False  # Reset stop flag for each session

    def wait_for_input():
        """Wait for user input in a separate thread to stop the timer."""
        input("\n⏳ Pomodoro started! Press ENTER to stop early...\n")
        global stop_timer
        stop_timer = True  # Set stop flag to True when ENTER is pressed

    # Start user input listener in a separate thread
    input_thread = threading.Thread(target=wait_for_input, daemon=True)
    input_thread.start()

    # Work session countdown
    for remaining in range(work_time * 60, 0, -1):
        if stop_timer:
            print("\n🛑 Pomodoro Timer Stopped Early!\n")
            return  # Exit the function immediately
        print(f"🕒 {remaining // 60}:{remaining % 60:02d} remaining...", end="\r")
        time.sleep(1)

    print("\n🚀 Time for a break!")

    # Break session countdown
    for remaining in range(break_time * 60, 0, -1):
        if stop_timer:
            print("\n🛑 Pomodoro Timer Stopped Early!\n")
            return  # Exit the function immediately
        print(f"☕ {remaining // 60}:{remaining % 60:02d} remaining...", end="\r")
        time.sleep(1)

    print("\n🎉 Break over! Ready for another session?")


def main():
    while True:
        print("\n🔹 Zenith Task Manager 🔹")
        print("1️⃣ Add Task")
        print("2️⃣ View Tasks")
        print("3️⃣ Complete Task")
        print("4️⃣ Delete Task")
        print("5️⃣ Create Category")  
        print("6️⃣ View Categories")  
        print("7️⃣ Start Pomodoro Timer")
        print("8️⃣ Exit")

        choice = input("Select an option (1-8): ")

        if choice == "1":
            task = input("Enter task description: ")
            category = input("Enter task category (or press Enter for 'General'): ") or "General"
            add_task(task, category)

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            view_tasks()
            category = input("Enter the category of the task: ")
            task_number = int(input("Enter task number to complete: "))
            complete_task(task_number, category)

        elif choice == "4":
            view_tasks()
            category = input("Enter the category of the task: ")  # ✅ Now asks for category
            task_number = int(input("Enter task number to delete: "))
            delete_task(task_number, category)  # ✅ Correctly passes both arguments


        elif choice == "5":
            category_name = input("Enter new category name: ")
            create_category(category_name)

        elif choice == "6":
            view_categories()

        elif choice == "7":
            work_time = input("Enter focus time in minutes (default 25): ") or "25"
            break_time = input("Enter break time in minutes (default 5): ") or "5"
            pomodoro_timer(int(work_time), int(break_time))

        elif choice == "8":
            print("👋 Exiting Zenith Task. Stay productive!")
            break

        else:
            print("❌ Invalid choice. Please select 1-7.")



if __name__ == "__main__":
    main()


