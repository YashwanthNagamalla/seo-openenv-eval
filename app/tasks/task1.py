import random

SAMPLES = [
    {"meta_desc": "", "expected": "MISSING"},
    {"meta_desc": "Too short", "expected": "TOO_SHORT"},
    {"meta_desc": "A" * 170, "expected": "TOO_LONG"},
    {"meta_desc": "This is a perfectly valid meta description for an SEO audit.", "expected": "VALID"},
]

def run_task1():
    sample = random.choice(SAMPLES)
    state = {
        "page_url": "https://example.com/sample-page",
        "meta_description": sample["meta_desc"],
        "title": "Sample Page | Example"
    }
    return sample, state

def grade_task1(action: str, task_data: dict) -> float:
    action = action.strip().upper()
    expected = task_data["expected"]
    if action == expected:
        return 1.0
    # Partial credit
    if expected == "TOO_SHORT" and action in ["MISSING", "VALID"]:
        return 0.3
    return 0.0
