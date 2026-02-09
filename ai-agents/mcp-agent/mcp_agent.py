import requests

# ---------------- CONFIG ---------------- #

OLLAMA_URL = "http://localhost:11434/api/generate"
CONTEXT_URL = "http://localhost:3333/context"
MODEL = "qwen2.5:1.5b"

MAX_CONTEXT_CHARS = 500  # limit per file to avoid token overload

# ---------------- CONTEXT ---------------- #

def get_project_context():
    """
    Fetches project context from local context server
    and trims large files for LLM safety.
    """
    try:
        response = requests.get(CONTEXT_URL)
        response.raise_for_status()
        context_json = response.json()
    except Exception as e:
        return f"ERROR: Unable to fetch context - {e}"

    trimmed_context = {}

    for file_path, content in context_json.items():
        trimmed_context[file_path] = content[:MAX_CONTEXT_CHARS]

    return str(trimmed_context)

# ---------------- AI CALL ---------------- #

def ask_ai(prompt, context):
    """
    Sends prompt + context to Ollama and safely parses response.
    """
    payload = {
        "model": MODEL,
        "prompt": f"""
You are a Senior QA Automation Engineer.

Project Context:
{context}

Task:
{prompt}
""",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"ERROR: Ollama request failed - {e}"

    # Defensive parsing (VERY IMPORTANT)
    if isinstance(data, dict):
        if "response" in data:
            return data["response"]
        if "message" in data:
            return data["message"]
        if "error" in data:
            return f"OLLAMA ERROR: {data['error']}"

    return f"Unexpected Ollama response: {data}"

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    print("\n🔹 Fetching project context...")
    context = get_project_context()

    if context.startswith("ERROR"):
        print(context)
        exit(1)

    print("✅ Context fetched successfully\n")

    prompt = """
Review the Selenium automation framework and suggest
improvements to increase test stability and maintainability.
Focus on waits, locators, and framework structure.
"""

    print("🔹 Sending prompt to AI...\n")
    ai_response = ask_ai(prompt, context)

    print("🤖 AI RESPONSE:\n")
    print(ai_response)