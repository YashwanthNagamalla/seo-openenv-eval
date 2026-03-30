import os
from openai import OpenAI
import requests
import json
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-3-flash-preview")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
ENV_URL = os.environ.get("ENV_URL", "http://localhost:8080")

if not HF_TOKEN:
    print("Please set HF_TOKEN environment variable in .env or your system.")
    exit(1)

client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL
)

TASKS = ["meta_description_check", "alt_tag_audit", "full_onpage_audit"]

def run_episode(task_id: str) -> float:
    reset_resp = requests.post(f"{ENV_URL}/reset", params={"task_id": task_id})
    data = reset_resp.json()
    state = data["state"]
    instructions = data["instructions"]

    prompt = f"""You are an SEO expert agent. 
Task: {instructions}
Page data: {json.dumps(state, indent=2)}
Respond with ONLY your bare answer, no explanation. Do not wrap in markdown or backticks."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        action = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  [API Error] Could not generate response: {type(e).__name__}: {str(e)}")
        print("  Please make sure your API Key and Base URL are correctly configured.")
        return 0.0
    
    # Strip markdown backticks robustly if the model still uses them
    action = action.strip()
    if action.startswith("```"):
        # Remove the first line (e.g. ```json)
        first_newline = action.find('\n')
        if first_newline != -1:
            action = action[first_newline+1:]
        # Remove the closing backticks
        if action.endswith("```"):
            action = action[:-3].strip()

    # Highly robust JSON extraction fallback
    if task_id in ["alt_tag_audit", "full_onpage_audit"]:
        import re
        if task_id == "full_onpage_audit":
            match = re.search(r'\{.*\}', action, re.DOTALL)
        else:
            match = re.search(r'\[.*\]', action, re.DOTALL)
        if match:
            action = match.group(0).strip()
            
    print(f"  Agent action: {action}")

    step_resp = requests.post(f"{ENV_URL}/step", json={"action": action})
    result = step_resp.json()
    print(f"  Reward: {result['reward']}")
    return result["reward"]

if __name__ == "__main__":
    scores = {}
    for task in TASKS:
        print(f"\nRunning task: {task}")
        score = run_episode(task)
        scores[task] = score

    print("\n=== FINAL SCORES ===")
    for task, score in scores.items():
        print(f"{task}: {score:.2f}")
    print(f"Average: {sum(scores.values())/len(scores):.2f}")
