from flask import Flask, jsonify
import os

app = Flask(__name__)

PROJECT_ROOT = os.path.abspath("../selenium-ai-framework")

def collect_context():
    context = {}
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    relative_path = file_path.replace(PROJECT_ROOT, "")
                    context[relative_path] = f.read()
    return context

@app.route("/context", methods=["GET"])
def get_context():
    return jsonify(collect_context())

if __name__ == "__main__":
    app.run(port=3333)
