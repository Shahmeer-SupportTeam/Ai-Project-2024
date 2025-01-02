# :book: Flashcard Quiz App

## :rocket: Introduction

The **Flashcard Quiz App** is an interactive and educational tool designed to help users learn through multiple-choice questions (**MCQs**). The app offers real-time feedback, tracks performance, and features an intuitive user interface. Developed with **Python** for the backend and **tkinter** for the GUI, this app provides an engaging learning experience.

---

## :bulb: Objectives

- Build an **interactive quiz app** with Python and tkinter.
- Store quiz questions and answers in a **MySQL** database for dynamic content.
- Provide **real-time feedback** and performance tracking.
- Ensure a **user-friendly interface** for both users and administrators.

---

## :zap: Features

### :star: Core Features

- **Dynamic Question Bank**: 
  - Questions and answers stored in a **MySQL** database, ensuring scalability and ease of modification.

- **Quiz Functionality**:
  - Displays questions one at a time with immediate feedback upon answer submission.

- **Performance Tracking**:
  - Calculates and shows the total score after completing the quiz.

- **Graphical User Interface (GUI)**:
  - A sleek, user-friendly interface powered by **tkinter**.

### :guardsman: Admin Features

- View all users' quiz marks.
- Add, edit, or remove quiz questions.
- **Logout functionality** for secure access.

### :bust_in_silhouette: User Features

- Users can attempt the quiz and track their scores.
- Users can only view their own marks — not others’.

---

## :wrench: Tools & Technologies

- **Programming Language**: Python
- **Libraries Used**:
  - `tkinter`: For GUI development.
  - `mysql-connector-python`: For MySQL database interaction.
- **Database**: **MySQL** database (`flashcard_quiz_app`).

---

## :rocket: Implementation

### :file_folder: Workflow

1. **MySQL Database Connection**:
   - The app connects to a **MySQL** database (`flashcard_quiz_app`), fetching questions for each quiz round.
  
2. **Interactive Questions**:
   - Displays one question at a time with choices, allowing users to submit answers.

3. **Instant Feedback**:
   - Upon submission, users receive real-time feedback:
     - **Correct**: The score increases and a "Correct!" message is shown.
     - **Incorrect**: Shows the correct answer and feedback.

4. **Quiz Conclusion**:
   - At the end of the quiz, the total score is displayed.

---

## :computer: Code Structure

- `load_flashcards()` - Retrieves questions and answers from the MySQL database.
- `next_question()` - Manages the display of the next question.
- `check_answer()` - Validates user input and updates the score.

### :art: GUI Elements:

- **Labels** for displaying questions and feedback.
- **Entry fields** for submitting answers.
- **Buttons** for navigating through the quiz.

---

## :family: Team Members & Roles

### :man_office_worker: **Umer** (Work on Backend) - [GitHub](https://github.com/Umar0075)

- Led backend development and logic implementation.
- Worked on the flashcards functionality and layout.
- Ensured smooth communication between backend and database.

### :man_technologist: **Shahmeer** (Work on Frontend) - [GitHub](https://github.com/Shahmeer-SupportTeam)

- Designed and implemented the app’s user interface using **tkinter**.
- Created and maintained the **MySQL** database.
- Contributed to integrating the database with the front-end.

### :man_student: **Yusha** (Database & Connectivity) - [GitHub](https://github.com/Yusha78)

- Designed and developed the **MySQL** database.
- Managed data retrieval and database connectivity.
- Managed database connectivity and integrity.


### :man_mechanic: **Mujtaba** (QA Tester & Bug Fixes) - [GitHub](https://github.com/Mujtaba-ali999)

- Identified and fixed bugs, improving the app’s stability.
- Worked on enhancing **labels** and user experience.
- Conducted usability testing to improve the app.

---

## :hammer_and_wrench: Challenges & Solutions

- **Challenge**: Synchronizing tasks across different team members.
  - **Solution**: Regular meetings and well-defined role assignments ensured smooth collaboration.

- **Challenge**: Dealing with database connection issues.
  - **Solution**: Implemented error handling to tackle potential database connection failures.

- **Challenge**: Designing an intuitive and user-friendly interface.
  - **Solution**: Simplified the GUI, ensuring clarity with clear instructions, labels, and intuitive navigation.

---

## :trophy: Results

- Developed a **fully functional** Flashcard Quiz App.
- Gained valuable experience in team collaboration, programming, and testing.
- Established a **scalable foundation** for future improvements like new question types and user profiles.

---

## :chart_with_upwards_trend: Future Enhancements

- **User Profiles**: Implement authentication to track user progress over time.
- **Scalable Databases**: Migrate to advanced databases like **PostgreSQL** for scalability.
- **Multimedia Integration**: Add image/audio-based questions for more interactive quizzes.
- **Timed Quizzes**: Introduce a countdown timer for added challenge.

---

## :memo: Conclusion

The **Flashcard Quiz App** project allowed us to apply Python programming, **GUI design**, and **database management** in a practical scenario. We learned key skills in teamwork, problem-solving, and project execution. This app serves as a solid foundation for future enhancements and offers an engaging way for users to learn new concepts.

---


---

