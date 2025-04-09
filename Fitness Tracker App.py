#  Importing sqlite3 to create and manage the database
import sqlite3
#  Importing the datetime module to work with dates and times
from datetime import datetime

#  I will create a connection to the database.
#  I will create a cursore object to execute SQL commands.
def initialize_db():
    #  Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #  Create a table exercise category if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    #  Create a table for exercises if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            sets INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES exercise_category (id)
        )
    ''')

    #  Create a table for workout_routine if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_routine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            routine_name TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    #  Create a table routine_exercises if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routine_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            routine_id INTEGER NOT NULL,
            exercise_id INTEGER NOT NULL,
            FOREIGN KEY (routine_id) REFERENCES workout_routine (id),
            FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        )
    ''')

    #  Create a table for fitness goals if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fitness_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            progress INTEGER NOT NULL
        )
    ''')

    #  Create table for progress_logs if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            weight REAL NOT NULL,
            body_fat REAL NOT NULL,
            muscle_mass REAL NOT NULL,
            notes TEXT
        )
    ''')

    #  Commit the changes and close the connection
    conn.commit()
    conn.close()

#  Function to add a new exercise category
def add_exercise_category(name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exercise_category (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

#  Function to add a new exercise
def add_exercise(exercise_name, category_id, reps, sets, duration):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exercises (exercise_name, category_id, reps, sets, duration) VALUES (?, ?, ?, ?, ?)",
                   (exercise_name, category_id, reps, sets, duration))
    conn.commit()
    conn.close()

#  Function to add a new workout routine
def add_workout_routine(routine_name, date):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workout_routine (routine_name, date) VALUES (?, ?)",
                   (routine_name, date))
    conn.commit()
    conn.close()

#  Function to add exercises to a workout routine
def add_exercise_to_routine(routine_id, exercise_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO routine_exercises (routine_id, exercise_id) VALUES (?, ?)",
                   (routine_id, exercise_id))
    conn.commit()
    conn.close()

#  Function to add a fitness goal
def add_fitness_goal(goal, start_date, end_date, progress):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fitness_goals (goal, start_date, end_date, progress) VALUES (?, ?, ?, ?)",
                   (goal, start_date, end_date, progress))
    conn.commit()
    conn.close()

#  Function to add a progress log
def add_progress_log(date, weight, body_fat, muscle_mass, notes):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO progress_logs (date, weight, body_fat, muscle_mass, notes) VALUES (?, ?, ?, ?, ?)",
                   (date, weight, body_fat, muscle_mass, notes))
    conn.commit()
    conn.close()

#  Function to view all exercise categories
def view_exercise_categories():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercise_category")
    categories = cursor.fetchall()
    conn.close()
    return categories

#  Function to view all exercises
def view_exercises():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises")
    exercises = cursor.fetchall()
    conn.close()
    return exercises

#  Function to view all workout routines
def view_workout_routines():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workout_routine")
    routines = cursor.fetchall()
    conn.close()
    return routines

#  Function to view all fitness goals

def view_fitness_goals():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fitness_goals")
    goals = cursor.fetchall()
    conn.close()
    return goals

#  Function to view all progress logs
def view_progress_logs():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progress_logs")
    logs = cursor.fetchall()
    conn.close()
    return logs

#  Function to view exercises in a specific workout routine
def view_exercises_in_routine(routine_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.* FROM exercises e
        JOIN routine_exercises re ON e.id = re.exercise_id
        WHERE re.routine_id = ?
    ''', (routine_id,))
    exercises = cursor.fetchall()
    conn.close()
    return exercises

#  Function to view exercises in a specific category
def view_exercises_in_category_id(category_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises WHERE category_id = ?", (category_id,))
    exercises = cursor.fetchall()
    conn.close()
    return exercises

#  Function to view all exercises in a specific category
def view_exercises_in_category(category_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.* FROM exercises e
        JOIN exercise_category ec ON e.category_id = ec.id
        WHERE ec.name = ?
    ''', (category_name,))
    exercises = cursor.fetchall()
    conn.close()
    return exercises

#  Function to view all exercises in a specific workout routine
def view_exercises_in_routine_name(routine_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.* FROM exercises e
        JOIN routine_exercises re ON e.id = re.exercise_id
        JOIN workout_routine wr ON re.routine_id = wr.id
        WHERE wr.routine_name = ?
    ''', (routine_name,))
    exercises = cursor.fetchall()
    conn.close()
    return exercises

#  Function to view all exercises in a specific workout routine
def view_exercises_in_routine_id(routine_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.* FROM exercises e
        JOIN routine_exercises re ON e.id = re.exercise_id
        WHERE re.routine_id = ?
    ''', (routine_id,))
    exercises = cursor.fetchall()
    conn.close()
    return exercises

#  Add a new exercise category
def add_new_exercise_category():
    name = input("Enter the name of the exercise category: ")
    add_exercise_category(name)
    print(f"Exercise category '{name}' added successfully.")

#  Add a new exercise
def add_new_exercise():
    exercise_name = input("Enter the name of the exercise: ")
    category_id = int(input("Enter the category ID: "))
    reps = int(input("Enter the number of reps: "))
    sets = int(input("Enter the number of sets: "))
    duration = int(input("Enter the duration in seconds: "))
    add_exercise(exercise_name, category_id, reps, sets, duration)
    print(f"Exercise '{exercise_name}' added successfully.")

#  Add a new workout routine
def add_new_workout_routine():
    routine_name = input("Enter the name of the workout routine: ")
    date = input("Enter the date (YYYY-MM-DD): ")
    add_workout_routine(routine_name, date)
    print(f"Workout routine '{routine_name}' added successfully.")

#  Add exercises to a workout routine
def add_exercise_to_workout_routine():
    routine_id = int(input("Enter the routine ID: "))
    exercise_id = int(input("Enter the exercise ID: "))
    add_exercise_to_routine(routine_id, exercise_id)
    print(f"Exercise with ID '{exercise_id}' added to routine with ID '{routine_id}' successfully.")

#  Add a fitness goal
def add_new_fitness_goal():
    goal = input("Enter the fitness goal: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    progress = int(input("Enter the progress (0-100): "))
    add_fitness_goal(goal, start_date, end_date, progress)
    print(f"Fitness goal '{goal}' added successfully.")

#  Add a progress log
def add_new_progress_log():
    date = input("Enter the date (YYYY-MM-DD): ")
    weight = float(input("Enter your weight: "))
    body_fat = float(input("Enter your body fat percentage: "))
    muscle_mass = float(input("Enter your muscle mass: "))
    notes = input("Enter any notes: ")
    add_progress_log(date, weight, body_fat, muscle_mass, notes)
    print(f"Progress log for '{date}' added successfully.")

#  View all exercise categories
def view_all_exercise_categories():
    categories = view_exercise_categories()
    print("Exercise Categories:")
    for category in categories:
        print(f"ID: {category[0]}, Name: {category[1]}")

#  View all exercises
def view_all_exercises():
    exercises = view_exercises()
    print("Exercises:")
    for exercise in exercises:
        print(f"ID: {exercise[0]}, Name: {exercise[1]}, Category ID: {exercise[2]}, Reps: {exercise[3]}, Sets: {exercise[4]}, Duration: {exercise[5]} seconds")

#  View exercises in a specific category
def view_exercises_in_category():
    category_name = input("Enter the name of the exercise category: ")
    exercises = view_exercises_in_category(category_name)
    print(f"Exercises in category '{category_name}':")
    for exercise in exercises:
        print(f"ID: {exercise[0]}, Name: {exercise[1]}, Category ID: {exercise[2]}, Reps: {exercise[3]}, Sets: {exercise[4]}, Duration: {exercise[5]} seconds")

#  View exercises in a specific workout routine
def view_exercises_in_routine():
    routine_name = input("Enter the name of the workout routine: ")
    exercises = view_exercises_in_routine_name(routine_name)
    print(f"Exercises in routine '{routine_name}':")
    for exercise in exercises:
        print(f"ID: {exercise[0]}, Name: {exercise[1]}, Category ID: {exercise[2]}, Reps: {exercise[3]}, Sets: {exercise[4]}, Duration: {exercise[5]} seconds")

#  View all workout routines
def view_all_workout_routines():
    routines = view_workout_routines()
    print("Workout Routines:")
    for routine in routines:
        print(f"ID: {routine[0]}, Name: {routine[1]}, Date: {routine[2]}")

#  View all fitness goals
def view_all_fitness_goals():
    goals = view_fitness_goals()
    print("Fitness Goals:")
    for goal in goals:
        print(f"ID: {goal[0]}, Goal: {goal[1]}, Start Date: {goal[2]}, End Date: {goal[3]}, Progress: {goal[4]}%")

#  View all progress logs
def view_all_progress_logs():
    logs = view_progress_logs()
    print("Progress Logs:")
    for log in logs:
        print(f"ID: {log[0]}, Date: {log[1]}, Weight: {log[2]}, Body Fat: {log[3]}%, Muscle Mass: {log[4]}%, Notes: {log[5]}")

#  Call the initialize_db function to create the database and tables
initialize_db()

#  Main menu loop
while True:
        print("\nFitness Tracker App")
        print("1. Add Exercise Category")
        print("2. Add Exercise")
        print("3. Add Workout Routine")
        print("4. Add Exercise to Workout Routine")
        print("5. Add Fitness Goal")
        print("6. Add Progress Log")
        print("7. View Exercise Categories")
        print("8. View Exercises")
        print("9. View Workout Routines")
        print("10. View Fitness Goals")
        print("11. View Progress Logs")
        print("12. View Exercises in Category")
        print("13. View Exercises in Routine")
        print("14. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_new_exercise_category()
        elif choice == "2":
            add_new_exercise()
        elif choice == "3":
            add_new_workout_routine()
        elif choice == "4":
            add_exercise_to_workout_routine()
        elif choice == "5":
            add_new_fitness_goal()
        elif choice == "6":
            add_new_progress_log()
        elif choice == "7":
            view_all_exercise_categories()
        elif choice == "8":
            view_all_exercises()
        elif choice == "9":
            view_all_workout_routines()
        elif choice == "10":
            view_all_fitness_goals()
        elif choice == "11":
            view_all_progress_logs()
        elif choice == "12":
            view_exercises_in_category()
        elif choice == "13":
            view_exercises_in_routine()
        elif choice == "14":
            break
        else:
            print("Invalid choice. Please try again.")

print("Goodbye!")
