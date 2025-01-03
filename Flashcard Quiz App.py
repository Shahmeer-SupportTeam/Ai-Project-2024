import tkinter as tk
from tkinter import ttk
import mysql.connector
import random
import time

# Database connection setup
def connect_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="umar0075@",  # Change this to your MySQL root password
            database="flashcard_quiz_app"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Tkinter GUI
class FlashcardQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz App")
        self.root.geometry("800x600")
        self.root.configure(bg="#2D2D2D")  # Dark background for modern theme

        # Define custom styles
        style = ttk.Style()
        style.configure("Main.TFrame", background="#2D2D2D")
        style.configure("TLabel", background="#2D2D2D", foreground="white", font=("Arial", 14))
        style.configure("Oval.TButton", font=("Arial", 14), padding=10, relief="flat", background="lime", foreground="black")
        style.map("Oval.TButton", background=[('active', 'lightblue')], relief=[('pressed', 'sunken')])

        # Initialize variables
        self.current_user_id = None
        self.current_user_role = None
        self.score = 0
        self.timer = 60  # Total quiz time
        self.question_timer = 60  # Per-question time
        self.running = False  # Timer running state
        self.question_running = False  # Question running state
        self.start_time = None
        self.skipped_flashcards = []
        self.load_flashcards()
        self.login_screen()

    # Load flashcards from the database
    def load_flashcards(self):
        conn = connect_database()
        if conn is None:
            print("Failed to connect to the database.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flashcards")
        self.flashcards = cursor.fetchall()
        self.total_questions = len(self.flashcards)
        conn.close()

    # Clear the current screen
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Display the login screen
    def login_screen(self):
        self.clear_screen()
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Welcome To Flash Card Quiz", foreground="lime", font=("Arial", 20, "bold", "underline")).pack(pady=20)
        ttk.Label(main_frame, text="Username").pack(pady=5)
        self.username_entry = ttk.Entry(main_frame, font=("Arial", 14), width=20)
        self.username_entry.pack(pady=5)
        ttk.Label(main_frame, text="Password").pack(pady=5)
        self.password_entry = ttk.Entry(main_frame, font=("Arial", 14), show="*", width=20)
        self.password_entry.pack(pady=5)
        ttk.Button(main_frame, text="Login", style="Oval.TButton", command=self.login).pack(pady=20)
        ttk.Button(main_frame, text="Register as User", style="Oval.TButton", command=self.register_screen).pack(pady=5)
        self.login_error_label = ttk.Label(main_frame, text="", foreground="red")
        self.login_error_label.pack(pady=5)

    # Display the registration screen
    def register_screen(self):
        self.clear_screen()
        main_frame = ttk.Frame(self.root, style="Main .TFrame")
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text=" Register", font=("Arial", 24, "bold")).pack(pady=20)
        ttk.Label(main_frame, text="Username").pack(pady=5)
        self.reg_username_entry = ttk.Entry(main_frame, font=("Arial", 14), width=20)
        self.reg_username_entry.pack(pady=5)
        ttk.Label(main_frame, text="Password").pack(pady=5)
        self.reg_password_entry = ttk.Entry(main_frame, font=("Arial", 14), show="*", width=20)
        self.reg_password_entry.pack(pady=5)
        ttk.Button(main_frame, text="Register", style="Oval.TButton", command=self.register).pack(pady=20)
        ttk.Button(main_frame, text="Back", style="Oval.TButton", command=self.login_screen).pack(pady=5)
        self.reg_error_label = ttk.Label(main_frame, text="", foreground="red")
        self.reg_error_label.pack(pady=5)

    # Register a new user
    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if username and password:
            try:
                conn = connect_database()
                if conn is None:
                    self.reg_error_label.config(text="Failed to connect to the database")
                    return

                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, 'user'))
                conn.commit()
                conn.close()
                self.registration_success()
            except mysql.connector.IntegrityError:
                self.reg_error_label.config(text="Username already exists")
        else:
            self.reg_error_label.config(text="Please fill in all fields")

    # Show registration success screen
    def registration_success(self):
        self.clear_screen()
        ttk.Label(self.root, text="Successfully Registered", font=("Arial", 18), foreground="green").pack(pady=20)
        ttk.Button(self.root, text="Login", style="Oval.TButton", command=self.login_screen).pack(pady=10)

    # Login the user
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_database()
        if conn is None:
            self.login_error_label.config(text="Failed to connect to the database")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.current_user_id = user[0]
            self.current_user_role = user[3]
            self.dashboard()
        else:
            self.login_error_label.config(text="Invalid username or password")

    # Display the dashboard
    def dashboard(self):
        self.clear_screen()
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Dashboard", font=("Arial", 24, "bold")).pack(pady=20)

        if self.current_user_role == 'admin':
            ttk.Button(main_frame, text="View All Marks", style="Oval.TButton", command=self.view_all_marks).pack(pady=10)
            ttk.Button(main_frame, text="Modify Quizzes", style="Oval.TButton", command=self.modify_quizzes).pack(pady=10)

        ttk.Button(main_frame, text="Take Quiz", style="Oval.TButton", command=self.start_quiz).pack(pady=10)
        ttk.Button(main_frame, text="View My Marks", style="Oval.TButton", command=self.view_my_marks).pack(pady=10)
        ttk.Button(main_frame, text="Logout", style="Oval.TButton", command=self.login_screen).pack(pady=10)

    # Start the quiz
    def start_quiz(self):
        self.score = 0
        self.skipped_flashcards = []
        self.load_flashcards()
        random.shuffle(self.flashcards)
        self.start_time = time.time()
        self.running = True
        self.question_running = True
        self.questions_attempted = 0
        self.total_questions = 10 
        self.next_question()
        self.update_timer()

    # Update the timer
    def update_timer(self):
        if self.running:
            if self.timer > 0:
                mins, secs = divmod(self.timer, 60)
                quiz_time_format = '{:02d}:{:02d}'.format(mins, secs)
                self.timer_label.config(text=f"Total Time Left: {quiz_time_format}")
                self.timer -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.running = False
                self.show_score()

        if self.question_running:
            if self.question_timer > 0:
                mins, secs = divmod(self.question_timer, 60)
                question_time_format = '{:02d}:{:02d}'.format(mins, secs)
                self.question_timer_label.config(text=f"Question Time Left: {question_time_format}")
                self.question_timer -= 1
            else:
                self.question_running = False
                self.skip_question()  # Skip the question if time runs out
        self.root.after(1000, self.update_timer)

    # Load the next question
    def next_question(self):
        if self.questions_attempted < self.total_questions and self.flashcards:
            self.current_question = self.flashcards.pop(0)
            self.questions_attempted += 1
            self.question_timer = 60  # Reset the per-question timer
            self.question_running = True
            self.display_question()
        else:
            self.show_score()  # End the quiz after 10 questions

    # Display the current question
    def display_question(self):
        self.clear_screen()
        ttk.Label(self.root, text=self.current_question[1], font=("Arial", 16)).pack(pady=10)

        options = [self.current_question[2], self.current_question[3], self.current_question[4], self.current_question[5]]
        random.shuffle(options)

        self.correct_option = self.current_question[6]

        # Create frames for options
        options_frame_line1 = ttk.Frame(self.root)
        options_frame_line1.pack(pady=10)

        options_frame_line2 = ttk.Frame(self.root)
        options_frame_line2.pack(pady=10)

        # Display options in two lines
        ttk.Button(options_frame_line1, text=options[0], style="Oval.TButton", command=lambda opt=options[0]: self.check_answer(opt)).pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame_line1, text=options[1], style="Oval.TButton", command=lambda opt=options[1]: self.check_answer(opt)).pack(side=tk.LEFT, padx=5)

        ttk.Button(options_frame_line2, text=options[2], style="Oval.TButton", command=lambda opt=options[2]: self.check_answer(opt)).pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame_line2, text=options[3], style="Oval.TButton", command=lambda opt=options[3]: self.check_answer(opt)).pack(side=tk.LEFT, padx=5)

        ttk.Button(self.root, text="Skip", style="Oval.TButton", command=self.skip_question).pack(pady=5)

        self.timer_label = ttk.Label(self.root, text="Total Time Left: 1:00", foreground="green", font=("Arial", 10, "bold", "italic"))
        self.timer_label.place(x=10, y=10)

        self.counter_label = ttk.Label(self.root, text=f"Question: {self.questions_attempted}/{self.total_questions}", font=("Arial", 10, "bold", "italic"))
        self.counter_label.place(x=10, y=40)

        self.feedback_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)

    # Skip the current question
    def skip_question(self):
        self.next_question()

    # Check the answer to the current question
    def check_answer(self, selected_option):
        if selected_option == self.correct_option:
            self.score += 1
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text=f"Wrong! Correct: {self.correct_option}", foreground="red")

        self.root.after(500, self.next_question)

    # Show the final score and the quiz completion time
    def show_score(self):
        self.clear_screen()
        completion_time = int(time.time() - self.start_time)

        conn = connect_database()
        if conn is None:
            self.feedback_label.config(text="Failed to connect to the database")
            return

        cursor = conn.cursor()
        cursor.execute("INSERT INTO marks (user_id, score) VALUES (%s, %s)", (self.current_user_id, self.score))
        cursor.execute("INSERT INTO quiz_times (user_id, completion_time) VALUES (%s, %s)", (self.current_user_id, completion_time))
        conn.commit()
        conn.close()

        ttk.Label(self.root, text=f"Quiz Completed! Your score: {self.score}/{self.total_questions}", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.root, text=f"Time Taken: {completion_time} seconds", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.root, text="Back to Dashboard", style="Oval.TButton", command=self.dashboard).pack(pady=10)

    # View the user's marks
    def view_my_marks(self):
        self.clear_screen()
        conn = connect_database()
        if conn is None:
            self.feedback_label.config(text="Failed to connect to the database")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT score, completion_time FROM marks JOIN quiz_times ON marks.user_id = quiz_times.user_id WHERE marks.user_id = %s", (self.current_user_id,))
        records = cursor.fetchall()
        conn.close()

        ttk.Label(self.root, text="Your Quiz Attempts", font=("Arial", 16)).pack(pady=10)

        for i, record in enumerate(records, start=1):
            ttk.Label(self.root, text=f"Attempt {i}: Score = {record[0]}, Time Taken = {record[1]} seconds").pack()

        ttk.Button(self.root, text="Back to Dashboard", style="Oval.TButton", command=self.dashboard).pack(pady=10)

    # View all users' marks and completion times (for admin)
    def view_all_marks(self):
        self.clear_screen()
        conn = connect_database()
        if conn is None:
            self.feedback_label.config(text="Failed to connect to the database")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT users.username, marks.score, quiz_times.completion_time FROM users JOIN marks ON users.id = marks.user_id JOIN quiz_times ON users.id = quiz_times.user_id")
        records = cursor.fetchall()
        conn.close()

        ttk.Label(self.root, text="All Users' Marks", font=("Arial", 16)).pack(pady=10)

        for record in records:
            ttk.Label(self.root, text=f"{record[0]}: {record[1]} points, {record[2]} seconds").pack()

        ttk.Button(self.root, text="Back to Dashboard", style="Oval.TButton", command=self.dashboard).pack(pady=10)

    # Modify quizzes (for admin)
    def modify_quizzes(self):
        self.clear_screen()
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Modify Quizzes", font=("Arial", 24, "bold")).pack(pady=20)
        ttk.Button(main_frame, text="Add New Question", style="Oval.TButton", command=self.add_question_screen).pack(pady=20)
        ttk.Button(main_frame, text="Back to Dashboard", style="Oval.TButton", command=self.dashboard).pack(pady=10)

    # Screen to add a new question (for admin)
    def add_question_screen(self):
        self.clear_screen()
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Add New Question", font=("Arial", 24, "bold")).pack(pady=20)
        ttk.Label(main_frame, text="Question", font=("Arial", 14)).pack(pady=5)
        self.new_question_entry = ttk.Entry(main_frame, font=("Arial", 14), width=30)
        self.new_question_entry.pack(pady=5)

        for i, opt in enumerate(["Option 1", "Option 2", "Option 3", "Option 4"], start=1):
            ttk.Label(main_frame, text=opt, font=("Arial", 14)).pack(pady=5)
            setattr(self, f"new_option{i}_entry", ttk.Entry(main_frame, font=("Arial", 14), width=30))
            getattr(self, f"new_option{i}_entry").pack(pady=5)

        ttk.Label(main_frame, text="Correct Answer", font=("Arial", 14)).pack(pady=5)
        self.new_correct_answer_entry = ttk.Entry(main_frame, font=("Arial", 14), width=30)
        self.new_correct_answer_entry.pack(pady=5)

        ttk.Button(main_frame, text="Add Question", style="Oval.TButton", command=self.add_question).pack(pady=20)
        ttk.Button(main_frame, text="Back", style="Oval.TButton", command=self.modify_quizzes).pack(pady=10)

    # Add a new question to the database 
    def add_question(self):
        question = self.new_question_entry.get()
        option1 = self.new_option1_entry.get()
        option2 = self.new_option2_entry.get()
        option3 = self.new_option3_entry.get()
        option4 = self.new_option4_entry.get()
        correct_answer = self.new_correct_answer_entry.get()

        if question and option1 and option2 and option3 and option4 and correct_answer:
            try:
                conn = connect_database()
                if conn is None:
                    self.feedback_label.config (text="Failed to connect to the database")
                    return

                cursor = conn.cursor()
                cursor.execute("INSERT INTO flashcards (question, option1, option2, option3, option4, correct_answer) VALUES (%s, %s, %s, %s, %s, %s)",
                               (question, option1, option2, option3, option4, correct_answer))
                conn.commit()
                conn.close()
                self.feedback_label.config(text="Question added successfully!", foreground="green")
                self.modify_quizzes()
            except mysql.connector.Error as err:
                self.feedback_label.config(text=f"Error adding question: {err}")
        else:
            self.feedback_label.config(text="Please fill in all fields")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardQuizApp(root)
    root.mainloop()
