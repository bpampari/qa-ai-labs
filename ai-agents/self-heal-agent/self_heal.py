import subprocess
import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
CONTEXT_URL = "http://localhost:3333/context"
MODEL = "qwen2.5:1.5b"

BASE_DIR = os.path.abspath("../../selenium-ai-framework")

def run_tests():
    print("Running Maven tests...\n")

    result = subprocess.run(
        ["mvn", "test"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        shell=True
    )

    return result.stdout + result.stderr

def get_context():
    project_context = requests.get(CONTEXT_URL).text

    html_path = os.path.join(BASE_DIR, "page-source.html")
    html_content = ""

    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            html_content = f.read()[:6000]

    return f"""
PROJECT CONTEXT:
{project_context}

PAGE HTML:
{html_content}
"""

def clean_ai_output(text):
    # Remove markdown fences
    if "```" in text:
        parts = text.split("```")
        if len(parts) > 1:
            text = parts[1]

    # Remove accidental leading "java"
    lines = text.strip().splitlines()
    if lines and lines[0].strip().lower() == "java":
        lines = lines[1:]

    return "\n".join(lines).strip()


def ask_ai(failure_log, context):

    prompt = f"""
You are a Senior Selenium Automation Fixing Agent.

Project Context:
{context}

Test Failure (last 1500 chars):
{failure_log[-1500:]}

TASK:
1. Inspect PAGE HTML.
2. Fix only incorrect locator.
3. Keep all existing imports.
4. Do NOT remove or modify imports.
5. Return FULL valid Java file.
6. Do NOT add markdown.
7. Do NOT add explanation.
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=180
    )

    data = response.json()

    if "response" in data:
        return clean_ai_output(data["response"])

    return "No fix returned"

def overwrite_file(java_code):

    file_path = os.path.join(
        BASE_DIR,
        "src",
        "test",
        "java",
        "pages",
        "LoginPage.java"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(java_code)

    print(f"\nUpdated file: {file_path}")

if __name__ == "__main__":

    logs = run_tests()

    if "BUILD SUCCESS" in logs:
        print("Tests already passing. No healing needed.")
        exit()

    print("Failure detected. Sending to AI...\n")

    context = get_context()
    fix_code = ask_ai(logs, context)

    print("\nAI Suggested Fix:\n")
    print(fix_code)

    if "package pages" not in fix_code:
        print("⚠️ AI output invalid. Skipping overwrite.")
        exit()
    overwrite_file(fix_code)

    print("\nRe-running tests after fix...\n")
    new_logs = run_tests()

    if "BUILD SUCCESS" in new_logs:
        print("✅ Self-healing successful!")
    else:
        print("❌ Fix attempt failed. Manual review required.")
