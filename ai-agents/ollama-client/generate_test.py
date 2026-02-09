import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"


def generate_code(prompt):

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=data)
    result = response.json()

    return result["response"]


if __name__ == "__main__":

    prompt = """
    Create a Selenium Java TestNG test for login page
    using Page Object Model and proper waits.
    """

    code = generate_code(prompt)

    print("\n===== AI GENERATED CODE =====\n")
    print(code)
