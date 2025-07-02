class User:
    def __init__(self, username):
        self.username = username

    def view_profile(self):
        with open("users.txt", "r") as file:
            for line in file:
                row = line.strip().split(",")
                if row[0] == self.username:
                    print("Profile:", row)

    def view_grades(self):
        with open("grades.txt", "r") as file:
            for line in file:
                row = line.strip().split(",")
                if row[0] == self.username:
                    print("Grades:", row[1:])

    def view_eca(self):
        with open("eca.txt", "r") as file:
            for line in file:
                row = line.strip().split(",")
                if row[0] == self.username:
                    print("ECA Activities:", row[1:])

class Admin(User):
    def add_user(self):
        username = input("Username: ")
        name = input("Name: ")
        age = input("Age: ")
        role = input("Role (Admin/Student): ")
        password = input("Password: ")

        with open("users.txt", "a") as ufile:
            ufile.write(f"{username},{name},{age},{role}\n")

        with open("passwords.txt", "a") as pfile:
            pfile.write(f"{username},{password}\n")

        print("User added!")

    def delete_user(self):
        username = input("Enter username to delete: ")

        for fname in ["users.txt", "passwords.txt", "grades.txt", "eca.txt"]:
            try:
                rows = []
                with open(fname, "r") as f:
                    for line in f:
                        row = line.strip().split(",")
                        if row and row[0] != username:
                            rows.append(line.strip())
                with open(fname, "w") as f:
                    for row in rows:
                        f.write(row + "\n")
            except FileNotFoundError:
                continue

        print("User deleted!")

    def view_average_grades(self):
        total = []
        count = 0
        try:
            with open("grades.txt", "r") as f:
                for line in f:
                    row = line.strip().split(",")
                    try:
                        grades = list(map(int, row[1:]))
                        if not total:
                            total = [0] * len(grades)
                        for i in range(len(grades)):
                            total[i] += grades[i]
                        count += 1
                    except:
                        continue
        except FileNotFoundError:
            print("grades.txt not found.")
            return

        if count:
            average = [round(t / count, 2) for t in total]
            print("Average Grades:", average)
        else:
            print("No grades found.")

    def add_grades(self):
        username = input("Student username: ")
        grades = input("Enter grades separated by commas (e.g. 90,80,85): ").split(",")

        updated = False
        rows = []
        try:
            with open("grades.txt", "r") as f:
                for line in f:
                    row = line.strip().split(",")
                    if row and row[0] == username:
                        rows.append(",".join([username] + grades))
                        updated = True
                    else:
                        rows.append(line.strip())
        except FileNotFoundError:
            pass

        if not updated:
            rows.append(",".join([username] + grades))

        with open("grades.txt", "w") as f:
            for row in rows:
                f.write(row + "\n")

        print("Grades saved.")

    def add_eca(self):
        username = input("Student username: ")
        activities = input("Enter activities separated by commas (e.g. Music,Sports): ").split(",")

        updated = False
        rows = []
        try:
            with open("eca.txt", "r") as f:
                for line in f:
                    row = line.strip().split(",")
                    if row and row[0] == username:
                        rows.append(",".join([username] + activities))
                        updated = True
                    else:
                        rows.append(line.strip())
        except FileNotFoundError:
            pass

        if not updated:
            rows.append(",".join([username] + activities))

        with open("eca.txt", "w") as f:
            for row in rows:
                f.write(row + "\n")

        print("ECA activities saved.")

class Student(User):
    def update_profile(self):
        new_name = input("New name: ")
        new_age = input("New age: ")
        rows = []

        with open("users.txt", "r") as f:
            for line in f:
                row = line.strip().split(",")
                if row[0] == self.username:
                    row[1], row[2] = new_name, new_age
                rows.append(",".join(row))

        with open("users.txt", "w") as f:
            for row in rows:
                f.write(row + "\n")

        print("Profile updated!")

def login():
    while True:
        username = input("Username: ")
        password = input("Password: ")

        try:
            with open("passwords.txt", "r") as f:
                for line in f:
                    row = line.strip().split(",")
                    if row == [username, password]:
                        with open("users.txt", "r") as ufile:
                            for urow in ufile:
                                user_row = urow.strip().split(",")
                                if user_row[0] == username:
                                    print("Login successful!")
                                    return username, user_row[3].lower()
        except FileNotFoundError:
            pass

        print("Login failed. Try again.")

def main():
    username, role = login()

    if role == "admin":
        admin = Admin(username)
        while True:
            print("\nAdmin Menu")
            print("1. Add User")
            print("2. Delete User")
            print("3. View Average Grades")
            print("4. Add Grades")
            print("5. Add ECA")
            print("6. Logout")
            choice = input("Choose: ")

            if choice == "1":
                admin.add_user()
            elif choice == "2":
                admin.delete_user()
            elif choice == "3":
                admin.view_average_grades()
            elif choice == "4":
                admin.add_grades()
            elif choice == "5":
                admin.add_eca()
            elif choice == "6":
                break

    elif role == "student":
        student = Student(username)
        while True:
            print("\nStudent Menu")
            print("1. View Profile")
            print("2. View Grades")
            print("3. View ECA")
            print("4. Update Profile")
            print("5. Logout")
            choice = input("Choose: ")

            if choice == "1":
                student.view_profile()
            elif choice == "2":
                student.view_grades()
            elif choice == "3":
                student.view_eca()
            elif choice == "4":
                student.update_profile()
            elif choice == "5":
                break

if __name__ == "__main__":
    main()
