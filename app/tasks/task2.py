import random, json

def run_task2():
    images = [
        {"src": "/img/hero.jpg", "alt": "Hero banner"},
        {"src": "/img/logo.png", "alt": ""},           # missing
        {"src": "/img/team.jpg", "alt": "Our team"},
        {"src": "/img/product.png", "alt": ""},        # missing
        {"src": "/img/icon.svg", "alt": "Menu icon"},
    ]
    missing = [img["src"] for img in images if img["alt"] == ""]
    state = {"page_url": "https://example.com/about", "images": images}
    return {"missing_alts": missing}, state

def grade_task2(action: str, task_data: dict) -> float:
    try:
        predicted = json.loads(action)
        if not isinstance(predicted, list):
            return 0.0
        expected = set(task_data["missing_alts"])
        predicted_set = set(predicted)
        if not expected:
            return 1.0 if not predicted_set else 0.0
        tp = len(expected & predicted_set)
        precision = tp / len(predicted_set) if predicted_set else 0
        recall = tp / len(expected)
        if precision + recall == 0:
            return 0.0
        f1 = 2 * precision * recall / (precision + recall)
        return round(f1, 2)
    except:
        return 0.0
