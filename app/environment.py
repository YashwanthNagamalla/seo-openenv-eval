import random
from app.tasks.task1 import run_task1, grade_task1
from app.tasks.task2 import run_task2, grade_task2
from app.tasks.task3 import run_task3, grade_task3

TASKS = ["meta_description_check", "alt_tag_audit", "full_onpage_audit"]

class SEOEnvironment:
    def __init__(self):
        self.current_task = None
        self.current_state = {}
        self.done = False
        self.task_data = {}

    def reset(self, task_id: str = None):
        self.done = False
        self.current_task = task_id or random.choice(TASKS)

        if self.current_task == "meta_description_check":
            self.task_data, self.current_state = run_task1()
            instructions = "Check if this page has a valid meta description (50-160 chars). Reply with: MISSING, TOO_SHORT, TOO_LONG, or VALID."
        elif self.current_task == "alt_tag_audit":
            self.task_data, self.current_state = run_task2()
            instructions = "Find all images missing alt tags. Return a JSON list of src URLs."
        else:
            self.task_data, self.current_state = run_task3()
            instructions = "Audit this page. Return JSON with keys: title_ok, h1_ok, meta_desc_ok, canonical_ok and a 'fixes' list."

        return {
            "state": self.current_state,
            "task_id": self.current_task,
            "instructions": instructions
        }

    def step(self, action: str):
        if self.current_task == "meta_description_check":
            reward = grade_task1(action, self.task_data)
        elif self.current_task == "alt_tag_audit":
            reward = grade_task2(action, self.task_data)
        else:
            reward = grade_task3(action, self.task_data)

        self.done = True
        return {
            "state": self.current_state,
            "reward": round(reward, 2),
            "done": self.done,
            "info": {"task_id": self.current_task}
        }

    def state(self):
        return {
            "state": self.current_state,
            "task_id": self.current_task,
            "done": self.done
        }

env = SEOEnvironment()  # singleton
