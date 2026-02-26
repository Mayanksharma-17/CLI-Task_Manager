import os
import hashlib

# ====== CONFIG ======
USER_FILE = "users.txt"
DATA_FOLDER = "data"

# Create data folder if not exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


# ====== MAIN MENU ======
def main():
    while True:
        print("\n===== TASK MANAGER =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice!")


# ====== PASSWORD HASHING ======
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ====== CHECK IF USER EXISTS ======
def user_exists(username):
    if not os.path.exists(USER_FILE):
        return False

    with open(USER_FILE, "r") as f:
        return any(line.startswith(f"{username} :") for line in f)


# ====== REGISTER ======
def register():
    username = input("Enter Username: ")

    if user_exists(username):
        print("Username already exists!")
        return

    password = input("Enter Password: ")

    with open(USER_FILE, "a") as f:
        f.write(f"{username} : {hash_password(password)}\n")

    print("Registration successful!")


# ====== LOGIN ======
def login():
    if not os.path.exists(USER_FILE):
        print("No users registered yet.")
        return

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    hashed = hash_password(password)

    with open(USER_FILE, "r") as f:
        for line in f:
            if line.strip() == f"{username} : {hashed}":
                print("Login successful!")
                user_dashboard(username)
                return

    print("Login failed!")


# ====== USER DASHBOARD ======
def user_dashboard(username):
    while True:
        print(f"\n===== Welcome {username} =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Logout")

        choice = input("Choose: ")

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            delete_task(username)
        elif choice == "4":
            print("Logged out.")
            break
        else:
            print("Invalid option!")


# ====== ADD TASK ======
def add_task(username):
    task = input("Enter Task: ")

    filepath = os.path.join(DATA_FOLDER, f"{username}.txt")

    with open(filepath, "a") as f:
        f.write(task + "\n")

    print("Task added successfully!")


# ====== VIEW TASKS ======
def view_tasks(username):
    filepath = os.path.join(DATA_FOLDER, f"{username}.txt")

    if not os.path.exists(filepath):
        print("No tasks yet.")
        return

    with open(filepath, "r") as f:
        tasks = f.readlines()

    if not tasks:
        print("No tasks yet.")
        return

    print("\nYour Tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.strip()}")


# ====== DELETE TASK ======
def delete_task(username):
    filepath = os.path.join(DATA_FOLDER, f"{username}.txt")

    if not os.path.exists(filepath):
        print("No tasks to delete.")
        return

    with open(filepath, "r") as f:
        tasks = f.readlines()

    if not tasks:
        print("No tasks to delete.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.strip()}")

    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            tasks.pop(num - 1)

            with open(filepath, "w") as f:
                f.writelines(tasks)

            print("Task deleted successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


# ====== RUN PROGRAM ======
if __name__ == "__main__":
    main()