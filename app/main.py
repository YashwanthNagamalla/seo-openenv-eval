from fastapi import FastAPI
from app.models import StepAction, StepResult, ResetResult, StateResult
from app.environment import env

app = FastAPI(title="SEO Audit OpenEnv")

@app.get("/")
def root():
    return {"status": "ok", "env": "seo-audit-env"}

@app.post("/reset", response_model=ResetResult)
def reset(task_id: str = None):
    return env.reset(task_id)

@app.post("/step", response_model=StepResult)
def step(action: StepAction):
    return env.step(action.action)

@app.get("/state", response_model=StateResult)
def state():
    return env.state()

@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {"id": "meta_description_check", "difficulty": "easy"},
            {"id": "alt_tag_audit", "difficulty": "medium"},
            {"id": "full_onpage_audit", "difficulty": "hard"}
        ]
    }
