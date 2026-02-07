import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# Change path if your repo is elsewhere
PROJECT_PATH = "../../selenium-ai-framework/src/test/java/tests"


def ask_ai(prompt):

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    res = requests.post(OLLAMA_URL, json=data)
    return res.json()["response"]


def clean_code(code):

    # Remove markdown if AI adds it
    if "```" in code:
        code = code.split("```")[1]

    return code.strip()


def save_test(class_name, code):

    file_path = os.path.join(PROJECT_PATH, f"{class_name}.java")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Saved: {file_path}")


if __name__ == "__main__":
    prompt = """
You are a Senior Selenium Automation Engineer.

Target website:
https://opensource-demo.orangehrmlive.com

Task:
Create a Selenium Java TestNG test class
to validate successful login.

Rules:
- Use only real elements from the site
- Do NOT invent IDs
- Prefer text-based or stable XPath
- Verify 'Dashboard' text after login
- Use WebDriverWait
- Extend BaseTest
- Use existing LoginPage
- Add assertion

Class name: DashboardTest
Package: tests
    """


    print("Sending prompt to AI...")

    ai_code = ask_ai(prompt)

    final_code = clean_code(ai_code)

    save_test("DashboardTest", final_code)

    print("\nDone. Test created.")
