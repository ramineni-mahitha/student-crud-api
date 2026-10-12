from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

from database import create_table, get_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


app = FastAPI(
    title="Student Database CRUD API",
    lifespan=lifespan
)


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    date_of_birth: str
    email: EmailStr | None = None
    phone: str | None = None
    course: str | None = None
    address: str | None = None
    enrollment_date: str | None = None


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    course: str | None = None
    address: str | None = None
    enrollment_date: str | None = None


def row_to_dict(row):
    return dict(row)


@app.get("/")
def home():
    return {"message": "Student Database API is running!"}


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    connection = get_connection()
    try:
        cursor = connection.execute(
            """INSERT INTO students
            (name, date_of_birth, email, phone, course, address, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                student.name, student.date_of_birth, student.email,
                student.phone, student.course, student.address,
                student.enrollment_date
            )
        )
        connection.commit()
        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (cursor.lastrowid,)
        ).fetchone()
        return row_to_dict(row)
    except Exception as error:
        connection.rollback()
        if "UNIQUE constraint failed" in str(error):
            raise HTTPException(status_code=409, detail="Email already exists")
        raise
    finally:
        connection.close()


@app.get("/students")
def list_students():
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT * FROM students ORDER BY student_id"
        ).fetchall()
        return [row_to_dict(row) for row in rows]
    finally:
        connection.close()


@app.get("/students/{student_id}")
def get_student(student_id: int):
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return row_to_dict(row)
    finally:
        connection.close()


@app.patch("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    changes = student.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided")

    connection = get_connection()
    try:
        existing = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Student not found")

        for field, value in changes.items():
            if value is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"{field} cannot be null"
                )

        assignments = ", ".join(f"{field} = ?" for field in changes)
        values = list(changes.values()) + [student_id]

        connection.execute(
            f"UPDATE students SET {assignments} WHERE student_id = ?",
            values
        )
        connection.commit()

        updated = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()
        return row_to_dict(updated)
    except Exception as error:
        connection.rollback()
        if "UNIQUE constraint failed" in str(error):
            raise HTTPException(status_code=409, detail="Email already exists")
        raise
    finally:
        connection.close()


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_connection()
    try:
        cursor = connection.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        connection.commit()
        return {"message": "Student deleted successfully"}
    finally:
        connection.close()