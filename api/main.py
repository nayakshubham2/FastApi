from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import csv
from pathlib import Path

app = FastAPI()

# Enable CORS to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

csv_path = Path(__file__).parent / "q-fastapi.csv"
# Load data from CSV once when the server starts
students_data = []
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Ensure studentId is int
        students_data.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })

@app.get("/")
def get_students():
    return {"students": student_data}
    
@app.get("/api")
def get_students_in_a_class(class_: Optional[List[str]] = Query(None, alias="class")):
    if class_:
        filtered = [student for student in students_data if student["class"] in class_]
    else:
        filtered = students_data
    return {"students": filtered}
