# Study-Tracker
A command-line study tracking application built with Python and MySQL. This project helps students record their study sessions, track the time spent on different subjects, and view detailed reports to monitor their progress over time.

## Features

- Add study sessions
- View all study records
- Update existing entries
- Track total study time
- View subject-wise study statistics
- Check today's study summary
- View monthly study records
- Calculate monthly study time
- Generate weekly study reports

## Technologies Used
* Python
* MySQL
* mysql-connector-python
* tabulate

## What the Application Tracks

Each study session includes:
* Date
* Day
* Subject
*Topic Studied
* Study Time

The data is stored in a MySQL database, making it easy to retrieve and analyze study habits over time.

## How to Run

- Install the required packages:
pip install mysql-connector-python tabulate

- Create a MySQL database named "study_tracker".

- Create the required table:

CREATE TABLE study_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    day VARCHAR(20),
    subject VARCHAR(50),
    topic VARCHAR(255),
    study_time TIME
);

- Update the database credentials in the Python file.

- Run the application:
python study_tracker.py

## Reports Available
* Total Study Time
* Subject-wise Statistics
* Today's Summary
* Monthly View
* Monthly Total Study Time
* Weekly Report

## Purpose
As a student, I wanted a way to keep track of my study hours and monitor my progress over time. Building this project helped me practice Python, MySQL, database management, SQL queries, and data analysis while creating something that I could actually use in my daily life.

## Future Improvements
* Study streak tracking
* Goal setting and progress monitoring
* Data visualization using charts
* CSV/PDF report exports
* Graphical User Interface (GUI)
* Subject-wise performance trends