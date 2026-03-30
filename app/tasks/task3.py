import random, json

def run_task3():
    scenarios = [
        {
            "title": "A" * 80,   # too long
            "h1": "Welcome",
            "meta_desc": "Good description here that fits nicely.",
            "canonical": "",     # missing
            "expected": {"title_ok": False, "h1_ok": True, "meta_desc_ok": True, "canonical_ok": False}
        },
        {
            "title": "Good Title",
            "h1": "",            # missing
            "meta_desc": "",     # missing
            "canonical": "https://example.com/page",
            "expected": {"title_ok": True, "h1_ok": False, "meta_desc_ok": False, "canonical_ok": True}
        }
    ]
    s = random.choice(scenarios)
    state = {k: v for k, v in s.items() if k != "expected"}
    state["page_url"] = "https://example.com/page"
    return {"expected": s["expected"]}, state

def grade_task3(action: str, task_data: dict) -> float:
    try:
        predicted = json.loads(action)
        expected = task_data["expected"]
        keys = ["title_ok", "h1_ok", "meta_desc_ok", "canonical_ok"]
        correct = sum(1 for k in keys if predicted.get(k) == expected.get(k))
        return round(correct / len(keys), 2)
    except:
        return 0.0
