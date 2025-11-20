import os
import random
import datetime

USERS_FILE = "users.txt"
SCORES_FILE = "scores.txt"
QUESTIONS_FILE = {
    'DSA': "dsa_questions.txt",
    'DBMS': "dbms_questions.txt",
    'PYTHON': "python_questions.txt"
}
ADMIN = {'username': 'admin', 'password': 'admin123'}

# --- ADMIN DASHBOARD ---
def admin_dashboard():
    while True:
        print("\n--- ADMIN DASHBOARD ---")
        print("1. Add Question")
        print("2. View All Users")
        print("3. View All Scores")
        print("4. Logout")
        choice = input("Choose: ")
        
        if choice == "1":
            add_question()
        elif choice == "2":
            view_all_users()
        elif choice == "3":
            view_all_scores()
        elif choice == "4":
            print("Logging out admin...")
            break
        else:
            print("Invalid Choice!")

def add_question():
    category = input("Category (DSA/DBMS/PYTHON): ").upper()
    question = input("Question: ")
    options = [input(f"Option {i+1}: ") for i in range(4)]
    answer = input("Correct Option: ")
    filepath = QUESTIONS_FILE.get(category)
    if filepath:
        with open(filepath, "a") as f:
            f.write(f"{question}#{options[0]}#{options[1]}#{options[2]}#{options[3]}#{answer}\n")
        print("Question added successfully.")

def view_all_users():
    print("\n--- USERS LIST ---")
    with open(USERS_FILE, "r") as f:
        for line in f:
            data = line.strip().split(",")
            print(f"Enrollment: {data[0]}, Name: {data[5]}, Email: {data[1]}")

def view_all_scores():
    print("\n--- ALL SCORES ---")
    with open(SCORES_FILE, "r") as f:
        for line in f:
            print(line.strip())

# --- STUDENT DASHBOARD ---
def student_dashboard(user):
    while True:
        print("\n--- STUDENT DASHBOARD ---")
        print("1. Attempt Quiz")
        print("2. View Scores")
        print("3. Update Profile")
        print("4. View Profile")
        print("5. Logout")
        choice = input("Choose: ")
        if choice == '1':
            attempt_quiz(user)
        elif choice == '2':
            view_scores(user[0])
        elif choice == '3':
            update_profile(user)
        elif choice == '4':
            display_profile(user)
        elif choice == '5':
            break
        else:
            print("Invalid Choice")

def attempt_quiz(user):
    category = input("Category (DSA/DBMS/PYTHON): ").upper()
    if category in QUESTIONS_FILE:
        questions = []
        with open(QUESTIONS_FILE[category], "r") as f:
            for line in f:
                qdata = line.strip().split("#")
                questions.append(qdata)
        random.shuffle(questions)
        score = 0
        for i, q in enumerate(questions[:10]):
            print(f"Q{i+1}: {q[0]}")
            for idx in range(4):
                print(f"\t{idx+1}. {q[1+idx]}")
            ans = int(input("Answer (1/2/3/4): "))
            if q[1+ans-1] == q[5]:
                score += 1
        with open(SCORES_FILE, "a") as sfile:
            sfile.write(f"{user[0]},{category},{score}/{len(questions[:10])},{datetime.datetime.now()}\n")
        print(f"Your Score: {score}/{len(questions[:10])}")
    else:
        print("Invalid Category")

def view_scores(enrollment):
    print("\n--- YOUR SCORES ---")
    with open(SCORES_FILE, "r") as sf:
        for line in sf:
            data = line.strip().split(",")
            if data[0] == enrollment:
                print(f"{data[1]}: {data[2]}, {data[3]}")

def update_profile(user):
    print("Update Profile Fields (press enter to skip):")
    fields = ['email', 'branch', 'year', 'contact', 'name']
    new_data = user[:]
    for i, field in enumerate(fields, start=1):
        val = input(f"New {field} ({user[i]}): ")
        if val:
            new_data[i] = val
    users = []
    with open(USERS_FILE, "r") as f:
        for line in f:
            data = line.strip().split(",")
            if data[0] == user[0]:
                users.append(",".join(new_data) + "\n")
            else:
                users.append(line)
    with open(USERS_FILE, "w") as f:
        f.writelines(users)
    print("Profile Updated!")

def display_profile(user):
    print(f"Enrollment: {user[0]}\nEmail: {user[1]}\nBranch: {user[2]}\nYear: {user[3]}\nContact: {user[4]}\nName: {user[5]}")

# --- REGISTRATION/LOGIN ---
def register():
    enrollment = input("Enrollment Number: ")
    email = input("Email: ")
    branch = input("Branch: ")
    year = input("Year: ")
    contact = input("Contact: ")
    name = input("Name: ")
    password = input("Set Password: ")
    with open(USERS_FILE, "a") as f:
        f.write(f"{enrollment},{email},{branch},{year},{contact},{name},{password}\n")
    print("Registration successful!")

def login():
    print("1. User Login\n2. Admin Login")
    ch = input("Choose: ")
    if ch == '1':
        enrollment = input("Enrollment Number: ")
        password = input("Password: ")
        with open(USERS_FILE, "r") as f:
            for line in f:
                user = line.strip().split(",")
                if user[0] == enrollment and user[6] == password:
                    print("Login Success!")
                    return user
        print("Invalid credentials!")
        return None
    elif ch == '2':
        username = input("Admin Username: ")
        password = input("Admin Password: ")
        if username == ADMIN['username'] and password == ADMIN['password']:
            print("Admin Login Success!")
            return 'admin'
        else:
            print("Invalid Admin Credentials!")
            return None
    else:
        print("Invalid Choice!")
        return None

# --- MAIN APPLICATION LOOP ---
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")
        if choice == '1':
            register()
        elif choice == '2':
            res = login()
            if res == 'admin':
                admin_dashboard()
            elif res:
                student_dashboard(res)
        elif choice == '3':
            print("Exiting!")
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()
