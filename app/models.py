from pydantic import BaseModel
from typing import Optional, Any

class StepAction(BaseModel):
    action: str  # the agent's response/answer

class StepResult(BaseModel):
    state: dict
    reward: float       # 0.0 to 1.0
    done: bool
    info: dict

class ResetResult(BaseModel):
    state: dict
    task_id: str
    instructions: str

class StateResult(BaseModel):
    state: dict
    task_id: str
    done: bool
