from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Radiology Education Service")

class Case(BaseModel):
    id: str
    title: str
    description: str
    study_instance_uid: str
    tags: List[str]
    is_public: bool = True

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer_index: int

class Quiz(BaseModel):
    id: str
    case_id: str
    questions: List[QuizQuestion]

# Mock Database
cases_db = {}
quizzes_db = {}

@app.post("/cases", response_model=Case)
async def create_case(case: Case):
    cases_db[case.id] = case
    return case

@app.get("/cases", response_model=List[Case])
async def get_cases():
    return list(cases_db.values())

@app.get("/cases/{case_id}", response_model=Case)
async def get_case(case_id: str):
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Case not found")
    return cases_db[case_id]

@app.post("/quizzes", response_model=Quiz)
async def create_quiz(quiz: Quiz):
    quizzes_db[quiz.id] = quiz
    return quiz

@app.get("/quizzes/{case_id}", response_model=List[Quiz])
async def get_quizzes_for_case(case_id: str):
    return [q for q in quizzes_db.values() if q.case_id == case_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
