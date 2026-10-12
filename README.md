Student Database CRUD API

Project Overview

The Student Database CRUD API is a beginner-friendly backend application developed using Python, FastAPI, and SQLite. It allows users to manage student records through REST API endpoints.

Technologies Used

- Python
- FastAPI
- SQLite
- Uvicorn

Features

- Create a new student record
- View all student records
- Retrieve a student by ID
- Update student details
- Delete a student record
- Store student data in an SQLite database

API Endpoints

Method| Endpoint| Description
POST| "/students"| Create a student
GET| "/students"| View all students
GET| "/students/{student_id}"| Retrieve a student by ID
PATCH| "/students/{student_id}"| Update student details
DELETE| "/students/{student_id}"| Delete a student

How to Run the Project

1. Install Python.

2. Install the required packages using "pip install -r requirements.txt".

3. Start the server using:
   
   "python -m uvicorn main:app --reload"

4. Open "http://127.0.0.1:8000/docs" in your browser to test the API.

Database

Student records are stored locally in an SQLite database named "students.db".

Project Status

Completed the main CRUD operations and tested the API endpoints using FastAPI Swagger UI.
